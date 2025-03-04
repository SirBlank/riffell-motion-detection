import asyncio
from alicat import FlowController

error_counter = 0

async def main():
    global error_counter
    try:
        # Retry logic
        while error_counter < 5:
            try:
                async with FlowController('/dev/ttyController1') as flow_controller1:
                    print(await flow_controller1.get())
                    await flow_controller1.set_gas('Air')
                    await flow_controller1.set_flow_rate(1)
                async with FlowController('/dev/ttyController2') as flow_controller2:
                    print(await flow_controller2.get())
                    await flow_controller2.set_gas('Air')
                    await flow_controller2.set_flow_rate(2)
                async with FlowController('/dev/ttyController3') as flow_controller3:
                    print(await flow_controller3.get())
                    await flow_controller3.set_gas('Air')
                    await flow_controller3.set_flow_rate(3)
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

asyncio.run(main())
