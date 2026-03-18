import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import datetime
import matplotlib.pyplot as plt
import os

class VibrationPredictor:
    def __init__(self, threshold_red=None):
        """
        Initialize Predictor โดยดึงค่าจาก Environment Variables
        """
        # ดึงค่า Threshold จาก .env ถ้าไม่มีให้ใช้ค่า Default 7.1 (ตาม ISO 10816-3 Group 1)
        if threshold_red is None:
            self.threshold_red = float(os.getenv("THRESHOLD_RED", 7.1))
        else:
            self.threshold_red = threshold_red

        # ดึงค่าจำนวนวันที่ต้องการพยากรณ์ไปข้างหน้าจาก .env (Default: 30 วัน)
        self.days_to_predict = int(os.getenv("DAYS_TO_PREDICT", 30))
        
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

        # ฝึกสอน Model (Training) จากข้อมูลประวัติทั้งหมด
        self.model.fit(X, y)
        slope = self.model.coef_[0]
        intercept = self.model.intercept_

        # คำนวณวันที่พยากรณ์ (Predicted Date)
        predicted_date = None
        if slope > 0:
            # สูตร: y = mx + c  => x = (y - c) / m
            target_ordinal = (self.threshold_red - intercept) / slope
            
            try:
                # ตรวจสอบว่าค่าที่ได้ไม่เกินขีดจำกัดของระบบวันที่ Python
                predicted_date = datetime.date.fromordinal(int(target_ordinal))
            except (ValueError, OverflowError):
                predicted_date = None

        # --- ส่วนการสร้างกราฟ (Visualization) ---
        if save_graph_path:
            plt.figure(figsize=(10, 6))
            
            # 1. พล็อตจุดข้อมูลจริง (Actual Data)
            plt.scatter(df['Timestamp'], y, color='blue', label='Actual RMS Data', zorder=5)
            
            # 2. สร้างเส้นแนวโน้ม (Trend Line)
            # ใช้ค่า DAYS_TO_PREDICT จาก .env มากำหนดระยะเวลาที่ต้องการลากเส้นกราฟ
            forecast_delta = datetime.timedelta(days=self.days_to_predict)
            last_data_date = df['Timestamp'].max().date()
            
            if predicted_date:
                # ถ้าพยากรณ์วันพังได้ ให้ลากเส้นไปถึงวันพัง หรือตามระยะ DAYS_TO_PREDICT อย่างใดอย่างหนึ่งที่ไกลกว่า
                end_date = max(predicted_date, last_data_date + forecast_delta)
            else:
                # ถ้าพยากรณ์ไม่ได้ (กราฟไม่ชันขึ้น) ให้ลากเส้นไปข้างหน้าตามจำนวนวันที่ตั้งค่าไว้ใน .env
                end_date = last_data_date + forecast_delta
            
            # คำนวณจุดบนเส้น Trend
            X_range_ordinals = np.array([X.min(), datetime.datetime.toordinal(end_date)]).reshape(-1, 1)
            y_trend = self.model.predict(X_range_ordinals)
            
            # แปลง Ordinal กลับเป็นวันที่เพื่อพล็อตลงแกน X
            start_date_plot = datetime.datetime.fromordinal(int(X_range_ordinals[0][0]))
            end_date_plot = datetime.datetime.fromordinal(int(X_range_ordinals[1][0]))
            
            plt.plot([start_date_plot, end_date_plot], 
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
            
            # ตรวจสอบและสร้างโฟลเดอร์สำหรับบันทึกรูป
            if not os.path.exists(save_graph_path):
                os.makedirs(save_graph_path)
                
            # ตั้งชื่อไฟล์รูปตามชื่อเครื่องจักร
            clean_name = equipment_name.replace("/", "_").replace(" ", "_")
            file_name = f"trend_{clean_name}.png"
            plt.savefig(os.path.join(save_graph_path, file_name))
            plt.close()

        # สรุปผลสถานะแนวโน้ม
        status = "Degrading" if slope > 0 else "Stable or Improving"
        return status, predicted_date

if __name__ == "__main__":
    # จำลองการใช้งานเบื้องต้น
    from dotenv import load_dotenv
    load_dotenv() # โหลดค่าจาก .env มาทดสอบ
    
    test_data = {
        'Equipment': ['Test Motor'] * 3,
        'Timestamp': pd.to_datetime(['2024-06-01', '2024-08-01', '2024-10-01']),
        'RMS_Value': [1.2, 2.5, 4.0]
    }
    df_test = pd.DataFrame(test_data)
    
    predictor = VibrationPredictor() # จะดึงค่าจาก .env อัตโนมัติ
    status, fail_date = predictor.predict_rul(df_test, save_graph_path="./output_test")
    
    print(f"--- Predictor Unit Test ---")
    print(f"Target Threshold: {predictor.threshold_red}")
    print(f"Forecast Horizon: {predictor.days_to_predict} days")
    print(f"Resulting Trend: {status}")
    print(f"Est. Failure Date: {fail_date}")