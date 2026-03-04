import os
from dotenv import load_dotenv

load_dotenv()

class ISOAnalyzer:
    def __init__(self, group=1):
        # โหลดค่า Threshold จาก .env (ถ้าไม่มีให้ใช้ค่า Default ตาม Group 1 & 3)
        self.yellow = float(os.getenv("THRESHOLD_YELLOW", 2.3))
        self.orange = float(os.getenv("THRESHOLD_ORANGE", 4.5))
        self.red = float(os.getenv("THRESHOLD_RED", 7.1))
        
    def classify_status(self, rms_value):
        """
        จัดกลุ่มสถานะตามค่า RMS และเกณฑ์ ISO 10816-3
        """
        if rms_value <= self.yellow:
            return "Zone A (Green) - Newly commissioned"
        elif rms_value <= self.orange:
            return "Zone B (Yellow) - Unrestricted operation"
        elif rms_value <= self.red:
            return "Zone C (Orange) - Restricted operation"
        else:
            return "Zone D (Red) - DAMAGE OCCURS"

    def analyze_dataframe(self, df):
        """
        เพิ่มคอลัมน์สถานะลงใน DataFrame
        """
        df['ISO_Status'] = df['RMS_Value'].apply(self.classify_status)
        return df

# ตัวอย่างการใช้งาน
if __name__ == "__main__":
    # จำลองข้อมูลที่ได้จาก processor.py ของคุณ
    import pandas as pd
    data = {'Equipment': ['Motor Compressor'], 'RMS_Value': [15.55]}
    test_df = pd.DataFrame(data)
    
    analyzer = ISOAnalyzer()
    result = analyzer.analyze_dataframe(test_df)
    print(result)