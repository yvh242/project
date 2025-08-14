import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

st.title("QR-code Generator met kader en 'Scan me'")

# Invoer
url = st.text_input("Voer een weblink in (verplicht):")
image_file = st.file_uploader("Optionele afbeelding (logo)", type=["png", "jpg", "jpeg"])
add_frame = st.checkbox("Voeg afgeronde kader toe")
add_scan_me = st.checkbox("Voeg 'Scan me' tekst toe")

if url:
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

    # Optioneel logo toevoegen
    if image_file:
        logo = Image.open(image_file).convert("RGBA")
        qr_width, qr_height = img_qr.size
        logo_size = qr_width // 4
        logo.thumbnail((logo_size, logo_size))
        pos = ((qr_width - logo.width) // 2, (qr_height - logo.height) // 2)
        img_qr.paste(logo, pos, logo)

    # Optioneel kader toevoegen
    if add_frame or add_scan_me:
        padding = 40
        frame_img = Image.new("RGB", (img_qr.width + padding*2, img_qr.height + padding*2), "white")
        draw = ImageDraw.Draw(frame_img)

        if add_frame:
            radius = 20
            draw.rounded_rectangle(
                [(0, 0), frame_img.size],
                radius=radius,
                outline="black",
                width=5
            )
        frame_img.paste(img_qr, (padding, padding))

        # Optioneel "Scan me"
        if add_scan_me:
            try:
                font = ImageFont.truetype("arial.ttf", 30)
            except:
                font = ImageFont.load_default()

            text = "Scan me"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = (frame_img.width - text_width) // 2
            text_y = frame_img.height - text_height - 10
            draw.text((text_x, text_y), text, font=font, fill="black")

        img_qr = frame_img

    # Weergave
    st.image(img_qr)

    # Download
    buf = io.BytesIO()
    img_qr.save(buf, format="PNG")
    st.download_button("Download QR-code", buf.getvalue(), file_name="qr_code.png", mime="image/png")
else:
    st.warning("Voer eerst een weblink in.")
