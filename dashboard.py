import streamlit as st
import pandas as pd
import plotly.express as px
import requests  # ใช้ตัวนี้แทน supabase เพราะติดตั้งง่ายกว่ามาก

st.set_page_config(page_title="My Money Dashboard", layout="wide")

st.title("📊 สรุปภาพรวมการเงิน")

# ฟังก์ชันดึงข้อมูลจาก FastAPI (ตัว Python ที่คุณรัน uvicorn ไว้)
def load_data():
    try:
        # ดึงข้อมูลจาก API หลังบ้านของเราโดยตรง
        response = requests.get('http://127.0.0.1:8000/transactions')
        data = response.json()['data']
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"เชื่อมต่อหลังบ้านไม่ได้: {e}")
        return pd.DataFrame()

# โหลดข้อมูลมาใส่ตัวแปร df
df = load_data()

if not df.empty:
    # คำนวณยอดรวม (เหมือนเดิม)
    total_income = df[df['type'] == 'income']['amount'].sum()
    total_expense = df[df['type'] == 'expense']['amount'].sum()
    balance = total_income - total_expense

    # แสดงบัตรตัวเลขสรุป
    col1, col2, col3 = st.columns(3)
    col1.metric("รายรับทั้งหมด", f"฿{total_income:,.2f}")
    col2.metric("รายจ่ายทั้งหมด", f"฿{total_expense:,.2f}", delta_color="inverse")
    col3.metric("ยอดคงเหลือ", f"฿{balance:,.2f}")

    st.divider()

    # กราฟวงกลมสรุปรายจ่าย
    st.subheader("🛒 สัดส่วนรายจ่ายตามหมวดหมู่")
    expense_df = df[df['type'] == 'expense']
    
    if not expense_df.empty:
        fig = px.pie(expense_df, values='amount', names='category', 
                     hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("ยังไม่มีข้อมูลรายจ่าย")

    # แสดงตารางข้อมูล
    st.subheader("📋 รายการทั้งหมด")
    st.dataframe(df.sort_values('transaction_date', ascending=False), use_container_width=True)

else:
    st.warning("ไม่พบข้อมูลในระบบ หรือยังไม่ได้รัน FastAPI (uvicorn)")