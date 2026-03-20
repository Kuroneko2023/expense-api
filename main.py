import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from supabase import create_client, Client
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import uvicorn  

# สั่งให้โหลดไฟล์ .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# --- ระบบตบตาเช็คบั๊ก (เดี๋ยวค่อยลบทีหลัง) ---
print("==== เช็คสถานะไฟล์ .env ====")
print(f"URL ที่ดึงมาได้: {SUPABASE_URL}")
print(f"KEY ที่ดึงมาได้: {'มีข้อมูล (ยาวๆ)' if SUPABASE_KEY else 'None'}")
print("===========================")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("🚨 แจ้งเตือน: หาไฟล์ .env ไม่เจอ หรือในไฟล์ไม่มีคำว่า SUPABASE_URL ครับ")
    print("👉 วิธีแก้: เช็คว่าสร้างไฟล์ชื่อ .env ถูกต้องไหม และต้องอยู่โฟลเดอร์เดียวกับ main.py นะ")
    exit() # สั่งหยุดการทำงานทันทีจะได้ไม่ Error แดงๆ ยาวๆ
# ----------------------------------------

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()
# 2. ปลดล็อก CORS (เพื่อให้ App มือถือคุยกับคอมได้)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Transaction(BaseModel):
    type: str
    amount: float
    category: str
    note: Optional[str] = None
    transaction_date: str

# 3. Routes สำหรับดึงข้อมูล
@app.get("/transactions")
def get_all_transactions():
    try:
        response = supabase.table("transactions").select("*").execute()
        return {"data": response.data}
    except Exception as e:
        return {"error": str(e)}

# 4. Routes สำหรับเพิ่มข้อมูล
@app.post("/transactions")
def add_transaction(transaction: Transaction):
    try:
        data_to_insert = {
            "type": transaction.type,
            "amount": transaction.amount,
            "category": transaction.category,
            "note": transaction.note,
            "transaction_date": transaction.transaction_date
        }
        response = supabase.table("transactions").insert(data_to_insert).execute()
        return {"message": "บันทึกสำเร็จ!", "data": response.data}
    except Exception as e:
        return {"error": str(e)}

# --- ส่วนที่แก้ไข: การย่อหน้าต้องชิดขอบซ้ายสุด ไม่ซ้อนอยู่ในฟังก์ชันใดๆ ---
if __name__ == "__main__":
    # host="0.0.0.0" สำคัญมาก เพื่อให้ Device อื่นในวงแลนมองเห็นคอมเครื่องนี้
    uvicorn.run(app, host="0.0.0.0", port=8000)