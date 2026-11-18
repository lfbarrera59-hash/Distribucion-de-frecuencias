import os
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cv2

def make_qr_card():
    # Dimensions: 1080 x 1440 px (high-res standard 3:4 portrait poster)
    W, H = 1080, 1440
    
    # Target URL
    url = "https://lfbarrera59-hash.github.io/Distribucion-de-frecuencias/"
    
    # Base canvas
    base = Image.new("RGBA", (W, H), (247, 249, 252, 255))
    draw = ImageDraw.Draw(base)
    
    # 1. Header gradient matching Quarto document header:
    # Rich deep blue #1e3a8a at top transitioning smoothly into pastel blue #98b6ed
    banner_height = 420
    for y in range(banner_height):
        ratio = y / banner_height
        r = int(24 * (1 - ratio) + 152 * ratio)
        g = int(50 * (1 - ratio) + 182 * ratio)
        b = int(130 * (1 - ratio) + 237 * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))
        
    # Fonts
    font_dir = "C:/Windows/Fonts/"
    font_badge = ImageFont.truetype(os.path.join(font_dir, "segoeuib.ttf"), 19)
    font_title = ImageFont.truetype(os.path.join(font_dir, "segoeuib.ttf"), 52)
    font_sub = ImageFont.truetype(os.path.join(font_dir, "segoeui.ttf"), 26)
    font_scan = ImageFont.truetype(os.path.join(font_dir, "segoeuib.ttf"), 30)
    font_scan_sub = ImageFont.truetype(os.path.join(font_dir, "segoeui.ttf"), 20)
    font_url = ImageFont.truetype(os.path.join(font_dir, "segoeuib.ttf"), 21)
    font_sec_title = ImageFont.truetype(os.path.join(font_dir, "segoeuib.ttf"), 20)
    font_authors = ImageFont.truetype(os.path.join(font_dir, "segoeui.ttf"), 20)
    font_footer = ImageFont.truetype(os.path.join(font_dir, "segoeui.ttf"), 16)

    # 2. ESAP Institution Pill / Badge at top
    badge_text = "ESCUELA SUPERIOR DE ADMINISTRACIÓN PÚBLICA • ESAP"
    b_bbox = font_badge.getbbox(badge_text)
    bw = b_bbox[2] - b_bbox[0]
    pill_w = bw + 44
    pill_h = 40
    pill_x = (W - pill_w) // 2
    pill_y = 48
    draw.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + pill_h], radius=20, fill=(255, 255, 255, 45), outline=(255, 255, 255, 95), width=1)
    draw.text((pill_x + 22, pill_y + 8), badge_text, fill=(255, 255, 255, 250), font=font_badge)

    # 3. Main Document Title
    title = "Distribución de Frecuencias"
    t_bbox = font_title.getbbox(title)
    draw.text(((W - (t_bbox[2] - t_bbox[0])) // 2, 114), title, fill=(255, 255, 255, 255), font=font_title)

    # Subtitle
    sub = "TALLER 2 • Tablas y Gráficas Estadísticas"
    s_bbox = font_sub.getbbox(sub)
    draw.text(((W - (s_bbox[2] - s_bbox[0])) // 2, 184), sub, fill=(235, 245, 255, 240), font=font_sub)

    # 4. Central Card with Soft Ambient Shadow
    card_w, card_h = 760, 800
    card_x = (W - card_w) // 2
    card_y = 250
    
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.rounded_rectangle([card_x, card_y + 12, card_x + card_w, card_y + card_h + 16], radius=34, fill=(15, 23, 42, 35))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    base = Image.alpha_composite(base, shadow)
    
    draw = ImageDraw.Draw(base)
    # White card container
    draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=32, fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=2)
    
    # Place ESAP Logo elegantly at the top of the card
    if os.path.exists("Logo_Esap.png"):
        try:
            esap_logo = Image.open("Logo_Esap.png").convert("RGBA")
            esap_logo.thumbnail((120, 65), Image.Resampling.LANCZOS)
            el_w, el_h = esap_logo.size
            base.paste(esap_logo, (card_x + (card_w - el_w) // 2, card_y + 24), esap_logo)
        except Exception as e:
            print("Logo error:", e)

    # Card Call To Action header
    scan_text = "Escanea para ver el informe interactivo"
    st_bbox = font_scan.getbbox(scan_text)
    draw.text((card_x + (card_w - (st_bbox[2] - st_bbox[0])) // 2, card_y + 95), scan_text, fill=(15, 23, 42, 255), font=font_scan)

    scan_sub = "Tablas dinámicas, filtros y gráficos de 200 registros de servidores públicos"
    ss_bbox = font_scan_sub.getbbox(scan_sub)
    draw.text((card_x + (card_w - (ss_bbox[2] - ss_bbox[0])) // 2, card_y + 138), scan_sub, fill=(100, 116, 139, 255), font=font_scan_sub)

    # 5. Generate high precision QR Code (Clean & 100% accessible to every scanner)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=12,
        border=3,
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#0F172A", back_color="white").convert("RGBA")
    
    qr_w, qr_h = qr_img.size
    qr_x = card_x + (card_w - qr_w) // 2
    qr_y = card_y + 180
    
    # Decorative QR frame container
    draw.rounded_rectangle([qr_x - 10, qr_y - 10, qr_x + qr_w + 10, qr_y + qr_h + 10], radius=18, fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=2)
    base.paste(qr_img, (qr_x, qr_y), qr_img)

    # 6. Clickable / readable URL bar at bottom of card
    url_box_w = card_w - 70
    url_box_h = 56
    ub_x = card_x + 35
    ub_y = card_y + card_h - 85
    draw.rounded_rectangle([ub_x, ub_y, ub_x + url_box_w, ub_y + url_box_h], radius=16, fill=(241, 245, 249, 255), outline=(203, 213, 225, 255), width=1)
    
    url_display = "https://lfbarrera59-hash.github.io/Distribucion-de-frecuencias/"
    ud_bbox = font_url.getbbox(url_display)
    draw.text((ub_x + (url_box_w - (ud_bbox[2] - ud_bbox[0])) // 2, ub_y + 15), url_display, fill=(37, 99, 235, 255), font=font_url)

    # 7. Authors Card Section
    authors_y = card_y + card_h + 35
    team_title = "EQUIPO DE AUTORES / INVESTIGADORES"
    tt_bbox = font_sec_title.getbbox(team_title)
    draw.text(((W - (tt_bbox[2] - tt_bbox[0])) // 2, authors_y), team_title, fill=(71, 85, 105, 255), font=font_sec_title)

    # 4 Authors neatly placed
    col1_x = 180
    col2_x = 580
    draw.text((col1_x, authors_y + 36), "• Luis Felipe Barrera Gómez", fill=(30, 41, 59, 255), font=font_authors)
    draw.text((col1_x, authors_y + 70), "• Oscar Iván Guerrero Contreras", fill=(30, 41, 59, 255), font=font_authors)
    draw.text((col2_x, authors_y + 36), "• Diana Lizeth Rubio Bermejo", fill=(30, 41, 59, 255), font=font_authors)
    draw.text((col2_x, authors_y + 70), "• Luis Alberto Varón Trujillo", fill=(30, 41, 59, 255), font=font_authors)

    # 8. Bottom Footer details
    footer_text = "Publicación Interactiva en Web • Quarto Document • GitHub Pages"
    ft_bbox = font_footer.getbbox(footer_text)
    draw.text(((W - (ft_bbox[2] - ft_bbox[0])) // 2, H - 45), footer_text, fill=(148, 163, 184, 255), font=font_footer)

    # Save outputs
    output_png = "codigo_qr_distribucion_frecuencias.png"
    base.convert("RGB").save(output_png, "PNG", quality=95)
    print("Poster saved successfully to", output_png)
    
    # Standalone QR
    qr_standalone = "qr_codigo_solo.png"
    qr_clean = qr.make_image(fill_color="#0F172A", back_color="white").convert("RGBA")
    qr_clean.save(qr_standalone, "PNG")
    print("Standalone QR saved to", qr_standalone)

    # Verify detection with OpenCV
    img_cv = cv2.imread(output_png)
    detector = cv2.QRCodeDetector()
    val, points, _ = detector.detectAndDecode(img_cv)
    print("OpenCV decode test on poster image:", val)

if __name__ == "__main__":
    make_qr_card()
