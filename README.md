# 💰 Expense Tracker App (Full-stack Mobile Application)

แอปพลิเคชันจัดการรายรับ-รายจ่ายที่เน้นความเร็วในการใช้งาน (Quick UX) และการวิเคราะห์ข้อมูลที่ชัดเจน พัฒนาด้วยเทคโนโลยีที่ทันสมัยทั้ง Frontend และ Backend

### 🚀 Key Features
* **Quick Entry:** บันทึกรายการได้รวดเร็วพร้อมระบบ Quick Notes ตามหมวดหมู่
* **Data Visualization:** แสดงผลรายจ่ายรายเดือนด้วย Pie Chart (react-native-chart-kit)
* **Daily Grouping:** ระบบจัดกลุ่มรายการแยกตามวันที่ ดูง่าย เป็นระเบียบ
* **Professional UX:** มีการใช้ Haptic Feedback (ระบบสั่น) และ Loading States

### 🛠 Tech Stack
* **Frontend:** React Native (Expo Router), Axios, Lucide Icons
* **Backend:** Python (FastAPI / Flask), SQLite
* **State Management:** React Hooks (useState, useEffect, useCallback)

### 📦 Installation & Setup
1. **Backend:**
   - `cd backend`
   - `pip install -r requirements.txt`
   - `python main.py`
2. **Frontend:**
   - `cd expense-app`
   - `npm install`
   - สร้างไฟล์ `.env` และกำหนด `EXPO_PUBLIC_API_URL`
   - `npx expo start`