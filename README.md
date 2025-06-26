# STM32 Photoresistor Logging and Visualization System

## Requirements
### Hardware
- **Board**: Nucleo-G474RE  
- **MCU**: STM32G474RE  
- **Additional Components**:
  - USB to UART Converter
  - Jumper Wires
  - Photoresistor (with built-in 10k ohm resistor)

### Software
- **IDEs**: STM32CubeIDE, VS Code  
- **Languages**: C/C++, Python  
- **Python Libraries**:
  ```bash
  pyserial matplotlib pandas

### Practical Use Cases

- Monitor sunlight intensity to automate shade systems or supplemental lighting
- Ensure consistent illumination for camera inspection systems
- Trigger window coverings based on real-time light measurements

## Project Description

### This system:

- Reads photoresistor values (0-4095 range)
- 0 = no light
- 4095 = maximum light intensity
- Saves values to CSV file
- Provides visual data representation

## Physical Connections:
- Connect the Nucleo board to your PC using the ST link cable
- Connect PC10 on the board to the TX pin , connect PC11 on the board to the RX pin , connect GND on the board to the GND pin (TX , RX and GND pins can all be found on the USB to UART converter and can be connected using jumper cables)
- After using the jumper cables to connect the board and the USB to UART converter plug the convertor into your PC
- Connect 3v3 on the board to the pin found in the middle of the 3 pins, connect GND on the board to the pin lablled (-) , connect PA0 to the pin lablled (S) (pin labbled (-) , pin lablled (S) and the middle pin can all be found on the photoresistor and can be connected to the pins on the board using jumper cables)

![STM32 Photoresistor Setup](STM32_Photoresistor_Setup.jpg)

## How to run this project:
- Using STMcubeIDE open the project , build the project and then run it
- Run serial_listener.py to read the data obtained from the photoresistor and write it to CSV
- Run visualise_data.py to read the data from the CSV file and create a visiual representation

## Code to run the python files (make sure you are in the same directory to run):
```python3 serial_listener.py COM3 ```

This line is to run the serial_listener , make sure to switch COM3 with the actual port name

```python3 visualize_data.py sensor_data.csv```

This line is to run visualize_data.py however it is a static plot

```python visualize_data.py sensor_data.csv --live```

This line is also to run visualize_data.py however it is a live plot

### Helpful Resources:
- https://www.electrothinks.com/2023/07/photoresistor-module.html (photoresistor pinout)
- https://os.mbed.com/platforms/ST-Nucleo-G474RE/ (nucleo board schematic)
