# 🛠️ Vibration Predictive Maintenance System (ISO 10816-3)

ระบบวิเคราะห์แนวโน้มความเสียหายของเครื่องจักรหมุน (Rotating Machinery) โดยอ้างอิงตามมาตรฐาน **ISO 10816-3**. โปรแกรมนี้สามารถอ่านข้อมูลความสั่นสะเทือนแบบ Waveform (Acceleration in G-s), คำนวณค่า RMS, จำแนกสถานะความปลอดภัย และพยากรณ์วันที่คาดว่าเครื่องจักรจะชำรุดล่วงหน้าด้วย Machine Learning.

## 📋 คุณสมบัติของระบบ

* **Data Processing**: ดึงข้อมูลจากไฟล์ `.txt` และแปลงค่า Acceleration เป็น RMS อัตโนมัติ.
* **ISO Analysis**: จำแนกสถานะเครื่องจักรเป็น 4 โซน (Green, Yellow, Orange, Red) ตามมาตรฐานสากล.
* **Predictive Modeling**: ใช้ Linear Regression เพื่อคำนวณหา Remaining Useful Life (RUL).
* **Environment Support**: ตั้งค่า Path ข้อมูลและเกณฑ์การตัดสินใจผ่านไฟล์ `.env`.

---

## 🚀 การเริ่มต้นใช้งาน (Getting Started)

### 1. สิ่งที่ต้องติดตั้งก่อน (Prerequisites)

เครื่องของคุณต้องมี **Python 3.8+** และติดตั้ง Library ที่จำเป็นดังนี้:

### การสร้าง Virtual Environment (แนะนำ)

เพื่อความสะอาดของระบบและป้องกันความขัดแย้งของ Library แนะนำให้สร้าง Environment ก่อนติดตั้ง `requirements.txt` ตามขั้นตอนของแต่ละ OS ดังนี้:

#### **สำหรับ Windows (PowerShell)**

```powershell
# 1. สร้าง Environment ชื่อ .venv
python -m venv .venv

# 2. Activate (เปิดใช้งาน)
.\.venv\Scripts\Activate.ps1

```

#### **สำหรับ Windows (Command Prompt)**

```cmd
# 1. สร้าง Environment
python -m venv .venv

# 2. Activate
.venv\Scripts\activate

```

#### **สำหรับ macOS / Linux**

```bash
# 1. สร้าง Environment
python3 -m venv .venv

# 2. Activate
source .venv/bin/activate

```

> **หมายเหตุ:** เมื่อทำการ Activate สำเร็จ คุณจะเห็นตัวอักษร `(.venv)` ปรากฏอยู่ที่หน้าชื่อบรรทัดใน Terminal ของคุณ หลังจากนั้นจึงค่อยเริ่มรันคำสั่ง `pip install -r requirements.txt` ครับ

---

### 💡 การปิดใช้งาน (Deactivate)

เมื่อเลิกใช้งานโปรเจกต์นี้แล้ว คุณสามารถออกจาก Environment ได้ง่ายๆ ด้วยคำสั่ง:

```bash
deactivate

```

---

### 🛠️ การ Maintenance โค้ดในอนาคต (เพิ่มเติม)

เพื่อให้โปรเจกต์นี้ทำงานได้อย่างต่อเนื่องในระยะยาว ควรทำสิ่งต่อไปนี้:

1. **Update Library**: หากมีการอัปเดต Library ใหม่ๆ ในอนาคต และคุณต้องการบันทึกเวอร์ชันปัจจุบันไว้ให้แม่นยำ ให้รันคำสั่ง:
```bash
pip freeze > requirements.txt

```

2. **Handle Data Scenarios**:
* หากไฟล์ใน `data/` มีการเปลี่ยน Format (เช่น เปลี่ยนชื่อหัวคอลัมน์) ให้ไปแก้ไข Regex ใน `src/processor.py`
* หากค่าพยากรณ์ใน `src/predictor.py` เริ่มไม่แม่นยำ ให้พิจารณาเปลี่ยนจาก `LinearRegression` เป็น `PolynomialFeatures` (องศาที่ 2) เพื่อรองรับกราฟที่เป็นเส้นโค้ง

3. **Log Monitoring**: หากรันผ่าน Task Scheduler ในอนาคต ควรเพิ่มการเก็บ Log ไฟล์ลงในโฟลเดอร์ `logs/` เพื่อตรวจสอบ Error ย้อนหลัง


*(Library หลักที่ใช้: `pandas`, `numpy`, `scikit-learn`, `python-dotenv`, `scipy`)*

### 2. การตั้งค่า Environment (.env)

สร้างไฟล์ชื่อ `.env` ไว้ที่ root directory ของโปรเจกต์ โดยอ้างอิงจากตัวอย่างใน `.env.example` และแก้ไขค่าของแต่ละตัวแปรตามที่ต้องการ

### 3. การรันโปรแกรม

เตรียมไฟล์ข้อมูล `.txt` ไว้ในโฟลเดอร์ `data/` จากนั้นรันคำสั่ง:

```bash
python main.py

```

---

## 📁 โครงสร้างโปรเจกต์

```text
vibration-predictive-maintenance/
├── data/           # เก็บไฟล์ .txt ข้อมูลความสั่นสะเทือน (Input)
├── output/         # ไฟล์รายงานสรุปในรูปแบบ .csv (Output)
├── src/            # Source code หลัก
│   ├── processor.py   # จัดการข้อมูลดิบและการดึงค่า (Parser)
│   ├── analyzer.py    # วิเคราะห์สถานะตามมาตรฐาน ISO
│   └── predictor.py   # พยากรณ์แนวโน้มความเสียหาย
├── main.py         # ไฟล์หลักสำหรับรันระบบทั้งหมด
└── requirements.txt

```

---

## 🔧 การดูแลรักษาโค้ด (Maintenance Guide)

### การเพิ่มเกณฑ์มาตรฐานใหม่

หากต้องการเปลี่ยนกลุ่มเครื่องจักร (Machinery Group) ตามมาตรฐาน ISO 10816-3 ให้แก้ไขค่า Threshold ในไฟล์ `.env` โดยไม่ต้องแก้ไขโค้ดใน `src/analyzer.py`.

### การปรับปรุง Model การพยากรณ์

หากมีข้อมูลสะสมมากขึ้น (มากกว่า 10 จุดต่อเครื่อง) สามารถเปลี่ยนอัลกอริทึมใน `src/predictor.py` จาก `LinearRegression` เป็น `Prophet` หรือ `LSTM` เพื่อความแม่นยำที่สูงขึ้นในกรณีที่กราฟไม่เป็นเส้นตรง.

### การจัดการข้อมูล Input

ไฟล์ข้อมูลใหม่ที่จะนำมาใช้ ต้องมีโครงสร้าง Header (Equipment, Date/Time, Amplitude) ตรงตามรูปแบบเดิมเพื่อให้ Regex ใน `processor.py` ทำงานได้ถูกต้อง.

---

## 📊 ผลลัพธ์ (Example Output)

เมื่อรันเสร็จสิ้น ระบบจะแสดงรายงานสรุปบนหน้าจอและสร้างไฟล์ `maintenance_report.csv` ในโฟลเดอร์ `output/` โดยมีข้อมูลดังนี้:

* **Latest_RMS**: ค่าความสั่นสะเทือนล่าสุด.
* **Current_Status**: สถานะปัจจุบันตามโซนสี.
* **Est_Failure_Date**: วันที่คาดการณ์ว่าเครื่องจะพัง (หากแนวโน้มแย่ลง).
