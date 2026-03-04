import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import datetime

class VibrationPredictor:
    def __init__(self, threshold_red=7.1):
        self.threshold_red = threshold_red
        self.model = LinearRegression()

    def predict_rul(self, df_equipment):
        """
        พยากรณ์วันที่ค่าความสั่นจะถึงเกณฑ์อันตราย (Remaining Useful Life)
        """
        # เตรียมข้อมูล: แปลง Timestamp เป็นตัวเลข (Ordinal) เพื่อเข้า Model
        df = df_equipment.copy().sort_values('Timestamp')
        X = df['Timestamp'].map(datetime.datetime.toordinal).values.reshape(-1, 1)
        y = df['RMS_Value'].values

        # ฝึกสอน Model ด้วยข้อมูลที่มี (Jun, Sep, Oct)
        self.model.fit(X, y)

        # หาค่าความชัน (Slope) เพื่อดูว่าแนวโน้มเพิ่มขึ้นหรือลดลง
        slope = self.model.coef_[0]

        if slope <= 0:
            return "Stable or Improving", None

        # คำนวณหา Date Ordinal ที่ y จะเท่ากับ threshold_red
        # สูตร: y = mx + c  => x = (y - c) / m
        intercept = self.model.intercept_
        target_ordinal = (self.threshold_red - intercept) / slope
        predicted_date = datetime.date.fromordinal(int(target_ordinal))

        return "Degrading", predicted_date

# ตัวอย่างการทดสอบ
if __name__ == "__main__":
    # จำลองข้อมูลที่ได้จาก processor.py
    data = {
        'Timestamp': pd.to_datetime(['2024-06-28', '2024-09-04', '2024-10-16']),
        'RMS_Value': [0.27, 15.55, 0.25] # ข้อมูลจาก Motor Compressor ของคุณ
    }
    df_test = pd.DataFrame(data)
    
    predictor = VibrationPredictor()
    status, p_date = predictor.predict_rul(df_test)
    print(f"Trend: {status}, Estimated Failure Date: {p_date}")