# สวัสดีครับสมาชิกชมรมทุกท่าน

## Microservice Architecture: To-Do App

ยินดีต้อนรับทุกท่านเข้าสู่โปรเจกต์ **To-Do App** ที่ถูกออกแบบมาในรูปแบบ **Microservice Architecture** ด้านล่างนี้เป็นคำแนะนำทีละขั้นตอนในการติดตั้งและใช้งานแอปพลิเคชันนี้

---

### 1. **เตรียมความพร้อม**
- ติดตั้ง **Git**: [ดาวน์โหลด Git](https://git-scm.com/)
- ติดตั้ง **Python** [ดาวน์โหลด Python](https://www.python.org/)
---

### 2. **การ Clone โปรเจกต์**

เปิด Command Prompt (Windows) หรือ Terminal (Mac/Linux) แล้วรันคำสั่งด้านล่าง:
```bash
git clone https://github.com/aikidoaikido115/Network.git
```

---

### 3. **ตั้งค่า Virtual Environment**

สร้าง Virtual Environment เพื่อแยก dependencies ของโปรเจกต์:
```bash
python -m venv venv
```
เปิดใช้งาน Virtual Environment:
- **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **Mac/Linux**:
  ```bash
  source venv/bin/activate
  ```

---

### 4. **ติดตั้ง Dependencies**

ติดตั้งไลบรารีที่จำเป็นทั้งหมดจากไฟล์ `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

### 5. **ตั้งค่า Environment Variables**

สร้างไฟล์ `.env` เพิ่มในโฟลเดอร์ llm_service
```plaintext
GEMINI=your_api_key
```

---

### **6. การรันแอปพลิเคชัน**
ในการรันแอปพลิเคชันแบบ Microservice Architecture คุณจะต้องเปิด Command Prompt หรือ Terminal หลายหน้าต่าง และรันแต่ละ Service ดังนี้:

1. เปิดหน้าต่าง **Command Prompt** หรือ **Terminal** สำหรับแต่ละ Service
2. ใช้คำสั่งด้านล่างนี้ในแต่ละหน้าต่างเพื่อรัน Service ที่เกี่ยวข้อง:

   - **Gateway Service**:  
     ```bash
     python gateway.py
     ```

   - **Gemini LLM Service**:  
     ```bash
     python gemini_llm.py
     ```

   - **Room Service**:  
     ```bash
     python room.py
     ```

   - **Task Service**:  
     ```bash
     python task.py
     ```

   - **Upload Image Service**:  
     ```bash
     python up_image.py
     ```

   - **User Service**:  
     ```bash
     python user.py
     ```

3. ตรวจสอบว่าแต่ละ Service ทำงานอยู่บนหน้าต่าง Command Prompt/Terminal แยกกัน