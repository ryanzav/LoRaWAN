# LoRaWAN
This is a LoRaWAN v1.0 implementation in python.

It uses: https://github.com/mayeranalytics/pySX127x

For reference on LoRa see: https://www.lora-alliance.org/portals/0/specs/LoRaWAN%20Specification%201R0.pdf

This fork adds support for the Adafruit LoRA Radio Bonnet with OLED - RFM95W @ 915MHZ.

It also allows you to connect as a client to the Helium Network.

You must create a device on the Helium Console at https://console.helium.com/

You need to rename "keys_example.py" to "keys.py" and enter you device information from the Helium Console.


## Installation
To register a device and get a device ID you need to run otaa_helium.py and stores the results in keys.py.

Then you can run tx_helium.py to send messages by specifying the msg and the frame like this:

    python3 tx_helium.py --msg "Test" --frame 1

If you leave out the arguments, "Test" will be used for the frame. If you initialized with `otaa_helium.py` a file called `.last_frame` will be created and set to `0`. `tx_helium.py` will automatically increment. If the frame count is off simply edit `.last_frame` to the last frame number recieved by Helium, or run `otaa_helium.py` again

You can run rssi_helium.py which utilizes the OLED screen and buttons.

This will sent a tranmission when it starts and whenever you press the middle button.

The transmission is a confirmed data message so a response will be received if a hotspot is in range.

The message just sends with the same frame to prevent having to track that and since the up link data is not needed.

The script pulls the RSSI, the packet RSSI, and the SNR and displays it on the OLED.

[pi]: pi.jpg "pi"

![alt text][pi]

##TODO
Automatically call otaa_helium if `.last_frame` is missing

