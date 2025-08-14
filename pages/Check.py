import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

st.title("QR Code Generator met optionele afbeelding en 'Scan Me' label")

# Invoer voor verplichte weblink
url = st.text_input("Voer de URL in (verplicht):", "")

# Upload optionele afbeelding
uploaded_image = st.file_uploader("Optionele afbeelding toevoegen (bijv. logo)", type=["png", "jpg", "jpeg"])

# Opties
add_frame = st.checkbox("Kader rond QR-code")
add_scan_me = st.checkbox("'Scan Me' label toevoegen")

if st.button("Genereer QR Code"):
    if not url.strip():
        st.error("Je moet een URL invullen.")
    else:
        # QR-code maken
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        # Afbeelding toevoegen (optioneel)
        if uploaded_image:
            logo = Image.open(uploaded_image)
            logo_size = int(qr_img.size[0] * 0.2)
            logo = logo.resize((logo_size, logo_size))
            pos = ((qr_img.size[0] - logo_size) // 2, (qr_img.size[1] - logo_size) // 2)
            qr_img.paste(logo, pos)

        draw = ImageDraw.Draw(qr_img)

        # Kader toevoegen
        if add_frame:
            border_thickness = 10
            draw.rectangle(
                [(0, 0), (qr_img.size[0] - 1, qr_img.size[1] - 1)],
                outline="black",
                width=border_thickness
            )

        # "Scan Me" toevoegen
        if add_scan_me:
            font = ImageFont.load_default()
            text = "SCAN ME"

            # Bepaal tekstgrootte via textbbox
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # Nieuwe afbeelding maken met extra ruimte onderaan
            new_height = qr_img.size[1] + text_height + 20
            new_img = Image.new("RGB", (qr_img.size[0], new_height), "white")
            new_img.paste(qr_img, (0, 0))

            # Tekst centreren
            text_x = (qr_img.size[0] - text_width) // 2
            text_y = qr_img.size[1] + 10
            draw = ImageDraw.Draw(new_img)
            draw.text((text_x, text_y), text, fill="black", font=font)

            qr_img = new_img

        # Tonen in Streamlit
        st.image(qr_img)

        # Downloadknop
        buf = io.BytesIO()
        qr_img.save(buf, format="PNG")
        st.download_button("Download QR Code", data=buf.getvalue(), file_name="qrcode.png", mime="image/png")
