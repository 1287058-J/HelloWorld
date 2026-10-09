import html
import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hello World Motion Lab", page_icon="✨", layout="wide")

st.title("Hello World Motion Lab")
st.caption("A tiny app for experimenting with text, fonts, backgrounds, and motion.")

with st.sidebar:
    st.header("Controls")
    name = st.text_input("Enter your name or message", value="Hello World", max_chars=80)
    font_family = st.selectbox(
        "Font type",
        ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana", "Trebuchet MS", "Impact", "monospace", "serif", "sans-serif"],
    )
    font_size = st.slider("Font size", min_value=20, max_value=100, value=48, step=2)
    background = st.selectbox(
        "Background",
        ["Light", "Dark", "Ocean", "Sunset", "Forest", "Lavender"],
    )
    name_mode = st.selectbox("Name display mode", ["Centered", "Ticker Tape", "Repeated"])
    effect = st.selectbox(
        "Dynamic action",
        ["None", "Rain", "Snow", "Hail", "Wind", "Confetti", "Tornado"],
    )
    effect_speed = st.select_slider(
        "Animation speed",
        options=["Slow", "Normal", "Fast"],
        value="Normal",
        help="The animation loops continuously inside the preview.",
    )

bg_styles = {
    "Light": ("#f8fafc", "#172033"),
    "Dark": ("#10131c", "#f8fafc"),
    "Ocean": ("linear-gradient(135deg, #0f766e, #164e63, #172554)", "#ffffff"),
    "Sunset": ("linear-gradient(135deg, #7c2d12, #db2777, #4c1d95)", "#ffffff"),
    "Forest": ("linear-gradient(135deg, #052e16, #166534, #365314)", "#f0fdf4"),
    "Lavender": ("linear-gradient(135deg, #ede9fe, #c4b5fd, #fbcfe8)", "#312e81"),
}
bg, text_color = bg_styles[background]
speed_seconds = {"Slow": 2.4, "Normal": 1.35, "Fast": 0.7}[effect_speed]

safe_name = html.escape(name or "Hello World")
safe_font = font_family.replace("'", "").replace('"', "")
if name_mode == "Repeated":
    name_markup = "<div class='repeated'>" + "<br>".join([safe_name] * 5) + "</div>"
elif name_mode == "Ticker Tape":
    name_markup = f"<div class='ticker'><span>{safe_name}&nbsp;&nbsp;&nbsp; ✦ &nbsp;&nbsp;&nbsp;{safe_name}&nbsp;&nbsp;&nbsp; ✦ &nbsp;&nbsp;&nbsp;</span></div>"
else:
    name_markup = f"<div class='center-name'>{safe_name}</div>"

# Build decorative particles. CSS moves these forever; no Streamlit rerun loop is needed.
random.seed(23)
particles = []
symbols = {
    "Rain": ["💧", "│", "╱"],
    "Snow": ["❄", "✳", "✦", "❅"],
    "Hail": ["●", "○", "🧊"],
    "Wind": ["〰", "﹏", "➝", "༄"],
    "Confetti": ["✦", "●", "■", "▲", "🎉", "✧"],
    "Tornado": ["〰", "∿", "༄", "🌀"],
}
if effect != "None":
    for i in range(42):
        symbol = random.choice(symbols[effect])
        left = random.randint(1, 98)
        delay = random.uniform(-8, 0)
        duration = speed_seconds * random.uniform(2.0, 5.0)
        size = random.randint(14, 30) if effect in ("Snow", "Confetti", "Tornado") else random.randint(12, 23)
        drift = random.randint(-90, 90)
        particles.append(
            f"<span class='particle p-{effect.lower()}' "
            f"style='left:{left}%; animation-delay:{delay:.2f}s; animation-duration:{duration:.2f}s; "
            f"font-size:{size}px; --drift:{drift}px;'>{html.escape(symbol)}</span>"
        )
particles_html = "".join(particles)

