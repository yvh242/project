import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="QR Code Generator", page_icon="🔗", layout="centered")

st.title("🔗 QR Code Generator")

# --- Verplichte invoer ---
url = st.text_input("Voer een URL in (verplicht):", placeholder="https://example.com")

# --- Opties ---
uploaded_image = st.file_uploader("Optionele afbeelding (logo in QR code)", type=["png", "jpg", "jpeg"])
add_border = st.checkbox("Kader rond QR-code")
add_text = st.checkbox("Voeg 'Scan Me' label toe")

generate_button = st.button("Genereer QR code")

if generate_button:
    if not url.strip():
        st.error("⚠️ Je moet een geldige URL invullen!")
    else:
        # QR-code maken
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img_qr = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        # Logo toevoegen als er een afbeelding is
        if uploaded_image is not None:
            logo = Image.open(uploaded_image)
            qr_width, qr_height = img_qr.size
            factor = 4
            logo_size = qr_width // factor
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            img_qr.paste(logo, pos, mask=logo if logo.mode == "RGBA" else None)

        # Kader toevoegen
        if add_border:
            border_size = 20
            new_size = (img_qr.size[0] + border_size * 2, img_qr.size[1] + border_size * 2)
            bordered_img = Image.new("RGB", new_size, "black")
            bordered_img.paste(img_qr, (border_size, border_size))
            img_qr = bordered_img

        # Tekst toevoegen
        if add_text:
            font_size = 40
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()

            text = "Scan Me"
            text_width, text_height = font.getsize(text)

            # Nieuw canvas voor extra ruimte onder QR
            new_img = Image.new("RGB", (img_qr.size[0], img_qr.size[1] + text_height + 10), "white")
            new_img.paste(img_qr, (0, 0))

            # Tekst tekenen
            draw = ImageDraw.Draw(new_img)
            text_x = (new_img.size[0] - text_width) // 2
            draw.text((text_x, img_qr.size[1] + 5), text, fill="black", font=font)

            img_qr = new_img

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
