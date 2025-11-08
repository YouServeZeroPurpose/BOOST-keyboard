import asyncio
from bleak import BleakScanner, BleakClient
from pynput.keyboard import Controller, Key

keyboard = Controller()

async def main():
    print("scanning...")
    devices = await BleakScanner.discover()
    hub = None
    for d in devices:
        if "Pybricks Hub" in (d.name or ""):
            hub = d
            break

    if hub is None:
        print("no Pybricks Hub found.")
        return

    print(f"found hub: {hub.name} ({hub.address})")

    async with BleakClient(hub.address) as client:
        print("connected!")
        await client.get_services()

        console_char = None
        for service in client.services:
            for char in service.characteristics:
                if "notify" in char.properties:
                    console_char = char
                    break
            if console_char:
                break

        if console_char is None:
            print("no notify-capable characteristic found")
            return

        print(f"using characteristic {console_char.uuid} for console output")

        buffer = []

        def handle_data(_, data: bytearray):
            nonlocal buffer
            text = data.decode(errors='ignore')
            for char in text:
                if char == "@":
                    continue
                elif char == "#":
                    line = (''.join(buffer)).strip()
                    print(f"received {line}!")
                    keyboard.type(line)
                    keyboard.press(Key.enter)
                    buffer.clear()
                else:
                    buffer.append(char)

        await client.start_notify(console_char.uuid, handle_data)
        while True:
            await asyncio.sleep(1)

asyncio.run(main())