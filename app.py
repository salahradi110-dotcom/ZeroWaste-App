import streamlit as st
import datetime
import pandas as pd
import os

# إعدادات الصفحة
st.set_page_config(page_title="ZeroWaste Home", page_icon="🥗", layout="centered")

# دالة لحفظ وتحميل البيانات (بشكل محلي بسيط)
if 'inventory' not in st.session_state:
    st.session_state.inventory = []

st.title("🥗 تطبيق ZeroWaste Home")
st.write("ابدأ بتنظيم مطبخك وتقليل الهدر الغذائي!")

# واجهة الإضافة
with st.expander("➕ إضافة صنف جديد"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("اسم المنتج")
    with col2:
        expiry = st.date_input("تاريخ الانتهاء", datetime.date.today())
    
    if st.button("إضافة للمخزن"):
        if name:
            st.session_state.inventory.append({"المنتج": name, "التاريخ": expiry})
            st.success(f"تمت إضافة {name}")
        else:
            st.error("أدخل اسم المنتج!")

# عرض القائمة
if st.session_state.inventory:
    df = pd.DataFrame(st.session_state.inventory)
    today = datetime.date.today()
    df['أيام متبقية'] = df['التاريخ'].apply(lambda x: (x - today).days)
    
    st.subheader("📋 حالة المخزن")
    st.dataframe(df.sort_values(by='أيام متبقية'), use_container_width=True)
    
    # تنبيهات
    for _, row in df.iterrows():
        if 0 <= row['أيام متبقية'] <= 2:
            st.warning(f"⚠️ {row['المنتج']} سينتهي قريباً!")
else:
    st.info("مخزنك فارغ حالياً.")
