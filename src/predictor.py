import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import datetime
import matplotlib.pyplot as plt
import os

class VibrationPredictor:
    def __init__(self, threshold_red=7.1):
        """
        Initialize Predictor ด้วยค่า Threshold (Red Zone) จาก ISO 10816-3
        """
        self.threshold_red = threshold_red
        self.model = LinearRegression()

    def predict_rul(self, df_equipment, save_graph_path=None):
        """
        พยากรณ์วันที่ค่าความสั่นจะถึงเกณฑ์อันตราย และสร้างกราฟแนวโน้ม
        """
        # ตรวจสอบว่ามีข้อมูลเพียงพอสำหรับการลากเส้นพยากรณ์หรือไม่ (ต้องมีอย่างน้อย 2 จุด)
        if len(df_equipment) < 2:
            return "Need more data", None

        # เตรียมข้อมูล: เรียงลำดับตามเวลา
        df = df_equipment.copy().sort_values('Timestamp')
        equipment_name = df['Equipment'].iloc[0]
        
        # แปลง Timestamp เป็นตัวเลข (Ordinal) เพื่อใช้เป็นแกน X ใน Linear Regression
        X = df['Timestamp'].map(datetime.datetime.toordinal).values.reshape(-1, 1)
        y = df['RMS_Value'].values

        # ฝึกสอน Model (Training)
        self.model.fit(X, y)
        slope = self.model.coef_[0]
        intercept = self.model.intercept_

        # คำนวณวันที่พยากรณ์ (Predicted Date)
        predicted_date = None
        if slope > 0:
            # สูตร: y = mx + c  => x = (y - c) / m
            target_ordinal = (self.threshold_red - intercept) / slope
            # ตรวจสอบว่าค่าที่ได้ไม่เกินขีดจำกัดของระบบวันที่ Python (max ordinal)
            try:
                predicted_date = datetime.date.fromordinal(int(target_ordinal))
            except (ValueError, OverflowError):
                predicted_date = None

        # --- ส่วนการสร้างกราฟ (Visualization) ---
        if save_graph_path:
            plt.figure(figsize=(10, 6))
            
            # 1. พล็อตจุดข้อมูลจริง (Actual Data)
            plt.scatter(df['Timestamp'], y, color='blue', label='Actual RMS Data', zorder=5)
            
            # 2. สร้างเส้นแนวโน้ม (Trend Line)
            # กำหนดจุดสิ้นสุดของเส้นกราฟ (ถ้าพยากรณ์ได้ให้ลากไปถึงวันนั้น ถ้าไม่ได้ให้ลากไปอีก 30 วัน)
            if predicted_date:
                end_date = max(predicted_date, df['Timestamp'].max().date() + datetime.timedelta(days=30))
            else:
                end_date = df['Timestamp'].max().date() + datetime.timedelta(days=30)
            
            X_range = np.array([X.min(), datetime.datetime.toordinal(end_date)]).reshape(-1, 1)
            y_trend = self.model.predict(X_range)
            
            # ดึงค่าออกมาเป็น scalar โดยใช้ [0][0] และ [1][0]
            start_date = datetime.datetime.fromordinal(int(X_range[0][0]))
            end_date_plot = datetime.datetime.fromordinal(int(X_range[1][0]))
            
            plt.plot([start_date, end_date_plot], 
                     y_trend, '--', color='orange', label='Trend Line (Prediction)')

            # 3. ขีดเส้นระดับอันตรายสีแดง (ISO Threshold)
            plt.axhline(y=self.threshold_red, color='red', linestyle='-', linewidth=2, 
                        label=f'Danger Threshold ({self.threshold_red} mm/s)')
            
            # ตกแต่งกราฟ
            plt.title(f"Vibration Trend Analysis: {equipment_name}", fontsize=14)
            plt.xlabel("Date", fontsize=12)
            plt.ylabel("RMS Value (mm/s)", fontsize=12)
            plt.legend()
            plt.grid(True, linestyle=':', alpha=0.6)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # ตรวจสอบและสร้างโฟลเดอร์สำหรับเซฟรูป
            if not os.path.exists(save_graph_path):
                os.makedirs(save_graph_path)
                
            # ตั้งชื่อไฟล์รูปตามชื่อเครื่องจักร
            clean_name = equipment_name.replace("/", "_").replace(" ", "_")
            file_name = f"trend_{clean_name}.png"
            plt.savefig(os.path.join(save_graph_path, file_name))
            plt.close() # ปิดรูปเพื่อคืน Memory

        # สรุปผลสถานะแนวโน้ม
        status = "Degrading" if slope > 0 else "Stable or Improving"
        return status, predicted_date

# สำหรับการทดสอบ Unit Test เฉพาะไฟล์นี้
if __name__ == "__main__":
    # จำลองข้อมูล
    test_data = {
        'Equipment': ['Test Motor'] * 3,
        'Timestamp': pd.to_datetime(['2024-06-01', '2024-08-01', '2024-10-01']),
        'RMS_Value': [1.2, 2.5, 4.0]
    }
    df_test = pd.DataFrame(test_data)
    
    predictor = VibrationPredictor(threshold_red=7.1)
    status, fail_date = predictor.predict_rul(df_test, save_graph_path="./output_test")
    
    print(f"Analysis Results:")
    print(f"Trend: {status}")
    print(f"Est. Failure Date: {fail_date}")