html_doc = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; }}
.stage {{
  position: relative; height: 610px; width: 100%; overflow: hidden;
  background: {bg}; color: {text_color}; border-radius: 18px;
  font-family: '{safe_font}', sans-serif;
}}
.effect-layer {{ position:absolute; inset:0; overflow:hidden; pointer-events:none; }}
.particle {{
  position:absolute; top:-12%; opacity:.8; user-select:none;
  animation-name: fall; animation-timing-function: linear; animation-iteration-count: infinite;
  text-shadow: 0 1px 5px rgba(0,0,0,.12);
}}
@keyframes fall {{
  0% {{ transform: translate3d(0,-10%,0) rotate(0deg); }}
  100% {{ transform: translate3d(var(--drift),700px,0) rotate(360deg); }}
}}
.p-snow {{ animation-name: snow; }}
@keyframes snow {{
  0% {{ transform:translate3d(0,-20px,0) rotate(0); }}
  50% {{ transform:translate3d(calc(var(--drift) * .5),320px,0) rotate(180deg); }}
  100% {{ transform:translate3d(var(--drift),700px,0) rotate(360deg); }}
}}
.p-hail {{ animation-name: hail; }}
@keyframes hail {{
  0% {{ transform:translate3d(0,-20px,0); }}
  85% {{ transform:translate3d(var(--drift),610px,0); }}
  90% {{ transform:translate3d(var(--drift),580px,0); }}
  100% {{ transform:translate3d(var(--drift),700px,0); }}
}}
.p-wind {{ animation-name: gust; animation-timing-function:ease-in-out; }}
@keyframes gust {{
  0% {{ transform:translate3d(-160px, 80px, 0) rotate(0); opacity:0; }}
  20% {{ opacity:.9; }}
  80% {{ opacity:.8; }}
  100% {{ transform:translate3d(110vw, 280px, 0) rotate(20deg); opacity:0; }}
}}
.p-confetti {{ animation-name: confetti; }}
@keyframes confetti {{
  0% {{ transform:translate3d(0,-30px,0) rotate(0); }}
  100% {{ transform:translate3d(var(--drift),700px,0) rotate(900deg); }}
}}
.p-tornado {{ animation-name: swirl; animation-timing-function:linear; }}
@keyframes swirl {{
  0% {{ transform:translate3d(-90px,-20px,0) rotate(0) scale(.7); opacity:0; }}
  20% {{ opacity:.9; }}
  50% {{ transform:translate3d(0,300px,0) rotate(540deg) scale(1.2); }}
  100% {{ transform:translate3d(90px,700px,0) rotate(1080deg) scale(.6); opacity:0; }}
}}
.name-layer {{
  position:absolute; z-index:2; inset:0; display:flex; align-items:center;
  justify-content:center; padding:32px; font-size:{font_size}px; font-weight:700;
  line-height:1.25; text-align:center; overflow:hidden; overflow-wrap:anywhere;
  text-shadow: 0 2px 14px rgba(0,0,0,.14);
}}
.center-name {{ max-width:100%; }}
.repeated {{ width:100%; }}
.ticker {{ width:100%; white-space:nowrap; overflow:hidden; }}
.ticker span {{ display:inline-block; padding-left:100%; animation: marquee 12s linear infinite; }}
@keyframes marquee {{ 0% {{ transform:translateX(0); }} 100% {{ transform:translateX(-100%); }} }}
.hint {{
  position:absolute; z-index:3; left:14px; bottom:12px; font:12px/1.3 Arial,sans-serif;
  opacity:.72; letter-spacing:.04em;
}}
</style>
</head>
<body>
  <div class="stage">
    <div class="effect-layer">{particles_html}</div>
    <div class="name-layer">{name_markup}</div>
    <div class="hint">HELLO WORLD MOTION LAB · {html.escape(effect.upper())}</div>
  </div>
</body>
</html>"""

components.html(html_doc, height=630, scrolling=False)

st.info("Tip: change the controls in the sidebar to explore how each setting changes the preview. The effects animate continuously in the preview without repeatedly rerunning the Streamlit app.")
