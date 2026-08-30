#!/usr/bin/env python3
"""TimeFlow - put a text file + live clock on your GNOME desktop wallpaper."""

import argparse
import datetime
import os
import subprocess
import time

from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def font(size, bold=False):
    """Load a DejaVu font (mono for text, sans version for the bold clock)."""
    for path in FONT_PATHS:
        if not os.path.exists(path):
            continue
        if bold and "Bold" not in path:
            continue
        if not bold and "Bold" in path:
            continue
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def screen_size():
    """Primary monitor resolution via xrandr; fall back to HD."""
    try:
        out = subprocess.run(["xrandr"], capture_output=True, text=True,
                             timeout=5).stdout
        for line in out.splitlines():
            if "*" in line:                       # line of a preferred mode
                words = [w for w in line.split() if w and w[0].isdigit()
                         and "x" in w]
                if words:
                    w, h = words[0].split("x")
                    if w.isdigit() and h.isdigit():
                        return int(w), int(h)
    except Exception:
        pass
    return 1920, 1080


def read_file(path):
    """Return (status, text). status is one of ok/empty/missing."""
    if not os.path.exists(path):
        return "missing", f"[file not found] create '{path}' and it appears here"
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    if not text.strip():
        return "empty", "[file is empty] write something and save it"
    return "ok", text


def set_wallpaper(png):
    """Tell GNOME to use png as the wallpaper (light + dark picture keys)."""
    uri = "file://" + os.path.abspath(png)
    for key in ("picture-uri", "picture-uri-dark"):
        subprocess.run(["gsettings", "set", "org.gnome.desktop.background",
                        key, uri], capture_output=True, timeout=5)
    subprocess.run(["gsettings", "set", "org.gnome.desktop.background",
                    "picture-options", "scaled"], capture_output=True, timeout=5)


def wrap_text(draw, text, body_font, max_width):
    """Wrap a paragraph to fit max_width, always breaking long words."""
    lines = []
    for raw in text.splitlines():
        if not raw.strip():
            continue
        words, line = raw.split(), ""
        for word in words:
            trial = (line + " " + word).strip()
            if draw.textlength(trial, font=body_font) <= max_width:
                line = trial
            else:
                if line:
                    lines.append(line)
                while draw.textlength(word, font=body_font) > max_width:
                    for cut in range(len(word) - 1, 0, -1):
                        if draw.textlength(word[:cut], font=body_font) <= max_width:
                            lines.append(word[:cut])
                            word = word[cut:]
                            break
                line = word
        if line:
            lines.append(line)
    return lines


# ---------------------------------------------------------------------------
# wallpaper rendering
# ---------------------------------------------------------------------------

ACCENT = (124, 106, 255)     # purple accent
TEXT = (232, 236, 245)       # main text
MUTED = (150, 158, 180)      # secondary text
PANEL = (24, 28, 44)         # card background
BORDER = (56, 62, 88)
TOP = (18, 22, 34)           # gradient top
BOTTOM = (30, 36, 54)        # gradient bottom


