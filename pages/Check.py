# mijn_streamlit_app/pages/2_Andere_Pagina.py
import streamlit as st
import qrcode
from PIL import Image
import io

st.set_page_config(page_title="QR Code Generator", page_icon="🔗", layout="centered")

st.title("🔗 QR Code Generator")

# --- Verplichte invoer ---
url = st.text_input("Voer een URL in (verplicht):", placeholder="https://example.com")

# --- Optionele afbeelding ---
uploaded_image = st.file_uploader("Optionele afbeelding (logo in QR code)", type=["png", "jpg", "jpeg"])

generate_button = st.button("Genereer QR code")

if generate_button:
    if not url.strip():
        st.error("⚠️ Je moet een geldige URL invullen!")
    else:
        # QR-code maken
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # H = hoogste foutcorrectie (nodig voor logo)
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img_qr = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        # Logo toevoegen als er een afbeelding is
        if uploaded_image is not None:
            logo = Image.open(uploaded_image)

            # Logo verkleinen
            qr_width, qr_height = img_qr.size
            factor = 4  # Logo 1/4 van QR breedte
            logo_size = qr_width // factor
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

            # Logo plaatsen in het midden
            pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            img_qr.paste(logo, pos, mask=logo if logo.mode == "RGBA" else None)

        # QR code tonen
        st.image(img_qr, caption="Gegenereerde QR Code")

        # Download-knop
        buf = io.BytesIO()
        img_qr.save(buf, format="PNG")
        st.download_button(
            label="📥 Download QR code",
            data=buf.getvalue(),
            file_name="qrcode.png",
            mime="image/png"
        )
