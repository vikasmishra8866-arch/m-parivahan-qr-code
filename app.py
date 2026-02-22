import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image
import pytesseract
import re

# Streamlit Cloud par Tesseract path
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

st.set_page_config(page_title="Compact Vehicle QR", layout="centered")

st.title("🚗 Compact Vehicle QR Generator")

uploaded_file = st.file_uploader("Browse Photo (Virtual RC)", type=["jpg", "jpeg", "png"])

# Default empty values
data = {"v_no": "", "reg_date": "", "owner": "", "chassis": "", "engine": ""}

if uploaded_file is not None:
    try:
        img_ocr = Image.open(uploaded_file)
        # Scan quality badhane ke liye grayscale
        text = pytesseract.image_to_string(img_ocr.convert('L'))
        
        # --- Advance Extraction Logic ---
        # 1. Vehicle Number (Pattern: GJ05CV9887)
        v_match = re.search(r'[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}', text)
        if v_match: data["v_no"] = v_match.group()

        # 2. Registration Date (Pattern: 25-Nov-2023)
        d_match = re.search(r'\d{1,2}-[A-Za-z]{3}-\d{4}', text)
        if d_match: data["reg_date"] = d_match.group()

        # 3. Owner Name (Name ke baad wali line)
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if "Name" in line and i+1 < len(lines):
                data["owner"] = lines[i].replace("Name", "").strip() or lines[i+1].strip()
            if "Chassis No." in line:
                data["chassis"] = line.split("No.")[-1].strip()
            if "Engine No." in line:
                data["engine"] = line.split("No.")[-1].strip()
                
    except Exception as e:
        st.error(f"Scanning Error: {e}")

with st.form("vehicle_form"):
    v_no = st.text_input("Vehicle Number", value=data["v_no"])
    reg_date = st.text_input("Registration Date", value=data["reg_date"])
    owner = st.text_input("Owner Name", value=data["owner"])
    chassis = st.text_input("Chassis Number", value=data["chassis"])
    engine = st.text_input("Engine Number", value=data["engine"])
    
    submit = st.form_submit_button("Generate Compact QR")

if submit:
    if v_no and owner:
        qr_data = f"Vehicle No: {v_no}\nReg Date: {reg_date}\nOwner: {owner}\nChassis: {chassis}\nEngine: {engine}"
        
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=0)
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buf = BytesIO()
        img.save(buf, format="PNG")
        
        st.success("✅ QR Taiyar Hai!")
        st.image(buf.getvalue(), width=250)
        st.download_button("📥 Download QR", data=buf.getvalue(), file_name=f"QR_{v_no}.png")
