import asyncio
from alicat import FlowController
import signal
import sys
import csv
import time
from datetime import datetime
import os

# Configuration
error_counter = 0
odor = "H2"  # Change odor here

# Default flow rates for toggling
odor_on = 200
co2_on= 200

def signal_handler(sig, frame):
    print("Mass Flow Controllers exiting gracefully...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

async def change_flow(flow_controller, gas, flow_rate):
    await flow_controller.set_gas(gas)
    await flow_controller.set_flow_rate(flow_rate)
    return await flow_controller.get()

async def adjust_flows(controller_air, controller_co2, controller_odor,
                       air_flow, co2_flow, odor_flow, csv_writer=None):
    """
    Adjust flows for each controller, and log changes to CSV if csv_writer is provided.
    """
    await asyncio.gather(
        change_flow(controller_air, 'Air', air_flow),
        change_flow(controller_co2, 'CO2', co2_flow),
        change_flow(controller_odor, odor, odor_flow)
    )
    print(f"Adjusted flows: Air={air_flow} SCCM, CO2={co2_flow} SCCM, {odor}={odor_flow} SCCM")

    # Log to CSV
    if csv_writer:
        timestamp = datetime.now()
        csv_writer.writerow([timestamp, air_flow, co2_flow, odor_flow])

async def keyboard_listener(controller_air, controller_co2, controller_odor, csv_writer=None):
    """
    Continuously reads user input (line-based) to toggle odor (o) or CO2 (k).
    Press 'q' to exit the listener.
    """
    odor_flow = 0
    co2_flow = 0
    air_flow = 0

    while True:
        key = await asyncio.to_thread(
            input, 
            "\nEnter 0 to emit nothing \nEnter 1 to emit only Air \nEnter 2 to emit Air + CO2 \n"
            "Enter 3 to emit Air + CO2 + Odor \nEnter 4 to emit Air + Odor \nEnter q to quit: "
        )

        key = key.lower().strip()
        if key == '0':
            print("Emitting nothing")
            odor_flow = 0
            co2_flow = 0
            air_flow = 0
            await adjust_flows(controller_air, controller_co2, controller_odor,
                               air_flow, co2_flow, odor_flow, csv_writer)

        elif key == '1':
            print("Emitting Air only")
            odor_flow = 0
            co2_flow = 0
            air_flow = 200
            await adjust_flows(controller_air, controller_co2, controller_odor,
                               air_flow, co2_flow, odor_flow, csv_writer)
        
        elif key == '2':
            print("Emitting Air + CO2")
            odor_flow = 0
            co2_flow = 10
            air_flow = 190
            await adjust_flows(controller_air, controller_co2, controller_odor,
                               air_flow, co2_flow, odor_flow, csv_writer)
            
        elif key == '3':
            print("Emitting Air + CO2 + Odor")
            odor_flow = 30
            co2_flow = 10
            air_flow = 160
            await adjust_flows(controller_air, controller_co2, controller_odor,
                               air_flow, co2_flow, odor_flow, csv_writer)
        
        elif key == '4':
            print("Emitting Air + Odor")
            odor_flow = 30
            co2_flow = 0
            air_flow = 170
            await adjust_flows(controller_air, controller_co2, controller_odor,
                               air_flow, co2_flow, odor_flow, csv_writer)

        elif key == 'q':
            print("Exiting keyboard listener.")
            break

async def main():
    global error_counter

    # Create a new CSV file
    log_time = int(time.time() * 1000)
    base_folder = '/mnt/data/DATA'
    filename = os.path.join(base_folder, f'{log_time}_mass_flow.csv')

    try:
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["timestamp", "air_flow", "co2_flow", "odor_flow"])

            controller_odor = None
            controller_co2 = None
            controller_air = None

            # Retry logic for opening the controllers
            while error_counter < 5:
                try:
                    async with FlowController('/dev/ttyController1') as controller_odor, \
                               FlowController('/dev/ttyController2') as controller_co2, \
                               FlowController('/dev/ttyController3') as controller_air:
                        print(await controller_air.get())
                        print(await controller_co2.get())
                        print(await controller_odor.get())

                        print("Starting gas emission!")
                        await adjust_flows(controller_air, controller_co2, controller_odor,
                                           200, 0, 0, csv_writer)
                        
                        # Start listening to user input in the background
                        await keyboard_listener(controller_air, controller_co2, controller_odor, csv_writer)
                        
                        # After finishing keyboard listener, set all flows to 0
                        await adjust_flows(controller_air, controller_co2, controller_odor,
                                           0, 0, 0, csv_writer)
                        
                        # If keyboard_listener ends (e.g. user pressed 'q'), break
                        break

                except Exception as e:
                    error_counter += 1
                    print(f"Attempt: {error_counter}")
                    print(f"Error: {e}")
                    if error_counter >= 5:
                        print("Max retry limit reached, stopping.")
                        raise e
                finally:
                    print("Mass Flow Controllers closed")

    except Exception as e:
        print(f"Error: {e}")
        raise Exception("Will not try again, have tried 5 times") from e

if __name__ == "__main__":
    asyncio.run(main())
