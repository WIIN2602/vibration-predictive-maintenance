# 🛠️ Vibration Predictive Maintenance System (ISO 10816-3)

ระบบวิเคราะห์และพยากรณ์ความเสียหายของเครื่องจักรหมุน (Rotating Machinery) โดยอ้างอิงตามมาตรฐาน **ISO 10816-3**. โปรแกรมนี้สามารถอ่านข้อมูลความสั่นสะเทือน, คำนวณค่า RMS, จำแนกสถานะความปลอดภัย และพยากรณ์วันที่คาดว่าเครื่องจักรจะชำรุดล่วงหน้าด้วย Machine Learning (Linear Regression)

---

## 📋 คุณสมบัติของระบบ (Key Features)

* **🔍 Data Processing**: ดึงข้อมูลจากไฟล์ `.txt` และแปลงค่า Amplitude เป็นค่า RMS อัตโนมัติโดยใช้ Regex และ NumPy
* **⚠️ ISO Analysis**: จำแนกสถานะสุขภาพเครื่องจักรเป็น 4 โซน (Green, Yellow, Orange, Red) ตามเกณฑ์มาตรฐานสากล
* **📈 Predictive Modeling**: ใช้ **Linear Regression** วิเคราะห์แนวโน้ม (Trend Analysis) เพื่อหา Remaining Useful Life (RUL)
* **📊 Visualization**: สร้างกราฟเส้นแนวโน้ม (Trend Line) และจุดวิกฤต (Threshold) บันทึกเป็นไฟล์ `.png` อัตโนมัติ
* **🖥️ Terminal UI**: แสดงผลรายงานสรุปในรูปแบบตาราง (Grid Table) ที่อ่านง่ายเหมือนการใช้คำสั่ง SQL
* **⚙️ Configurable**: รองรับการปรับเปลี่ยน Path ข้อมูลและค่า Threshold ผ่านไฟล์ `.env` โดยไม่ต้องแก้ไขโค้ด

---

## 📊 ตัวอย่างผลลัพธ์ (Example Output)

### 1. รายงานบน Terminal (Executive Summary)
แสดงตารางสรุปค่า RMS ล่าสุด, สถานะตามโซนสี, แนวโน้ม และวันที่คาดว่าจะเกิดความเสียหาย


### 2. กราฟวิเคราะห์แนวโน้ม (Trend Analysis Plot)
กราฟแสดงจุดข้อมูลจริง (Actual Data) เทียบกับเส้นพยากรณ์ (Trend Line) และเส้นระดับอันตราย (Danger Threshold)


---

## 🚀 การเริ่มต้นใช้งาน (Getting Started)

### 1. การเตรียมระบบ (Prerequisites)
* **Python 3.8+**
* ติดตั้ง Library ที่จำเป็น:
    ```bash
    pip install -r requirements.txt
    ```
    *(Library หลัก: `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `tabulate`, `python-dotenv`)*

### 2. การตั้งค่า Environment (.env)
คัดลอกไฟล์ `.env.example` ที่ Root Directory ของโปรเจกต์แล้ววางที่เดิม จากนั้นลบ `.example` ในชื่อออกและกำหนดค่าดังนี้:
```env
DATA_PATH=./data
EXPORT_PATH=./output
THRESHOLD_RED=7.1
```

### 3. การรันโปรแกรม
วางไฟล์ข้อมูล `.txt` ที่ดึงมาจากเซนเซอร์ไว้ในโฟลเดอร์ `data/` จากนั้นรันคำสั่ง:
```bash
python main.py
```

---

## 📁 โครงสร้างโปรเจกต์ (Project Structure)

```text
vibration-predictive-maintenance/
├── data/               # โฟลเดอร์เก็บไฟล์ข้อมูลดิบ (.txt)
├── output/             # โฟลเดอร์เก็บรายงาน (.csv) และกราฟ (.png)
├── src/                # Source code แยกตามโมดูล
│   ├── processor.py    # ส่วนประมวลผลข้อมูลและคำนวณ RMS
│   ├── analyzer.py     # ส่วนวิเคราะห์สถานะตามมาตรฐาน ISO
│   └── predictor.py    # ส่วนพยากรณ์และสร้าง Visualization
├── .env                # ไฟล์กำหนดค่าตัวแปรระบบ
├── main.py             # จุดเริ่มต้นการรันโปรแกรม (Entry Point)
└── requirements.txt    # รายการ Library สำหรับติดตั้ง
```

---

## 🔧 การดูแลรักษา (Maintenance & Future Updates)

1.  **การปรับปรุงโมเดล**: หากข้อมูลมีลักษณะความชันไม่คงที่ (Non-linear) สามารถพิจารณาเปลี่ยนจาก `LinearRegression` เป็น `PolynomialFeatures` ใน `src/predictor.py`
2.  **การเพิ่มเครื่องจักร**: ระบบรองรับการเพิ่มข้อมูลเครื่องจักรใหม่โดยอัตโนมัติ เพียงเพิ่มไฟล์ `.txt` ลงในโฟลเดอร์ `data` ระบบจะทำการวนลูปประมวลผลให้เอง
3.  **การอัปเดตเกณฑ์**: สามารถปรับค่า `THRESHOLD` ในไฟล์ `.env` ได้ทันทีเมื่อมีการเปลี่ยนกลุ่มเครื่องจักรตามมาตรฐาน ISO 10816-3 (Machine Group 1-4)
4.  **การแสดงผล**: หากตารางใน Terminal แสดงผลไม่พอดีหน้าจอ สามารถขยายหน้าต่าง Terminal หรือปรับปรุงการตัดคำใน `main.py` ส่วนการเรียกใช้งาน `tabulate`