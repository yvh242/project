import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

st.title("QR-code generator met optioneel kader en 'Scan me' tekst")

# Invoer van de gebruiker
url = st.text_input("Voer een verplichte web link in")
image_file = st.file_uploader("Upload optioneel een afbeelding", type=["png", "jpg", "jpeg"])
add_border = st.checkbox("Kader rond QR-code")
add_text = st.checkbox("Voeg 'Scan me' tekst toe")

if url:
    # QR-code genereren
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # Optioneel afbeelding toevoegen
    if image_file:
        logo = Image.open(image_file)
        qr_width, qr_height = qr_img.size
        logo_size = qr_width // 4
        logo = logo.resize((logo_size, logo_size))
        pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
        qr_img.paste(logo, pos, mask=logo if logo.mode == "RGBA" else None)

    # Kader toevoegen
    if add_border:
        border_size = 20
        new_size = (qr_img.width + border_size * 2, qr_img.height + border_size * 2)
        bordered_img = Image.new("RGB", new_size, "black")
        bordered_img.paste(qr_img, (border_size, border_size))
        qr_img = bordered_img

    # 'Scan me' tekst toevoegen
    if add_text:
        draw = ImageDraw.Draw(qr_img)
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()

        text = "Scan me"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (qr_img.width - text_width) // 2
        y = qr_img.height - text_height - 10
        draw.text((x, y), text, font=font, fill="black")

    # QR-code weergeven
    st.image(qr_img)

    # Downloadknop
    buf = io.BytesIO()
    qr_img.save(buf, format="PNG")
    buf.seek(0)
    st.download_button("Download QR-code", data=buf, file_name="qr_code.png", mime="image/png")
else:
    st.warning("Gelieve een web link in te vullen.")
