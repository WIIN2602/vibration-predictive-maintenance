# 🛠️ Vibration Predictive Maintenance System (ISO 10816-3)

ระบบวิเคราะห์และพยากรณ์ความเสียหายของเครื่องจักรหมุน (Rotating Machinery) โดยอ้างอิงตามมาตรฐาน **ISO 10816-3**. โปรแกรมนี้สามารถอ่านข้อมูลความสั่นสะเทือน, คำนวณค่า RMS, จำแนกสถานะความปลอดภัย และพยากรณ์วันที่คาดว่าเครื่องจักรจะชำรุดล่วงหน้าด้วย Machine Learning (Linear Regression)

---

## 📋 คุณสมบัติของระบบ (Key Features)

* **🔍 Data Processing**: ดึงข้อมูลจากไฟล์ `.txt` และแปลงค่า Amplitude เป็นค่า RMS อัตโนมัติโดยใช้ Regex และ NumPy
* **⚠️ ISO Analysis**: จำแนกสถานะสุขภาพเครื่องจักรเป็น 4 โซน (Green, Yellow, Orange, Red) ตามเกณฑ์มาตรฐานสากล
* **📈 Predictive Modeling**: ใช้ **Linear Regression** วิเคราะห์แนวโน้ม (Trend Analysis) เพื่อหา Remaining Useful Life (RUL)
* **🎯 Interactive Selection**: ระบบ Menu ID ที่ช่วยให้ผู้ใช้เลือกดูรายงานสรุปรายเครื่องจักรได้ทันที หรือเลือกแสดงผลทั้งหมด (Total View)
* **📊 Visualization**: สร้างกราฟเส้นแนวโน้ม (Trend Line) และจุดวิกฤต (Threshold) บันทึกเป็นไฟล์ `.png` อัตโนมัติ
* **🖥️ Terminal UI**: แสดงผลรายงานสรุปในรูปแบบตาราง (Grid Table) ที่อ่านง่ายและเป็นระเบียบด้วย `tabulate`
* **⚙️ Configurable**: รองรับการปรับเปลี่ยน Path ข้อมูลและค่า Threshold ผ่านไฟล์ `.env` โดยไม่ต้องแก้ไขโค้ด

---

## 📊 ตัวอย่างผลลัพธ์ (Example Output)

### 1. รายงานบน Terminal (Executive Summary)
แสดงตารางสรุปค่า RMS ล่าสุด, สถานะตามโซนสี, แนวโน้ม (Trend) และวันที่คาดว่าจะเกิดความเสียหาย (Est_Failure_Date) โดยมีการกรองข้อมูลตาม ID ที่ผู้ใช้เลือก

### 2. กราฟวิเคราะห์แนวโน้ม (Trend Analysis Plot)
กราฟแสดงจุดข้อมูลจริง (Actual Data) เทียบกับเส้นพยากรณ์ (Trend Line) และเส้นระดับอันตราย (Danger Threshold) เพื่อการวางแผนซ่อมบำรุงล่วงหน้า

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
THRESHOLD_YELLOW=2.3
THRESHOLD_ORANGE=4.5
THRESHOLD_RED=7.1
```

### 3. การรันโปรแกรม
วางไฟล์ข้อมูล `.txt` ไว้ในโฟลเดอร์ `data/` จากนั้นรันคำสั่ง:
```bash
python main.py
```
**การใช้งานเมนู:**
- พิมพ์ **เลข ID** ของเครื่องจักร เพื่อดูรายงานและวิเคราะห์เฉพาะเครื่องนั้น
- กด **Enter** ทันที เพื่อแสดงรายงานสรุปของเครื่องจักรทุกเครื่องพร้อมกัน

---

## 📁 โครงสร้างโปรเจกต์ (Project Structure)

```text
vibration-predictive-maintenance/
├── data/               # โฟลเดอร์เก็บไฟล์ข้อมูลดิบ (.txt)
├── output/             # โฟลเดอร์เก็บรายงาน (.csv) และกราฟแนวโน้ม (.png)
├── src/                # Source code แยกตามโมดูล (Modular Design)
│   ├── processor.py    # ส่วนประมวลผลข้อมูลและคำนวณ RMS
│   ├── analyzer.py     # ส่วนวิเคราะห์สถานะตามมาตรฐาน ISO 10816-3
│   └── predictor.py    # ส่วนพยากรณ์ Trend และสร้าง Visualization
├── .env                # ไฟล์กำหนดค่าตัวแปรระบบ (Configuration)
├── main.py             # จุดเริ่มต้นการรันโปรแกรมและ Interactive Menu
└── requirements.txt    # รายการ Library สำหรับติดตั้ง
```

---

## 🔧 การดูแลรักษาและอัปเดต (Maintenance)

1. **การปรับปรุงโมเดล**: หากข้อมูลมีลักษณะ Non-linear สามารถเปลี่ยนจาก `LinearRegression` เป็นโมเดลอื่นใน `src/predictor.py`
2. **การเพิ่มเครื่องจักร**: ระบบรองรับการเพิ่มไฟล์ `.txt` ใหม่ลงใน `data/` โดยโปรแกรมจะอัปเดตรายชื่อ ID ในเมนูให้โดยอัตโนมัติ
3. **เกณฑ์มาตรฐาน**: สามารถปรับค่า `THRESHOLD` ในไฟล์ `.env` ได้ตามความเหมาะสมของกลุ่มเครื่องจักร (Machine Group) ที่ใช้งานจริง
4. **Data Requirement**: การพยากรณ์แนวโน้ม (Trend) จำเป็นต้องมีข้อมูลอย่างน้อย 2 จุดขึ้นไป หากมีจุดเดียวระบบจะแสดงสถานะ ISO แต่จะข้ามการคำนวณพยากรณ์เพื่อความถูกต้องทางสถิติ