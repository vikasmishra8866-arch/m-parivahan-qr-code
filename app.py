import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image
import pytesseract
import re

# Streamlit Cloud par Tesseract ka rasta (Path)
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

st.set_page_config(page_title="Compact Vehicle QR", layout="centered")

st.title("🚗 Compact Vehicle QR Generator")

# --- Browse Photo Option ---
uploaded_file = st.file_uploader("Browse Photo (Virtual RC)", type=["jpg", "jpeg", "png"])

# Default values
v_no_val = ""
reg_date_val = ""
owner_val = ""
chassis_val = ""
engine_val = ""

if uploaded_file is not None:
    try:
        img_ocr = Image.open(uploaded_file)
        # Photo se text nikalne ki koshish
        text = pytesseract.image_to_string(img_ocr)
        
        # Regex se data match karna (Aapki photo ke hisaab se)
        v_no_match = re.search(r'[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}', text)
        if v_no_match: v_no_val = v_no_match.group()
        
        # Owner name aksar 'Name' ke baad hota hai
        owner_match = re.search(r'Name\s+([A-Z\s]+)', text)
        if owner_match: owner_val = owner_match.group(1).strip()

        # Chassis number match
        chassis_match = re.search(r'Chassis No\.\s+([A-Z0-9]+)', text)
        if chassis_match: chassis_val = chassis_match.group(1).strip()
    except Exception as e:
        st.warning("Photo scan karne mein thodi dikkat hui, aap manual bhi bhar sakte hain.")

with st.form("vehicle_form"):
    # Boxes automatic fill ho jayenge agar photo upload ki hai
    v_no = st.text_input("Vehicle Number", value=v_no_val, placeholder="GJ05BY9222")
    reg_date = st.text_input("Registration Date", value=reg_date_val, placeholder="16/07/2025")
    owner = st.text_input("Owner Name", value=owner_val, placeholder="AGARWAL ENTERPRISE")
    chassis = st.text_input("Chassis Number", value=chassis_val, placeholder="MA3ERXXXXXXXX")
    engine = st.text_input("Engine Number", value=engine_val, placeholder="E374XXXXX")
    
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
