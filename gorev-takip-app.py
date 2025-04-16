import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.set_page_config(page_title="Görev Takip Uygulaması", layout="centered")

st.title("📋 Görev Takip Uygulaması")

# Oturumda tabloyu tutmak için
if "gorevler" not in st.session_state:
    st.session_state["gorevler"] = []

# Giriş alanları
with st.form("gorev_formu"):
    col1, col2 = st.columns(2)
    with col1:
        gorev_adi = st.text_input("Görev Adı")
    with col2:
        sorumlu = st.text_input("Sorumlu Kişi")

    tarih = st.date_input("Tarih", value=datetime.today())

    ekle = st.form_submit_button("Görev Ekle")

    if ekle and gorev_adi and sorumlu:
        st.session_state["gorevler"].append({
            "Görev Adı": gorev_adi,
            "Sorumlu": sorumlu,
            "Tarih": tarih.strftime("%d.%m.%Y")
        })
        st.success("✅ Görev başarıyla eklendi.")

# Görevleri göster
if st.session_state["gorevler"]:
    df = pd.DataFrame(st.session_state["gorevler"])
    st.subheader("🗂️ Görev Listesi")
    st.dataframe(df, use_container_width=True)

    # Excel indirme butonu
    with io.BytesIO() as buffer:
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Görevler")
        excel_data = buffer.getvalue()

    st.download_button(
        label="📥 Excel olarak indir",
        data=excel_data,
        file_name="gorev_listesi.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("Henüz görev eklenmedi.")
