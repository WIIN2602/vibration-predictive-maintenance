import pandas as pd
import numpy as np
import re
import os
from dotenv import load_dotenv
from tabulate import tabulate

# โหลดค่าจากไฟล์ .env
load_dotenv()

def parse_vibration_file(file_path):
    """
    ดึงข้อมูล Header และค่า Amplitude จากไฟล์ text
    """
    with open(file_path, 'r') as f:
        content = f.read()

    # 1. ดึงข้อมูล Header ด้วย Regex
    equipment = re.search(r"Equipment:\s+(.*)", content).group(1).strip()
    meas_point = re.search(r"Meas. Point:\s+(.*)", content).group(1).strip()
    date_str = re.search(r"Date/Time:\s+(\d{2}-\w{3}-\d{2}\s+\d{2}:\d{2}:\d{2})", content).group(1)
    
    # 2. ดึงเฉพาะส่วนที่เป็นตัวเลข Amplitude
    table_data = []
    lines = content.split('\n')
    for line in lines[8:]: 
        values = re.findall(r"[-+]?\d*\.\d+|\d+", line)
        if len(values) >= 2:
            # เก็บเฉพาะค่า Amplitude (ดัชนีคี่)
            amps = [float(values[i]) for i in range(1, len(values), 2)]
            table_data.extend(amps)

    return {
        'equipment': equipment,
        'timestamp': pd.to_datetime(date_str),
        'amplitudes': np.array(table_data)
    }

def calculate_velocity_rms(amplitudes):
    """
    คำนวณค่า RMS จาก Amplitude
    """
    if len(amplitudes) == 0:
        return 0
    return np.sqrt(np.mean(np.square(amplitudes)))

def process_all_data(data_dir=None):
    """
    วนลูปอ่านทุกไฟล์ในโฟลเดอร์ data เพื่อสรุปผลเป็น DataFrame
    """
    if data_dir is None:
        data_dir = os.getenv("DATA_PATH", "./data")

    summary = []
    
    if not os.path.exists(data_dir):
        print(f"[Error] Data directory not found: {data_dir}")
        return pd.DataFrame()

    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(data_dir, filename)
            raw_data = parse_vibration_file(file_path)
            
            rms_val = calculate_velocity_rms(raw_data['amplitudes'])
            
            summary.append({
                'Equipment': raw_data['equipment'],
                'Timestamp': raw_data['timestamp'],
                'RMS_Value': rms_val,
                'Source_File': filename
            })
    
    return pd.DataFrame(summary).sort_values('Timestamp')

# สำหรับทดสอบรันเฉพาะไฟล์นี้
if __name__ == "__main__":
    df = process_all_data()
    if not df.empty:
        print("\n" + "="*80)
        print("      DATA PROCESSOR TEST RESULT (Extracted from .txt files)")
        print("="*80)
        # ใช้ tabulate แสดงผลเป็นตารางแบบ grid
        print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
        print("="*80)
    else:
        print("No data processed.")