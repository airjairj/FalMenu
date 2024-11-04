from time import time
from ReadWriteMemory import ReadWriteMemory
import threading
import json

rwm = ReadWriteMemory()

def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)

def save_config(config, filename):
    if not filename.endswith('.json'):
        filename += '.json'
    with open(filename, 'w') as file:
        json.dump(config, file)

def freeze_variable(pointer, value):
    def freeze():
        while not stop_event.is_set():
            process.write(pointer, value)
            time.sleep(0.01)
    
    stop_event = threading.Event()
    freeze_thread = threading.Thread(target=freeze)
    freeze_thread.start()
    return stop_event

# Add this to stop the thread when the program ends
stop_event = None
config = {}
loop_control = False

try:
    while not loop_control:
        print("Choose an option:")
        print("1. Manually set the config, and save it to a file")
        print("2. Load the config from a file")
        print("3. Advance to the next step")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            config["process_name"] = input("Enter the process name: ")
            config["base_address"] = int(input("Enter the base address: "), 16)
            config["base_offset"] = int(input("Enter the base offset: "), 16)
            config["offsets"] = [int(offset, 16) for offset in input("Enter the offsets (with 0x) separated by a space: ").split()]
            filename = input("Enter the filename to save the config to: ")
            save_config(config, filename)
            print("Config saved.")
        elif choice == '2':
            config = load_config()
            print("Config loaded.")
        elif choice == '3':
            print("Advancing...\n")

            # Open process
            process_name = config['process_name']
            process = rwm.get_process_by_name(process_name)
            process.open()

            # Base Address
            # process name + offest
            preferreImageBase = config['base_address']
            baseOffset = config['base_offset']
            base_address = preferreImageBase + baseOffset

            # Pointer
            # base address + array of offsets
            varpointer = process.get_pointer(base_address, offsets=config['offsets'])

            loop_control = True
        elif choice == '4':
            print("Exiting...\n")
            break
        else:
            print("Invalid choice. Please try again.")

    while loop_control == True:
        print("Choose an option:")
        print("1. Write a value")
        print("2. Read a value")
        print("3. Freeze a value")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1' or choice == 'w' or choice == 'W' or choice == 'write' or choice == 'Write':
            # Write the value
            value = int(input("Enter the value to write: "))
            process.write(varpointer, value)
        elif choice == '2' or choice == 'r' or choice == 'R' or choice == 'read' or choice == 'Read':
            # Read the value
            value = process.read(varpointer)
            print(f"Value: {value}")
        elif choice == '3' or choice == 'f' or choice == 'F' or choice == 'freeze' or choice == 'Freeze':
            # Freeze the value
            value = int(input("Enter the value to freeze: "))
            if stop_event:
                stop_event.set()
            stop_event = freeze_variable(varpointer, value)
        elif choice == '4' or choice == 'e' or choice == 'E' or choice == 'exit' or choice == 'Exit':
            print("Exiting...")
            if stop_event:
                stop_event.set()
            break
        else:
            print("Invalid choice. Please try again.")
except KeyboardInterrupt:
    print("\nExiting...")
    if stop_event:
        print("\nStopping the thread/s...")
        stop_event.set()