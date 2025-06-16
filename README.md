# Monitoring & Control GUI Robot Wireless

This project is an assignment from the RE-202 Object-Oriented Programming (OOP) course which aims to build a wireless robot monitoring and control system via Python GUI (Tkinter) connected to ESP32 via WiFi network.

## Features

Hardware:

- ESP32 Dev Board.

- DC Motor (2).

- Motor Driver (L298N).

- Line Sensor BFD 5 Channel.

- Micro Servo Mg90-s.

- Power Supply.

Software:

- Python 3.x + Tkinter + socket + threading.

- Arduino IDE + ESP32 WiFiManager Library.

- ESP32 as TCP/IP server.

## Works

- ESP32 opens AP mode + configuration portal (WiFiManager)

- ESP32 receives commands from GUI (eg: M:120,130) to set motor speed, and also to set degree angle on servo.

- ESP32 reads line sensor, then sends its status to GUI.

- Python GUI displays motor slider, direction button, and line sensor visualization.

## GUI

![](asset/gui.png)

## Team

- Ichsan Fajar Yudika (4222401042)
- Wildan Mahfudh Khoirul Murtadho (4222401046)
- M. Rasyid Prasetyo (4222411048)
- Moh. Abdul Hikmal (4222401032)
