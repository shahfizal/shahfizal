from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(r"C:\Users\Dell\Desktop\CLAUDE\S.A.M")
SRC_AVATAR = ROOT / "Shahfizal_Zainuddin.png"
SRC_BANNER = Path(r"C:\Users\Dell\Desktop\CLAUDE\studio\documentation\agentic-marketing\assets\skill-library.png")
OUT = ROOT / "github-profile" / "assets"
OUT.mkdir(parents=True, exist_ok=True)

FONT_DIR = Path.home() / "AppData" / "Local" / "Microsoft" / "Windows" / "Fonts"
BOLD = FONT_DIR / "Montserrat-Bold.ttf"
SEMI = FONT_DIR / "Montserrat-SemiBold.ttf"
REG = FONT_DIR / "Montserrat-Regular.ttf"

CREAM = (246, 240, 228)
GOLD = (201, 155, 90)
MUTED = (214, 204, 188)


def font(path, size):
    return ImageFont.truetype(str(path), size)


def tracked(draw, xy, text, fnt, fill, tracking=0):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill, anchor="ls")
        x += draw.textlength(ch, font=fnt) + tracking


def make_avatar():
    im = Image.open(SRC_AVATAR).convert("RGB")
    # The source is already square and centred.
    for size in (460, 800):
        out = im.resize((size, size), Image.LANCZOS)
        out.save(OUT / f"portrait-{size}.jpg", quality=92, optimize=True)
        out.save(OUT / f"portrait-{size}.png", optimize=True)
    print("avatar", im.size)


def make_banner():
    im = Image.open(SRC_BANNER).convert("RGB")
    w, h = im.size
    target_ratio = 3.0
    crop_h = int(w / target_ratio)
    top = max(0, (h - crop_h) // 2)
    im = im.crop((0, top, w, top + crop_h)).resize((1500, 500), Image.LANCZOS)

    # Darken the left side so the typography reads over the cards.
    shade = Image.new("L", (1, 500), 0)
    for y in range(500):
        shade.putpixel((0, y), 0)
    gradient = Image.new("L", (1500, 1), 0)
    for x in range(1500):
        alpha = 210 if x < 650 else max(0, int(210 * (1 - (x - 650) / 600)))
        gradient.putpixel((x, 0), alpha)
    mask = gradient.resize((1500, 500))
    black = Image.new("RGB", (1500, 500), (8, 7, 6))
    im = Image.composite(black, im, mask)

    draw = ImageDraw.Draw(im)
    tracked(draw, (72, 148), "SHAHFIZAL", font(BOLD, 58), CREAM, 2)
    tracked(draw, (72, 212), "ZAINUDDIN", font(BOLD, 58), CREAM, 2)
    draw.text((74, 286), "Agentic marketing for Malaysian startups", font=font(REG, 27), fill=CREAM, anchor="ls")
    draw.line((74, 330, 194, 330), fill=GOLD, width=4)
    draw.text((74, 372), "OpenCode  ·  DeepSeek  ·  Evidence, not hype", font=font(SEMI, 18), fill=GOLD, anchor="ls")
    im.save(OUT / "banner.png", optimize=True)
    print("banner", im.size)


if __name__ == "__main__":
    make_avatar()
    make_banner()
