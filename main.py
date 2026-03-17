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

    print("\n" + "="*60)
    print("   VIBRATION PREDICTIVE MAINTENANCE SYSTEM (ISO 10816-3)")
    print(f"   Working Directory: {data_path}")
    print("="*60)

    # 1. Process Data
    df = process_all_data(data_path)
    if df.empty:
        print("[Error] No data found in the specified directory.")
        return

    # 2. Analyze
    analyzer = ISOAnalyzer()
    df = analyzer.analyze_dataframe(df)
    
    # 3. Predict & Generate Report
    predictor = VibrationPredictor()
    report = []
    unique_equipment = sorted(df['Equipment'].unique())

    # สร้างรายชื่อเครื่องจักรพร้อมรันเลข ID
    eq_list_for_menu = []
    for idx, name in enumerate(unique_equipment, 1):
        eq_list_for_menu.append({"ID": idx, "Equipment Name": name})

    # ประมวลผลข้อมูลทั้งหมดเก็บไว้ใน List
    for equipment in unique_equipment:
        eq_data = df[df['Equipment'] == equipment]
        latest_status = eq_data.iloc[-1]['ISO_Status']
        latest_rms = eq_data.iloc[-1]['RMS_Value']
        trend, fail_date = predictor.predict_rul(eq_data, save_graph_path=export_path)
        
        report.append({
            'Equipment': equipment,
            'Latest_RMS': float(f"{latest_rms:.2f}"),
            'Current_Status': latest_status,
            'Trend': trend,
            'Est_Failure_Date': fail_date if fail_date else "N/A"
        })

    report_df = pd.DataFrame(report)

    # --- ส่วน Interactive Menu สำหรับเลือกเครื่องจักร ---
    print("\n[ Available Equipment List ]")
    print(tabulate(eq_list_for_menu, headers='keys', tablefmt='simple', showindex=False))
    print("-" * 30)
    
    user_input = input("Enter Equipment ID to filter (or press Enter to show ALL): ").strip()

    # ตรรกะการกรองข้อมูล
    if user_input.isdigit():
        choice = int(user_input)
        if 1 <= choice <= len(unique_equipment):
            selected_name = unique_equipment[choice - 1]
            display_df = report_df[report_df['Equipment'] == selected_name]
            print(f"\n[INFO] Filtering for: {selected_name}")
        else:
            print(f"\n[!] Invalid ID. Showing all equipment instead.")
            display_df = report_df
    else:
        display_df = report_df

    # 4. แสดงผลตารางสรุป
    print("\n" + "="*95)
    print("             EXECUTIVE SUMMARY REPORT (ISO 10816-3 Analysis)")
    print("="*95)
    print(tabulate(display_df, headers='keys', tablefmt='grid', showindex=False))
    
    # บันทึกไฟล์ CSV (บันทึกข้อมูลทั้งหมดเสมอเพื่อการใช้งานภาพรวม)
    file_name = "maintenance_report.csv"
    save_path = os.path.join(export_path, file_name)
    report_df.to_csv(save_path, index=False)
    
    print(f"\n[SUCCESS] Full report saved to: {save_path}")
    print("="*95)

if __name__ == "__main__":
    run_maintenance_system()