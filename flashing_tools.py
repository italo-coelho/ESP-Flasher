import os
import serial.tools.list_ports
import subprocess

def log(message, callback=None):
    if callback:
        callback(message)
    else:
        print(message)

def list_serial_ports():
    ports = []
    for port in serial.tools.list_ports.comports():
        desc = (port.description or "").lower()
        name = (port.device or "").lower()
        if("usb" in name):
            ports.append(port.device)
    return sorted(ports)

def detect_chip_type(port, callback=None):
    try:
        result = subprocess.run(
            ["esptool.py", "--port", port, "chip_id"],
            capture_output=True, text=True, timeout=10
        )
        output = result.stdout.lower()
        if "esp32-s3" in output:
            return "esp32s3"
        elif "esp32-s2" in output:
            return "esp32s2"
        elif "esp32-c3" in output:
            return "esp32c3"
        elif "esp8266" in output:
            return "esp8266"
        elif "esp32" in output:
            return "esp32"
        else:
            log(f"Could not detect chip type on {port}", callback)
            return None
    except subprocess.TimeoutExpired:
        log(f"Timeout while detecting chip on {port}", callback)
    except Exception as e:
        log(f"Error detecting chip on {port}: {e}", callback)
    return None

def flash_firmware(port, firmware, bootloader, partitions, callback=None):
    log(f"\nConnecting to {port}...", callback)

    chip_type = detect_chip_type(port, callback)
    if not chip_type:
        log(f"Skipping {port} due to unknown chip type.\n", callback)
        return False

    log(f"Detected chip: {chip_type.upper()}", callback)

    command = [
        "esptool.py",
        "--chip", chip_type,
        "--port", port,
        "--baud", "460800",
        "--before", "default_reset",
        "--after", "hard_reset",
        "write_flash", "-z"
    ]

    command.extend(["0x1000", bootloader])
    command.extend(["0x8000", partitions])
    command.extend(["0x10000", firmware])

    try:
        # subprocess.run(command, check=True)
        process = subprocess.Popen(
                                    command,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT,
                                    text=True,
                                    bufsize=1
                                  )
        for line in process.stdout:
            log(line, callback=callback)
        return_code = process.wait()
        if return_code == 0:
            log(f"Firmware uploaded successfully to {port}\n", callback=callback)
            return True
        else:
            log(f"Upload failed on {port} with code {return_code}\n", callback=callback)
            return False
    except subprocess.CalledProcessError:
        log(f"Upload failed on {port}\n", callback)
        return False