```markdown
# 🛠️ Vibration Predictive Maintenance System (ISO 10816-3)

ระบบวิเคราะห์และพยากรณ์ความเสียหายของเครื่องจักรหมุน (Rotating Machinery) โดยอ้างอิงตามมาตรฐาน **ISO 10816-3**. โปรแกรมนี้สามารถอ่านข้อมูลความสั่นสะเทือน, คำนวณค่า RMS, จำแนกสถานะความปลอดภัย และพยากรณ์วันที่คาดว่าเครื่องจักรจะชำรุดล่วงหน้าด้วย Machine Learning (Linear Regression).

---

## 📋 คุณสมบัติของระบบ (Key Features)

* **🔍 Data Processing**: ดึงข้อมูลจากไฟล์ `.txt` และแปลงค่า Amplitude เป็นค่า RMS อัตโนมัติโดยใช้ Regex และ NumPy
* **⚠️ ISO Analysis**: จำแนกสถานะสุขภาพเครื่องจักรเป็น 4 โซน (Green, Yellow, Orange, Red) ตามเกณฑ์มาตรฐานสากล
* **📈 Predictive Modeling**: ใช้ **Linear Regression** วิเคราะห์แนวโน้ม (Trend Analysis) เพื่อหา Remaining Useful Life (RUL)
* **📊 Visualization**: สร้างกราฟเส้นแนวโน้ม (Trend Line) และจุดวิกฤต (Threshold) บันทึกเป็นไฟล์ `.png` อัตโนมัติ
* **🖥️ Terminal UI**: แสดงผลรายงานสรุปในรูปแบบตาราง (Grid Table) ที่อ่านง่ายเหมือน SQL
* **⚙️ Configurable**: รองรับการปรับเปลี่ยน Path และค่า Threshold ผ่านไฟล์ `.env` โดยไม่ต้องแก้โค้ด

---

## 📊 ตัวอย่างผลลัพธ์ (Example Output)

### 1. รายงานบน Terminal (Executive Summary)
!
*(ระบบจะแสดงสถานะล่าสุด พร้อมวันที่คาดการณ์ว่าจะเกิดความเสียหาย)*

### 2. กราฟวิเคราะห์แนวโน้ม (Trend Analysis Plot)
!
*(กราฟแสดงจุดข้อมูลจริง เส้นแนวโน้ม และเส้นขีดจำกัดอันตรายตาม ISO)*

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
สร้างไฟล์ `.env` ที่ Root Directory และกำหนดค่าดังนี้:
```env
DATA_PATH=./data
EXPORT_PATH=./output
THRESHOLD_RED=7.1
```

### 3. การรันโปรแกรม
วางไฟล์ข้อมูล `.txt` ไว้ในโฟลเดอร์ `data/` จากนั้นรัน:
```bash
python main.py
```

---

## 📁 โครงสร้างโปรเจกต์ (Project Structure)

```text
vibration-predictive-maintenance/
├── data/               # ข้อมูลความสั่นสะเทือนดิบ (.txt)
├── output/             # รายงานสรุป (.csv) และกราฟแนวโน้ม (.png)
├── src/                # Source code แยกตามหน้าที่
│   ├── processor.py    # Parser ดึงข้อมูลและคำนวณ RMS
│   ├── analyzer.py     # Classify สถานะตาม ISO 10816-3
│   └── predictor.py    # ML Model และระบบสร้าง Visualization
├── .env                # ไฟล์ตั้งค่าระบบ
├── main.py             # Entry point สำหรับรันระบบทั้งหมด
└── requirements.txt    # รายการ Library ที่ต้องใช้
```

---

## 🔧 การดูแลรักษา (Maintenance & Future Updates)

1.  **การปรับปรุงโมเดล**: หากข้อมูลมีลักษณะไม่เป็นเส้นตรง (Non-linear) สามารถเปลี่ยนจาก `LinearRegression` เป็น `PolynomialFeatures` ใน `src/predictor.py`
2.  **การเพิ่มเครื่องจักร**: เพียงเพิ่มไฟล์ `.txt` ลงในโฟลเดอร์ `data` ระบบจะทำการวนลูปประมวลผลและสร้างกราฟให้เครื่องใหม่โดยอัตโนมัติ
3.  **การอัปเดตเกณฑ์**: สามารถปรับค่า `THRESHOLD_YELLOW/ORANGE/RED` ใน `.env` ได้ทันทีเมื่อมีการเปลี่ยนกลุ่มเครื่องจักร (Machine Group 1-4)
```