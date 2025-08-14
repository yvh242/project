import streamlit as st
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image, ImageDraw, ImageFont
import io

st.title("QR-code generator met 'Scan Me' optie")

# Input velden
url = st.text_input("Voer de weblink in (verplicht)")
uploaded_logo = st.file_uploader("Optioneel: upload een afbeelding (logo) voor in het midden van de QR-code", type=["png", "jpg", "jpeg"])
add_scan_me = st.checkbox("Voeg 'Scan Me' toe met kader", value=False)

if st.button("Genereer QR-code"):
    if not url:
        st.error("⚠️ Vul eerst een weblink in.")
    else:
        # QR-code maken
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        qr_img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            color_mask=SolidFillColorMask(back_color="white", front_color="black")
        ).convert("RGBA")

        # Logo in QR plaatsen
        if uploaded_logo:
            logo = Image.open(uploaded_logo).convert("RGBA")
            logo_size = int(qr_img.size[0] * 0.2)
            logo = logo.resize((logo_size, logo_size))
            pos = ((qr_img.size[0] - logo_size) // 2, (qr_img.size[1] - logo_size) // 2)
            qr_img.paste(logo, pos, mask=logo)

        # Als "Scan Me" is aangevinkt
        if add_scan_me:
            # Extra canvas maken
            padding = 40
            label_height = 50
            new_width = qr_img.size[0] + padding * 2
            new_height = qr_img.size[1] + padding * 2 + label_height
            new_img = Image.new("RGBA", (new_width, new_height), "white")
            draw = ImageDraw.Draw(new_img)

            # QR op nieuwe canvas
            new_img.paste(qr_img, (padding, padding))

            # Kader tekenen
            line_width = 5
            draw.rounded_rectangle(
                [(padding - 10, padding - 10), (new_width - padding + 10, new_height - padding - label_height + 10)],
                radius=20,
                outline="black",
                width=line_width
            )

            # "Scan Me" label tekenen
            font = ImageFont.load_default()
            text = "SCAN ME"
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            label_width = text_width + 40
            label_height_real = text_height + 20
            label_x1 = (new_width - label_width) // 2
            label_y1 = new_height - label_height_real - 10
            label_x2 = label_x1 + label_width
            label_y2 = label_y1 + label_height_real

            draw.rounded_rectangle([label_x1, label_y1, label_x2, label_y2], radius=15, outline="black", width=2)
            draw.text(
                ((new_width - text_width) // 2, label_y1 + (label_height_real - text_height) // 2),
                text, fill="black", font=font
            )

            qr_img = new_img

        # QR tonen
        st.image(qr_img)

        # Download knop
        buf = io.BytesIO()
        qr_img.save(buf, format="PNG")
        st.download_button("Download QR-code", buf.getvalue(), "qrcode.png", "image/png")
