import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.set_page_config(page_title="Görev Takip", layout="centered")

st.markdown("""
    <style>
        .big-button > button {
            width: 100%;
            padding: 0.75em;
            font-size: 1.1em;
            background-color: #1E90FF;
            color: white;
            border-radius: 8px;
        }

        .gorev-kart {
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 1em;
            margin-bottom: 1em;
            background-color: #f9f9f9;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
        }

        .gorev-baslik {
            font-weight: bold;
            font-size: 1.05em;
            margin-bottom: 0.3em;
        }

        .gorev-detay {
            font-size: 0.95em;
            color: #444;
        }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>📋 Görev Takip</h2>", unsafe_allow_html=True)

if "gorevler" not in st.session_state:
    st.session_state["gorevler"] = []

st.markdown("### ➕ Yeni Görev")

with st.form("form", clear_on_submit=True):
    gorev_adi = st.text_input("Görev Adı", placeholder="Örn: Sipariş Kontrolü")
    sorumlu = st.text_input("Sorumlu Kişi", placeholder="Örn: Ayşe")
    tarih = st.date_input("Tarih", value=datetime.today())
    submitted = st.form_submit_button("✅ Görevi Kaydet")

    if submitted:
        if gorev_adi and sorumlu:
            st.session_state["gorevler"].append({
                "Görev": gorev_adi,
                "Sorumlu": sorumlu,
                "Tarih": tarih.strftime("%d.%m.%Y")
            })
            st.success("Görev başarıyla kaydedildi ✅")
        else:
            st.warning("Lütfen tüm alanları doldurun.")

if st.session_state["gorevler"]:
    st.markdown("### 📌 Kayıtlı Görevler")

    for gorev in reversed(st.session_state["gorevler"]):
        st.markdown(f"""
        <div class="gorev-kart">
            <div class="gorev-baslik">{gorev['Görev']}</div>
            <div class="gorev-detay">👤 {gorev['Sorumlu']}</div>
            <div class="gorev-detay">📅 {gorev['Tarih']}</div>
        </div>
        """, unsafe_allow_html=True)

    df = pd.DataFrame(st.session_state["gorevler"])
    with io.BytesIO() as buffer:
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Görevler")
        data = buffer.getvalue()

    st.download_button(
        label="📥 Excel'e Aktar",
        data=data,
        file_name="gorevler.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("Henüz görev eklenmedi.")
