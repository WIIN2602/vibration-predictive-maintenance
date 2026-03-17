import os
import pandas as pd
from dotenv import load_dotenv
from src.processor import process_all_data
from src.analyzer import ISOAnalyzer
from src.predictor import VibrationPredictor
from tabulate import tabulate

# โหลดค่าจากไฟล์ .env
load_dotenv()

def run_maintenance_system():
    # ดึงค่า Path จาก .env
    data_path = os.getenv("DATA_PATH", "./data")
    export_path = os.getenv("EXPORT_PATH", "./output")
    
    # ตรวจสอบว่ามีโฟลเดอร์ output หรือไม่ ถ้าไม่มีให้สร้างใหม่
    if not os.path.exists(export_path):
        os.makedirs(export_path)

    print("="*50)
    print("VIBRATION PREDICTIVE MAINTENANCE SYSTEM")
    print(f"Working Directory: {data_path}")
    print("="*50)

    # 1. Process Data
    df = process_all_data(data_path)
    
    # 2. Analyze
    analyzer = ISOAnalyzer()
    df = analyzer.analyze_dataframe(df)
    
    # 3. Predict
    predictor = VibrationPredictor()
    report = []

    for equipment in df['Equipment'].unique():
        eq_data = df[df['Equipment'] == equipment]
        latest_status = eq_data.iloc[-1]['ISO_Status']
        latest_rms = eq_data.iloc[-1]['RMS_Value']
        trend, fail_date = predictor.predict_rul(eq_data, save_graph_path=export_path)
        
        report.append({
            'Equipment': equipment,
            'Latest_RMS': f"{latest_rms:.2f}",
            'Current_Status': latest_status,
            'Trend': trend,
            'Est_Failure_Date': fail_date if fail_date else "N/A"
        })

    # 4. แสดงผลและส่งออกไฟล์
    report_df = pd.DataFrame(report)
    
    print("\n" + "="*80)
    print("      EXECUTIVE SUMMARY REPORT (ISO 10816-3 Analysis)")
    print("="*80)
    print(tabulate(report_df, headers='keys', tablefmt='grid', showindex=False))
    file_name = "maintenance_report.csv"
    save_path = os.path.join(export_path, file_name)
    report_df.to_csv(save_path, index=False)
    print(f"\n[INFO] Report saved successfully to: {save_path}")
    print("="*80)

if __name__ == "__main__":
    run_maintenance_system()