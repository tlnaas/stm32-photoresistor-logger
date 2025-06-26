import serial
import csv
from datetime import datetime
import time
import os

def crc8(data):
    """Calculate CRC8 checksum matching your STM32 implementation"""
    crc = 0x00
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ 0x07
            else:
                crc <<= 1
            crc &= 0xFF
    return crc

def parse_packet(packet):
    """Parse a data packet and verify CRC"""
    try:
        # Split packet into data and CRC parts
        if '*' not in packet:
            return None
        
        data_part, crc_part = packet.rsplit('*', 1)
        
        # Remove brackets if present
        if data_part.startswith('[') and data_part.endswith(']'):
            data_part = data_part[1:-1]
        
        # Calculate CRC of data
        data_bytes = data_part.encode('ascii')
        calculated_crc = crc8(data_bytes)
        
        # Get received CRC
        received_crc = int(crc_part.strip(), 16)
        
        # Verify CRC
        if calculated_crc != received_crc:
            print(f"CRC mismatch: calculated {calculated_crc:02X}, received {received_crc:02X}")
            return None
        
        # Split data into fields
        fields = data_part.split(',')
        if len(fields) != 4:
            print(f"Invalid field count: {len(fields)}")
            return None
            
        return {
            'index': int(fields[0]),
            'timestamp': int(fields[1]),
            'sensor_id': fields[2],
            'value': int(fields[3]),
            'pc_timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Error parsing packet: {e}")
        return None

def serial_listener(port, baudrate=115200, output_file='sensor_data.csv'):
    """Listen to serial port and log data to CSV"""
    try:
        # Configure serial port
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"Listening on {port} at {baudrate} baud...")
        
        # Check if file exists to determine if we need to write headers
        file_exists = os.path.exists(output_file)
        
        with open(output_file, 'a', newline='') as csvfile:
            fieldnames = ['index', 'timestamp', 'sensor_id', 'value', 'pc_timestamp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            buffer = ""
            while True:
                # Read data from serial port
                data = ser.read(ser.in_waiting or 1).decode('ascii', errors='ignore')
                
                if data:
                    buffer += data
                    
                    # Check for complete packets (ending with newline)
                    while '\n' in buffer:
                        packet, buffer = buffer.split('\n', 1)
                        packet = packet.strip()
                        
                        if packet:
                            parsed = parse_packet(packet)
                            if parsed:
                                print(f"Received: {parsed}")
                                writer.writerow(parsed)
                                csvfile.flush()  # Ensure data is written immediately
                
                time.sleep(0.01)
                
    except serial.SerialException as e:
        print(f"Serial port error: {e}")
    except KeyboardInterrupt:
        print("\nStopping listener...")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='STM32 Sensor Data Logger')
    parser.add_argument('port', help='Serial port (e.g., COM3 or /dev/ttyUSB0)')
    parser.add_argument('--baud', type=int, default=115200, help='Baud rate (default: 115200)')
    parser.add_argument('--output', default='sensor_data.csv', help='Output CSV file')
    
    args = parser.parse_args()
    
    serial_listener(args.port, args.baud, args.output)