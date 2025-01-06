import pywinusb.hid as hid
from time import sleep
import sys
import random

USB_CFG_VENDOR_ID = 0x16c0  # Should suit, if not check ID with a tool like USBDeview
USB_CFG_DEVICE_ID = 0x05DF  # Should suit, if not check ID with a tool like USBDeview

filter = None
hid_device = None
device = None
report = None

last_row_status = None

 
 # Find the device using usb ids 
def get_Hid_USBRelay():
    global filter, hid_device, device
    filter = hid.HidDeviceFilter(vendor_id=USB_CFG_VENDOR_ID, product_id=USB_CFG_DEVICE_ID)
    hid_device = filter.get_devices()
    device = hid_device[0]

# Opens the device to be controlled
def open_device():
    if device.is_active():
        if not device.is_opened():
            device.open()
            get_report()
            return True
        else:
            print("Device already opened")
            return True
    else:
        print("Device is not active")
    return False

# Closes the device 
def close_device():
    if device.is_active():
        if device.is_opened():
            device.close()
            return True
        else:
            print("Device already closed")
    else:
        print("Device is not active")
    return True

# Refreshes the connection between the usb and pc
def refresh():
    get_Hid_USBRelay()
    open_device()

# Checks what if the usb being used or not
def get_report():
    global report
    if not device.is_active():
        report = None

    for rep in device.find_output_reports() + device.find_feature_reports():
        report = rep

# 
def read_status_row():
    global last_row_status
    if report is None:
        print("Cannot read report")
        last_row_status = [0, 1, 0, 0, 0, 0, 0, 0, 3]
    else:
        last_row_status = report.get()
    return last_row_status


def write_row_data(buffer):
    if report is not None:
        report.send(raw_data=buffer)
        return True
    else:
        print("Cannot write in the report. check if your device is still plugged")
        return False

# Turn on all the relays
def on_all():
    if write_row_data(buffer=[0, 0xFE, 0, 0, 0, 0, 0, 0, 1]):
        return read_relay_status(relay_number=3)
    else:
        print("Cannot put ON relays")
        return False

# Turn off all the relays
def off_all():
    if write_row_data(buffer=[0, 0xFC, 0, 0, 0, 0, 0, 0, 1]):
        return read_relay_status(relay_number=3)
    else:
        print("Cannot put OFF relays")
        return False

# Turn on a specific relay
def on_relay(relay_number):
    if write_row_data(buffer=[0, 0xFF, relay_number, 0, 0, 0, 0, 0, 1]):
        return read_relay_status(relay_number)
    else:
        print("Cannot put ON relay number {}".format(relay_number))
        return False

# Turn off a specific relay
def off_relay(relay_number):
    if write_row_data(buffer=[0, 0xFD, relay_number, 0, 0, 0, 0, 0, 1]):
        return read_relay_status(relay_number)
    else:
        print("Cannot put OFF relay number {}".format(relay_number))
        return False


def read_relay_status(relay_number):
    buffer = read_status_row()
    return relay_number & buffer[8]

# Check if a relay is on
def is_relay_on(relay_number):
    return read_relay_status(relay_number) > 0




# Main function
def main():
    get_Hid_USBRelay()
    print("Found device")
    open_device()
    print("Opened device")
    # User-variable to be controlled
    time = 15
    duration = 2

    while True:

        # Wait for a certain time
        sleep(time)

        # Turn on the first relay & wait duration
        print("TURN ON 1: {} ".format(on_relay(1)))
        print("READ STATE 1: {}".format(read_relay_status(1)))
        sleep(duration)

        # Turn off the first relay & wait before turning second on
        print("TURN OFF 1: {} ".format(off_relay(1)))
        print("READ STATE 1: {}".format(read_relay_status(1)))
        sleep(5)

        # Turn on the second relay & wait duration
        print("TURN ON 2: {} ".format(on_relay(2)))
        print("READ STATE 2: {}".format(read_relay_status(2)))
        sleep(duration)

        # Turn off the second relay
        print("TURN OFF 2: {} ".format(off_relay(2)))
        print("READ STATE 2: {}".format(read_relay_status(2)))


   
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
    finally:
        sys.exit()