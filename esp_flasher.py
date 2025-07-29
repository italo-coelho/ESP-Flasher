import os
import sys
import time
import base64
from PIL import Image
import FreeSimpleGUI as GUI

from flashing_tools import *

firmware = None
bootloader = None
partitions = None

def find_file(filename, search_path):
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

app_path = os.path.dirname(__file__)
path = os.path.join(os.path.dirname(__file__), './icon.png')
GUI.set_options (
                    font=("Courier Bold",16),
                    icon = base64.b64encode(open(path, 'rb').read()),
                    background_color = "light gray",
                    element_background_color = "light gray",
                    input_elements_background_color= "green",
                    text_element_background_color= "light gray",
                    text_color = "dark green"
                )

path = os.path.join(os.path.dirname(__file__), './logo.png')
image = Image.open(path)
image.thumbnail((600,600))
image.save(path)

layout =    [
                [GUI.Column([[GUI.Image(path)]], justification='center')],
                [GUI.Column([[GUI.FolderBrowse(button_text="PIO Project", initial_folder=app_path, button_color="dark green", key="-FOLDER-", enable_events=True)]]), GUI.Text("           ", key="-FOLDER_NAME-")],
                [GUI.Column([[GUI.Text("Firmware:")], [GUI.Text("Bootloader:")], [GUI.Text("Partitions:")]]), GUI.Column([[GUI.Text("-", key="-FIRMWARE-")], [GUI.Text("-", key="-BOOTLOADER-")], [GUI.Text("-", key="-PARTITIONS-")]])],
                [GUI.Text("", font=("Courier Bold",3))],
                [GUI.Column([[GUI.Button("Upload", key="-UPLOAD-", button_color="dark green", disabled=True)]]), GUI.Column([[GUI.Text("", key="-UPLOAD_TEXT-")]])],
                [GUI.Column([[GUI.Multiline(size=(35, 4), autoscroll=True, no_scrollbar=True, background_color="gray", text_color="white", disabled=True, key="-CONSOLE-")]])],
                # [GUI.Column([[GUI.Button("Stop", key="-STOP-", button_color="dark green", disabled=True)]])],
            ]

window = GUI.Window("ESP Flasher", layout, finalize=True)

def console_log(text):
    window["-CONSOLE-"].update(text)
    event, values = window.read(timeout=1)

    if event in (GUI.WIN_CLOSED, 'Exit'):
        sys.exit(0)

while True:
    event, values = window.read(timeout=1000)

    if event in (GUI.WIN_CLOSED, 'Exit'):
        break
    
    if(event == "-FOLDER-"):
        folder = values["-FOLDER-"]
        folder_name = os.path.basename(os.path.normpath(folder))
        window["-FOLDER_NAME-"].update(folder_name)

        firmware = find_file("firmware.bin", folder)
        bootloader = find_file("bootloader.bin", folder)
        partitions = find_file("partitions.bin", folder)

        if(firmware): window["-FIRMWARE-"].update("Ok!")
        else: window["-FIRMWARE-"].update("Not Found!")
        if(bootloader): window["-BOOTLOADER-"].update("Ok!")
        else: window["-BOOTLOADER-"].update("Not Found!")
        if(partitions): window["-PARTITIONS-"].update("Ok!")
        else: window["-PARTITIONS-"].update("Not Found!")

        if(firmware and bootloader and partitions):
            window["-UPLOAD-"].update(disabled = False)
        else:
            window["-UPLOAD-"].update(disabled = True)

    if(event == "-UPLOAD-"):
        pPorts = set()

        # window["-UPLOAD-"].update(disabled=True)
        window["-FOLDER-"].update(disabled=True)
        # window["-STOP-"].update(disabled=False)

        window["-UPLOAD_TEXT-"].update("Connect ESP...")

        while True:
            event, values = window.read(timeout=1)

            if event in (GUI.WIN_CLOSED, 'Exit'):
                sys.exit(0)
        
            if(event == "-STOP-"):
                break
            if(event == "-UPLOAD-"):
                break

            if(firmware and bootloader and partitions):
                ports = set(list_serial_ports())
                
                new_ports = ports - pPorts
                if(new_ports):
                    window["-UPLOAD_TEXT-"].update("Uploading...")
                    for p in new_ports:
                        flash_firmware(p, firmware, bootloader, partitions, callback=console_log)
                        time.sleep(1)
                    window["-UPLOAD_TEXT-"].update("Connect ESP...")
                
                pPorts = ports

        # window["-STOP-"].update(disabled=True)
        window["-FOLDER-"].update(disabled=False)
        # window["-UPLOAD-"].update(disabled=False)

        window["-UPLOAD_TEXT-"].update("")
        window["-CONSOLE-"].update("")


window.close()

print()
print("------------")
print("Ítalo Coelho")
print("2025")
print()