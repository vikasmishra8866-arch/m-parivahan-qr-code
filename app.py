import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Compact Vehicle QR", layout="centered")

st.title("🚗 Compact Vehicle QR Generator")

with st.form("vehicle_form"):
    v_no = st.text_input("Vehicle Number", placeholder="GJ05BY9222")
    reg_date = st.text_input("Registration Date", placeholder="16/07/2025")
    owner = st.text_input("Owner Name", placeholder="AGARWAL ENTERPRISE")
    chassis = st.text_input("Chassis Number", placeholder="MA3ERXXXXXXXX")
    engine = st.text_input("Engine Number", placeholder="E374XXXXX")
    
    submit = st.form_submit_button("Generate Compact QR")

if submit:
    if v_no and owner:
        qr_data = f"""📝 VEHICLE DETAILS
---------------------------
🔹 Vehicle No: {v_no}
🔹 Reg. Date: {reg_date}
🔹 Owner: {owner}
🔹 Chassis No: {chassis}
🔹 Engine No: {engine}
---------------------------
🔗 More Info: https://parivahan.gov.in/"""

        # --- QR Logic (Waisa hi jaisa aapne manga tha) ---
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=8,
            border=0,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        
        buf = BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.success("✅ Compact QR Taiyar Hai!")
        
        st.image(byte_im, caption="Scan karein (No Borders)", width=250)

        st.download_button(
            label="📥 Download Compact QR",
            data=byte_im,
            file_name=f"Compact_QR_{v_no}.png",
            mime="image/png"
        )
    else:
        st.error("⚠️ Detail bharna zaroori hai.")
