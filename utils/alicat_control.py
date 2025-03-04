import asyncio
from alicat import FlowController

"""
Original Plan:
- First 5 minutes: emit only air.
- After first 5 minutes: emit CO2 every 5 minutes for 5 seconds.
- After first 5 minutes: emit odor every 5 minutes for 2 seconds in addition to air and CO2.
"""

error_counter = 0
odor = "H2"  # Change odor here
initial_air_duration = 0 # first _ minutes, only emit air
co2_interval = 5*60 # emit CO2 every _ minutes
co2_duration = 5 # emit CO2 for _ seconds
co2_and_odor_interval = 60*60 # emit CO2 and odor every _ minutes
co2_and_odor_duration = 2 # emit CO2 and odor for _ seconds

async def change_flow(flow_controller, gas, flow_rate):
    await flow_controller.set_gas(gas)
    await flow_controller.set_flow_rate(flow_rate)
    return await flow_controller.get()

# Emit only air
async def set_air_only(controller1, controller2, controller3):
    await asyncio.gather(
        change_flow(controller1, 'Air', 200),
        change_flow(controller2, 'CO2', 0),
        change_flow(controller3, odor, 0)
    )
    print("Air only: Controller1 (Air) at 200 SCCM")

# Emit air and CO2
async def set_air_and_co2(controller1, controller2, controller3):
    await asyncio.gather(
        change_flow(controller1, 'Air', 170),
        change_flow(controller2, 'CO2', 30),
        change_flow(controller3, odor, 0)
    )
    print("Air and CO2: Controller1 (Air) at 170 SCCM, Controller2 (CO2) at 30 SCCM")

# Emit air, CO2, and odor
async def set_air_co2_and_odor(controller1, controller2, controller3):
    await asyncio.gather(
        change_flow(controller1, 'Air', 140),
        change_flow(controller2, 'CO2', 30),
        change_flow(controller3, odor, 30)
    )
    print(f"Air, CO2, and {odor}: Controller1 (Air) at 170 SCCM, Controller2 (CO2) at 30 SCCM, Controller3 ({odor}) at 30 SCCM")

async def manage_states(controller1, controller2, controller3):
    # Emit air only
    await set_air_only(controller1, controller2, controller3)
    await asyncio.sleep(initial_air_duration)

    # Emit CO2
    while True:
        print("Phase: Air and CO2")
        await set_air_and_co2(controller1, controller2, controller3)
        await asyncio.sleep(co2_duration)
        await set_air_only(controller1, controller2, controller3)
        await asyncio.sleep(co2_interval - co2_duration)

        # Emit CO2 and odor
        print("Phase: Air, CO2, and Odor")
        await set_air_co2_and_odor(controller1, controller2, controller3)
        await asyncio.sleep(co2_and_odor_duration)
        await set_air_only(controller1, controller2, controller3)
        await asyncio.sleep(co2_and_odor_interval - co2_and_odor_duration)

async def main():
    global error_counter

    try:
        # Retry logic
        while error_counter < 5:
            try:
                async with FlowController('/dev/ttyController1') as controller3, \
                           FlowController('/dev/ttyController2') as controller2, \
                           FlowController('/dev/ttyController3') as controller1:
                    print(await controller1.get())
                    print(await controller2.get())
                    print(await controller3.get())

                    print("Starting gas emission!")
                    await manage_states(controller1, controller2, controller3)
                break

            except Exception as e:
                error_counter += 1
                print(f"Attempt: {error_counter}")
                print(f"Error: {e}")
                if error_counter >= 5:
                    print("Max retry limit reached, stopping.")
                    raise e

    except Exception as e:
        print(f"Error: {e}")
        raise Exception("Will not try again, have tried 5 times") from e

    finally:
        print("bye")

if __name__ == "__main__":
    asyncio.run(main())
