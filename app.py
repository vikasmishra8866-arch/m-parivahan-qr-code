import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image
import pytesseract
import re

# Tesseract path for Streamlit Cloud
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

st.set_page_config(page_title="Compact Vehicle QR", layout="centered")
st.title("🚗 Compact Vehicle QR Generator")

uploaded_file = st.file_uploader("Browse Photo (Virtual RC)", type=["jpg", "jpeg", "png"])

# Data storage
res = {"v": "", "d": "", "o": "", "c": "", "e": ""}

if uploaded_file:
    img = Image.open(uploaded_file)
    # Text extraction with better configuration
    raw_text = pytesseract.image_to_string(img, config='--psm 6')
    
    # --- Strict Extraction Logic ---
    # 1. Vehicle No (Sabse upar bold mein hota hai)
    v_match = re.search(r'[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}', raw_text)
    if v_match: res["v"] = v_match.group()

    # 2. Owner Name (Line after 'Name')
    if "Name" in raw_text:
        res["o"] = raw_text.split("Name")[-1].split("\n")[0].strip()

    # 3. Chassis No
    if "Chassis No." in raw_text:
        res["c"] = raw_text.split("Chassis No.")[-1].split("\n")[0].strip()

    # 4. Engine No
    if "Engine No." in raw_text:
        res["e"] = raw_text.split("Engine No.")[-1].split("\n")[0].strip()

    # 5. Reg Date
    d_match = re.search(r'\d{2}-[A-Za-z]{3}-\d{4}', raw_text)
    if d_match: res["d"] = d_match.group()

with st.form("vehicle_form"):
    v_no = st.text_input("Vehicle Number", value=res["v"])
    reg_date = st.text_input("Registration Date", value=res["d"])
    owner = st.text_input("Owner Name", value=res["o"])
    chassis = st.text_input("Chassis Number", value=res["c"])
    engine = st.text_input("Engine Number", value=res["e"])
    submit = st.form_submit_button("Generate Compact QR")

if submit:
    if v_no and owner:
        qr_data = f"Vehicle: {v_no}\nDate: {reg_date}\nOwner: {owner}\nChassis: {chassis}\nEngine: {engine}"
        qr = qrcode.QRCode(version=1, box_size=8, border=0)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img_qr = qr.make_image(fill_color="black", back_color="white")
        buf = BytesIO()
        img_qr.save(buf, format="PNG")
        st.image(buf.getvalue(), width=250)
        st.download_button("📥 Download QR", buf.getvalue(), f"{v_no}.png")