def render(pw, ph, filename, status, text):
    """Draw the full wallpaper (clock + file content) for the given time."""
    now = datetime.datetime.now()
    pad = max(24, pw // 45)
    clock_h = int(ph * 0.24)
    top = ph - 40

    img = Image.new("RGB", (pw, ph))
    d = ImageDraw.Draw(img)

    # background gradient
    for y in range(ph):
        t = y / ph
        color = tuple(int(TOP[i] + (BOTTOM[i] - TOP[i]) * t) for i in range(3))
        d.line([(0, y), (pw, y)], fill=color)

    # rounded cards: clock on top, content below
    def card(y, height):
        d.rounded_rectangle([pad, y, pw - pad, y + height], radius=20,
                            fill=PANEL, outline=BORDER)

    card(pad, clock_h)
    card(pad + clock_h + 18, top - (pad + clock_h + 18))

    # ---- clock ----
    clock_font = font(max(30, clock_h // 3), bold=True)
    date_font = font(max(13, pw // 85))
    clock_str = now.strftime("%H:%M:%S")
    date_str = now.strftime("%A, %d %B %Y")
    cx, cy = pw // 2, pad + clock_h // 2
    d.text((cx, cy - 14), clock_str, font=clock_font, fill=TEXT, anchor="mm")
    d.text((cx, cy + 42), date_str, font=date_font, fill=MUTED, anchor="mm")

    # ---- content ----
    body_font = font(max(15, int(min(pw, ph) * 0.021)))
    head_font = font(max(15, pw // 80))
    body_w = pw - 2 * pad - 30
    y = pad + clock_h + 18 + 20
    line_h = int(body_font.getbbox("Hg")[3] * 1.45)
    max_lines = (top - 34 - y) // line_h

    d.rectangle([pad + 12, y, pad + 18, y + 16], fill=ACCENT)  # accent bar
    d.text((pad + 28, y - 8), filename.upper(), font=head_font, fill=TEXT)

    status_tag = {"ok": "SYNCED", "empty": "EMPTY", "missing": "MISSING"}[status]
    tag_w = d.textlength(status_tag, font=body_font) + 28
    d.rounded_rectangle([pw - pad - tag_w, y - 8, pw - pad - 4, y + 18],
                        radius=13, outline=ACCENT)
    d.text((pw - pad - tag_w + 14, y - 2), status_tag, font=body_font,
           fill=ACCENT)

    y += line_h + 12
    if status == "missing":
        d.text((pad + 12, y), "NOTHING TO SHOW", font=head_font, fill=ACCENT)
        d.text((pad + 12, y + line_h), text, font=body_font, fill=MUTED)
        return img
    if status == "empty":
        d.text((pad + 12, y), "EMPTY FILE", font=head_font, fill=ACCENT)
        d.text((pad + 12, y + line_h), text, font=body_font, fill=MUTED)
        return img

    lines = wrap_text(d, text, body_font, body_w)
    if len(lines) > max_lines:
        hidden = len(lines) - max_lines
        lines = lines[:max_lines]
        lines.append(f"... {hidden} more line(s) hidden")

    for i, line in enumerate(lines):
        color = ACCENT if line.startswith("#") else TEXT
        d.text((pad + 12, y + i * line_h), line, font=body_font, fill=color)

    # footer
    d.text((pad, top + 14), "TIMEFLOW  |  updates automatically on edit",
           font=font(max(12, pw // 100)), fill=MUTED)
    d.text((pw - pad, top + 14), now.strftime("%Y-%m-%d"), anchor="ra",
           font=font(max(12, pw // 100)), fill=MUTED)
    return img


# ---------------------------------------------------------------------------
# main loop
# ---------------------------------------------------------------------------

def clean_old_frames(current):
    """Remove earlier per-frame copies, keeping only the latest one."""
    for name in os.listdir(SCRIPT_DIR):
        if name.startswith("timeflow_wallpaper_") and name.endswith(".png"):
            if os.path.join(SCRIPT_DIR, name) != current:
                try:
                    os.unlink(os.path.join(SCRIPT_DIR, name))
                except OSError:
                    pass


def main():
    ap = argparse.ArgumentParser(description="Live text + clock wallpaper (GNOME)")
    ap.add_argument("-f", "--file", default="notes.txt",
                    help="text file to display on the wallpaper")
    args = ap.parse_args()

    pw, ph = screen_size()
    print(f"TimeFlow started - watching '{args.file}' "
          f"({pw}x{ph}), Ctrl+C to stop", flush=True)

    last_text = None
    seq = 0
    while True:
        try:
            status, text = read_file(args.file)
        except OSError as exc:
            status, text = "missing", str(exc)

        changed = text != last_text
        last_text = text
        if changed:
            print(f"  [{datetime.datetime.now():%H:%M:%S}] "
                  f"{status.upper():7s} {os.path.basename(args.file)}",
                  flush=True)

        frame = render(pw, ph, os.path.basename(args.file), status, text)

        # save under a fresh name every tick so GNOME always registers the
        # change, then keep a stable copy for convenience
        seq += 1
        live = os.path.join(SCRIPT_DIR, f"timeflow_wallpaper_{seq:05d}.png")
        frame.save(live)
        frame.save(os.path.join(SCRIPT_DIR, "timeflow_wallpaper.png"))
        set_wallpaper(live)
        clean_old_frames(live)

        time.sleep(1.0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nstopped - wallpaper stays as-is")