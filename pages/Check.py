import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

st.title("QR-code generator met optionele afbeelding en 'Scan Me' optie")

# Invoer
url = st.text_input("Voer de verplichte weblink in (URL):")
image_file = st.file_uploader("Optionele afbeelding uploaden", type=["png", "jpg", "jpeg"])
add_frame = st.checkbox("Kader rond QR-code")
add_scan_me = st.checkbox("Voeg 'Scan Me'-tekst toe")

if url:
    # QR-code maken
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )
    qr.add_data(url)
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # Afbeelding toevoegen in het midden
    if image_file:
        logo = Image.open(image_file)
        qr_width, qr_height = img_qr.size
        logo_size = qr_width // 4
        logo = logo.resize((logo_size, logo_size))
        pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
        img_qr.paste(logo, pos)

    draw = ImageDraw.Draw(img_qr)

    # Kader rond QR
    if add_frame:
        thickness = 8
        draw.rectangle(
            [(0, 0), (img_qr.size[0] - 1, img_qr.size[1] - 1)],
            outline="black", width=thickness
        )

    # "Scan Me"-tekst toevoegen
    if add_scan_me:
        try:
            font = ImageFont.truetype("arial.ttf", 28)
        except:
            font = ImageFont.load_default()

        text = "SCAN ME"
        text_width, text_height = draw.textsize(text, font=font)

        # Nieuw canvas maken met extra ruimte voor tekst
        new_height = img_qr.size[1] + text_height + 20
        new_img = Image.new("RGB", (img_qr.size[0], new_height), "white")
        new_img.paste(img_qr, (0, 0))

        draw = ImageDraw.Draw(new_img)

        # Kader rond tekst
        padding_x = 20
        padding_y = 5
        text_x = (new_img.size[0] - text_width) // 2
        text_y = img_qr.size[1] + 10
        box_coords = [
            (text_x - padding_x, text_y - padding_y),
            (text_x + text_width + padding_x, text_y + text_height + padding_y)
        ]
        draw.rounded_rectangle(box_coords, radius=15, outline="black", width=2)

        # Tekst tekenen
        draw.text((text_x, text_y), text, font=font, fill="black")
        img_qr = new_img

    # Resultaat tonen
    st.image(img_qr)

    # Downloadknop
    buf = io.BytesIO()
    img_qr.save(buf, format="PNG")
    st.download_button("Download QR-code", data=buf.getvalue(), file_name="qr_code.png", mime="image/png")
