import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Vehicle QR Generator", layout="centered")

st.title("🚗 Vehicle Detail QR Generator")
st.write("Details bhariye aur scan-able QR code generate kijiye.")

# --- Detail Input Form ---
with st.form("vehicle_form"):
    v_no = st.text_input("Vehicle Number", placeholder="GJ05BY9222")
    reg_date = st.text_input("Registration Date", placeholder="16/07/2025")
    owner = st.text_input("Owner Name", placeholder="AGARWAL ENTERPRISE")
    chassis = st.text_input("Chassis Number", placeholder="MA3ERXXXXXXXX")
    engine = st.text_input("Engine Number", placeholder="E374XXXXX")
    
    submit = st.form_submit_button("Generate QR Code")

if submit:
    if v_no and owner:
        # --- Data Formatting for QR ---
        # Jab koi scan karega toh ye text dikhega
        qr_data = f"""📝 VEHICLE DETAILS
---------------------------
🔹 Vehicle No: {v_no}
🔹 Reg. Date: {reg_date}
🔹 Owner: {owner}
🔹 Chassis No: {chassis}
🔹 Engine No: {engine}
---------------------------
🔗 More Info: https://parivahan.gov.in/
"""

        # --- QR Code Generation ---
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to buffer for download
        buf = BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()

        # --- Display Result ---
        st.success("✅ QR Code Taiyar Hai!")
        st.image(byte_im, caption="Scan karne par details dikhengi", width=300)

        # --- Download Button ---
        st.download_button(
            label="📥 Download QR Code",
            data=byte_im,
            file_name=f"QR_{v_no}.png",
            mime="image/png"
        )
        
        st.info("💡 Tip: Is QR ko scan karke check karein, saari details M-Parivahan link ke saath dikhengi.")
    else:
        st.error("⚠️ Please kam se kam Vehicle Number aur Owner Name bhariye.")
