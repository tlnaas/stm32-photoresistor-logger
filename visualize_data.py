import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
import argparse

def load_data(filename):
    """Load data from CSV file"""
    df = pd.read_csv(filename)
    
    # Convert timestamp columns to datetime if needed
    if 'pc_timestamp' in df.columns:
        df['pc_datetime'] = pd.to_datetime(df['pc_timestamp'])
    
    # Convert STM32 timestamp to seconds (assuming it's in milliseconds)
    if 'timestamp' in df.columns:
        df['time_seconds'] = df['timestamp'] / 1000.0
    
    return df

def plot_data(df, live_update=False):
    """Plot the sensor data"""
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(12, 6))
    
    if live_update:
        # For live updating plot
        def update(frame):
            ax.clear()
            df = load_data(filename)
            if not df.empty:
                ax.plot(df['time_seconds'], df['value'], 'b-', label='Photoresistor Value')
                ax.set_xlabel('Time (seconds)')
                ax.set_ylabel('Sensor Value')
                ax.set_title('Photoresistor Readings Over Time')
                ax.legend()
                ax.grid(True)
        
        ani = FuncAnimation(fig, update, interval=1000)
        plt.show()
    else:
        # Static plot
        if not df.empty:
            ax.plot(df['time_seconds'], df['value'], 'b-', label='Photoresistor Value')
            ax.set_xlabel('Time (seconds)')
            ax.set_ylabel('Sensor Value')
            ax.set_title('Photoresistor Readings Over Time')
            ax.legend()
            ax.grid(True)
            plt.tight_layout()
            plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='STM32 Sensor Data Visualizer')
    parser.add_argument('filename', default='sensor_data.csv', nargs='?', help='CSV file to visualize')
    parser.add_argument('--live', action='store_true', help='Enable live updating plot')
    
    args = parser.parse_args()
    filename = args.filename
    
    try:
        df = load_data(filename)
        print(f"Loaded {len(df)} records from {filename}")
        print(df.head())
        
        plot_data(df, args.live)
        
    except Exception as e:
        print(f"Error: {e}")