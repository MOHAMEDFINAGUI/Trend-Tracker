# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
import time as _time
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="SET DIRECTION",
    page_icon=":dart:",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── منع النوم — ping كل 50 ثانية ──
st_autorefresh(interval=50_000, key="ping")

# ── حالة الجلسة ──
if "result"   not in st.session_state: st.session_state.result   = None
if "last_run" not in st.session_state: st.session_state.last_run = 0
if "prev_dir" not in st.session_state: st.session_state.prev_dir = None

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Cairo:wght@400;600;700;900&display=swap');

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stHeader"],
[data-testid="manage-app-button"],
.stDeployButton,
.viewerBadge_container__1QSob,
.viewerBadge_link__1S137,
.st-emotion-cache-1dp5vir,
.st-emotion-cache-zq5wmm,
section[data-testid="stSidebar"],
[data-testid="collapsedControl"] { display:none !important; }

:root {
  --gold:#d4a843; --gl:#f5d060; --gd:#8b6914;
  --green:#00e676; --red:#ff1744; --amber:#ffab00; --blue:#448aff;
  --bg:#020407; --glass:rgba(255,255,255,0.033); --bdr:rgba(255,255,255,0.07);
  --txt:#e0e0e0; --dim:#484848;
}

html,body { background:var(--bg) !important; overflow-x:hidden; }
[data-testid="stAppViewContainer"] { background:var(--bg) !important; min-height:100vh; position:relative; }
[data-testid="stMain"],[data-testid="stMain"]>div { background:transparent !important; }

[data-testid="stAppViewContainer"]::before {
  content:'TREND TRACKER  TREND TRACKER  TREND TRACKER  TREND TRACKER  TREND TRACKER  TREND TRACKER  TREND TRACKER  TREND TRACKER  TREND TRACKER  TREND TRACKER  TREND TRACKER  TREND TRACKER  TREND TRACKER  TREND TRACKER  TREND TRACKER  TREND TRACKER  TREND TRACKER  TREND TRACKER  TREND TRACKER  TREND TRACKER  ';
  position:fixed; inset:-150px; z-index:0; pointer-events:none;
  font-family:'Orbitron',monospace; font-size:1.3rem; font-weight:900;
  letter-spacing:6px; word-spacing:18px; line-height:3.5;
  color:rgba(212,168,67,0.032); text-transform:uppercase;
  transform:rotate(-22deg); width:220%; overflow:hidden;
}

[data-testid="stAppViewContainer"]::after {
  content:''; position:fixed; inset:0; z-index:0; pointer-events:none;
  background-image:
    radial-gradient(1px 1px at  7% 12%,rgba(255,255,255,.85)0%,transparent 100%),
    radial-gradient(1px 1px at 21% 37%,rgba(255,255,255,.50)0%,transparent 100%),
    radial-gradient(1px 1px at 36% 66%,rgba(255,255,255,.70)0%,transparent 100%),
    radial-gradient(1px 1px at 52% 17%,rgba(255,255,255,.55)0%,transparent 100%),
    radial-gradient(1px 1px at 67% 51%,rgba(255,255,255,.80)0%,transparent 100%),
    radial-gradient(1px 1px at 82% 27%,rgba(255,255,255,.45)0%,transparent 100%),
    radial-gradient(1px 1px at 90% 76%,rgba(255,255,255,.65)0%,transparent 100%),
    radial-gradient(1px 1px at 15% 87%,rgba(255,255,255,.60)0%,transparent 100%),
    radial-gradient(1px 1px at 43% 43%,rgba(255,255,255,.50)0%,transparent 100%),
    radial-gradient(1.5px 1.5px at 29% 56%,rgba(212,168,67,.60)0%,transparent 100%),
    radial-gradient(2px 2px at  5% 47%,rgba(255,255,255,.90)0%,transparent 100%),
    radial-gradient(2px 2px at 93% 57%,rgba(255,255,255,.80)0%,transparent 100%),
    radial-gradient(1px 1px at 78% 88%,rgba(255,255,255,.50)0%,transparent 100%);
  animation:twinkle 9s ease-in-out infinite alternate;
}
@keyframes twinkle{0%{opacity:.35;}50%{opacity:1.0;}100%{opacity:.25;}}

.block-container { position:relative; z-index:1; padding:0 1rem 4rem !important; max-width:460px !important; margin:0 auto !important; }

.hdr { text-align:center; padding:2.5rem 0 1.4rem; user-select:none; position:relative; z-index:2; }
.hdr-icon { font-size:clamp(2.8rem,12vw,4rem); display:block; margin-bottom:.45rem; animation:flt 3.5s ease-in-out infinite; filter:drop-shadow(0 0 22px rgba(212,168,67,.6)); }
@keyframes flt{0%,100%{transform:translateY(0) rotate(-2deg);}50%{transform:translateY(-9px) rotate(2deg);}}
.hdr-title { font-family:'Orbitron',monospace; font-size:clamp(1.9rem,8.5vw,2.7rem); font-weight:900; letter-spacing:clamp(4px,2.5vw,8px); background:linear-gradient(135deg,var(--gd)0%,var(--gl)38%,var(--gold)68%,var(--gd)100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; filter:drop-shadow(0 0 24px rgba(212,168,67,.65)); line-height:1; margin-bottom:.3rem; }
.hdr-sub { font-family:'Orbitron',monospace; font-size:clamp(.6rem,2.8vw,.75rem); color:rgba(212,168,67,.32); letter-spacing:4px; }

.timebar { display:flex; justify-content:space-between; align-items:center; padding:.48rem .9rem; background:rgba(212,168,67,.038); border:1px solid rgba(212,168,67,.11); border-radius:10px; margin-bottom:.85rem; position:relative; z-index:2; }
.tb-label { font-family:'Cairo',sans-serif; font-size:.74rem; color:var(--dim); }
.tb-clock { font-family:'Orbitron',monospace; font-size:.70rem; color:rgba(212,168,67,.48); letter-spacing:2px; }
.tb-dot   { width:6px;height:6px; background:var(--green); border-radius:50%; box-shadow:0 0 6px var(--green); animation:pdot 1.5s ease-in-out infinite; }
@keyframes pdot{0%,100%{opacity:1;transform:scale(1);}50%{opacity:.3;transform:scale(.6);}}

div.stButton { padding:0 !important; margin:0 !important; }
div.stButton > button { width:100% !important; min-height:62px !important; background:linear-gradient(135deg,var(--gd),var(--gl)50%,var(--gold)) !important; border:none !important; border-radius:16px !important; color:#060400 !important; font-family:'Orbitron',monospace !important; font-size:clamp(.82rem,3.8vw,1.05rem) !important; font-weight:900 !important; letter-spacing:2px !important; cursor:pointer !important; transition:transform .2s ease !important; animation:gbtn 3s ease-in-out infinite !important; position:relative; z-index:2; }
@keyframes gbtn{0%,100%{box-shadow:0 4px 22px rgba(212,168,67,.42);}50%{box-shadow:0 6px 34px rgba(212,168,67,.68);}}
div.stButton > button:hover  { transform:translateY(-2px) !important; }
div.stButton > button:active { transform:translateY(1px) !important; }

.gc { background:var(--glass); border:1px solid var(--bdr); border-radius:20px; padding:1.5rem 1.3rem; backdrop-filter:blur(24px); -webkit-backdrop-filter:blur(24px); box-shadow:0 8px 32px rgba(0,0,0,.55); margin-bottom:1rem; position:relative; z-index:2; }

.closed-card { background:rgba(68,138,255,.055); border:1.5px solid rgba(68,138,255,.28); border-radius:20px; padding:2.4rem 1.5rem; text-align:center; margin-bottom:1rem; position:relative; z-index:2; }
.closed-icon  { font-size:clamp(3rem,13vw,4.5rem); display:block; margin-bottom:.5rem; animation:beat 2s ease-in-out infinite; }
.closed-title { font-family:'Orbitron',monospace; font-size:clamp(1.2rem,5.5vw,1.7rem); font-weight:900; letter-spacing:3px; color:var(--blue); display:block; margin-bottom:.4rem; }
.closed-desc  { font-family:'Cairo',sans-serif; font-size:1rem; color:#666; margin-bottom:.9rem; }
@keyframes beat{0%,100%{transform:scale(1);}50%{transform:scale(1.08);}}
.csched { background:rgba(255,255,255,.028); border:1px solid rgba(255,255,255,.06); border-radius:12px; padding:.85rem; }
.cs-row { display:flex; justify-content:space-between; align-items:center; padding:.4rem 0; border-bottom:1px solid rgba(255,255,255,.04); }
.cs-row:last-child { border-bottom:none; }
.cs-day  { font-family:'Cairo',sans-serif; font-size:.88rem; color:#666; }
.cs-time { font-family:'Orbitron',monospace; font-size:.7rem; color:var(--gold); }
.badge-open  { background:rgba(0,230,118,.14); color:var(--green); font-family:'Orbitron',monospace; font-size:.56rem; padding:.16rem .44rem; border-radius:6px; }
.badge-close { background:rgba(255,23,68,.11);  color:var(--red);   font-family:'Orbitron',monospace; font-size:.56rem; padding:.16rem .44rem; border-radius:6px; }

.rc { border-radius:20px; padding:2rem 1.2rem 1.6rem; text-align:center; margin-bottom:1rem; position:relative; z-index:2; }
.rc.up   { background:rgba(0,230,118,.055); border:1.5px solid rgba(0,230,118,.26); box-shadow:0 0 55px rgba(0,230,118,.07); }
.rc.down { background:rgba(255,23,68,.055);  border:1.5px solid rgba(255,23,68,.26);  box-shadow:0 0 55px rgba(255,23,68,.07); }
.rc.wait { background:rgba(255,171,0,.055);  border:1.5px solid rgba(255,171,0,.26);  box-shadow:0 0 55px rgba(255,171,0,.07); }
.rc-icon { font-size:clamp(3.2rem,13vw,4.8rem); display:block; margin-bottom:.35rem; animation:beat 2s ease-in-out infinite; }
.rc-word { font-family:'Orbitron',monospace; font-size:clamp(1.9rem,9.5vw,2.8rem); font-weight:900; letter-spacing:5px; display:block; margin-bottom:.35rem; }
.rc-word.up   { color:var(--green); filter:drop-shadow(0 0 18px rgba(0,230,118,.80)); }
.rc-word.down { color:var(--red);   filter:drop-shadow(0 0 18px rgba(255,23,68,.80)); }
.rc-word.wait { color:var(--amber); filter:drop-shadow(0 0 18px rgba(255,171,0,.80)); }
.rc-desc { font-family:'Cairo',sans-serif; font-size:1rem; color:#666; margin-bottom:.6rem; }
.rc-time { font-family:'Orbitron',monospace; font-size:.58rem; letter-spacing:2px; color:#2e2e2e; }

.flg { display:grid; grid-template-columns:1fr 1fr 1fr; gap:.5rem; }
.flc { border-radius:11px; padding:.6rem .35rem; text-align:center; border:1px solid; }
.flc.ok   { background:rgba(0,230,118,.065); border-color:rgba(0,230,118,.28); }
.flc.fail { background:rgba(255,23,68,.065);  border-color:rgba(255,23,68,.23); }
.fli { font-size:.9rem; display:block; margin-bottom:.18rem; }
.fll { font-family:'Orbitron',monospace; font-size:.48rem; letter-spacing:1px; color:var(--dim); text-transform:uppercase; display:block; }

.pr  { display:flex; justify-content:space-between; align-items:center; margin-bottom:.85rem; padding-bottom:.85rem; border-bottom:1px solid var(--bdr); }
.pl  { font-family:'Cairo',sans-serif; font-size:.95rem; color:var(--dim); }
.pv  { font-family:'Orbitron',monospace; font-size:1.25rem; font-weight:700; color:var(--gold); filter:drop-shadow(0 0 8px rgba(212,168,67,.5)); }
.ig  { display:grid; grid-template-columns:1fr 1fr; gap:.6rem; margin-bottom:.9rem; }
.ic  { background:rgba(255,255,255,.022); border:1px solid rgba(255,255,255,.055); border-radius:12px; padding:.8rem .65rem; text-align:center; }
.il  { font-family:'Orbitron',monospace; font-size:.54rem; letter-spacing:2px; color:var(--dim); margin-bottom:.32rem; text-transform:uppercase; display:block; }
.iv  { font-family:'Orbitron',monospace; font-size:.9rem; font-weight:700; color:var(--txt); }
.iv.gold { color:var(--gold); filter:drop-shadow(0 0 6px rgba(212,168,67,.48)); }
.bh  { display:flex; justify-content:space-between; align-items:baseline; margin-bottom:.4rem; }
.bl  { font-family:'Cairo',sans-serif; font-size:.78rem; color:var(--dim); letter-spacing:2px; }
.bp  { font-family:'Orbitron',monospace; font-size:1.15rem; font-weight:700; }
.bt  { background:rgba(255,255,255,.05); border-radius:50px; height:9px; overflow:hidden; border:1px solid rgba(255,255,255,.065); }
.bf  { height:100%; border-radius:50px; position:relative; }
.bf::after { content:''; position:absolute; right:0;top:0; width:14px;height:100%; background:rgba(255,255,255,.32); border-radius:50px; filter:blur(4px); }

[data-testid="stSpinner"] p { font-family:'Cairo',sans-serif !important; color:#555 !important; }
.sig { text-align:center; padding:2.2rem 0 .5rem; font-family:'Orbitron',monospace; font-size:.52rem; letter-spacing:3px; color:#1e1e1e; text-transform:uppercase; position:relative; z-index:2; }
.sig::before { content:''; display:block; width:38px;height:1px; background:linear-gradient(90deg,transparent,#262626,transparent); margin:0 auto .9rem; }

@media(max-width:400px){.block-container{padding:0 .55rem 3rem !important;}.gc{padding:1.1rem .8rem;}}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
def is_market_open() -> bool:
    now = datetime.utcnow()
    wd  = now.weekday()
    if wd == 5: return False
    if wd == 6: return False
    if wd == 4 and now.hour >= 23: return False
    return True


@st.cache_data(ttl=55, show_spinner=False)
def load_gold() -> pd.DataFrame:
    try:
        df = yf.download("GC=F", period="5d", interval="5m",
                         progress=False, auto_adjust=True)
        if df.empty:
            return pd.DataFrame()
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)
        return df[["Open", "High", "Low", "Close", "Volume"]].dropna()
    except Exception:
        return pd.DataFrame()


def _ema(s, n):
    return s.ewm(span=n, adjust=False).mean()

def _rsi(s, n=14):
    d  = s.diff().dropna()
    g  = d.clip(lower=0).ewm(span=n, adjust=False).mean()
    lo = (-d.clip(upper=0)).ewm(span=n, adjust=False).mean()
    return round(float((100 - 100 / (1 + g / lo.replace(0, np.nan))).iloc[-1]), 1)

def _atr(df, n=14):
    h, l, c = df["High"], df["Low"], df["Close"]
    tr = pd.concat([(h-l), (h-c.shift()).abs(), (l-c.shift()).abs()], axis=1).max(axis=1)
    return round(float(tr.ewm(span=n, adjust=False).mean().iloc[-1]), 2)

def _macd(s):
    m = _ema(s, 12) - _ema(s, 26)
    return float(m.iloc[-1]), float(_ema(m, 9).iloc[-1])

def analyze(df: pd.DataFrame) -> dict:
    c    = df["Close"]
    e9   = _ema(c, 9);  e21 = _ema(c, 21); e50 = _ema(c, 50)
    s20  = c.rolling(20).mean()
    price = float(c.iloc[-1])
    e9v   = float(e9.iloc[-1]);  e21v = float(e21.iloc[-1])
    e50v  = float(e50.iloc[-1]); s20v = float(s20.iloc[-1])
    rsi   = _rsi(c); atr = _atr(df); mv, ms = _macd(c)

    up = [e9v>e21v, e21v>e50v, rsi>52, price>s20v, mv>ms]
    dn = [e9v<e21v, e21v<e50v, rsi<48, price<s20v, mv<ms]
    bull = sum(up); bear = sum(dn)

    if bull >= 4:
        direction = "UP";   filters = up; score = bull
    elif bear >= 4:
        direction = "DOWN"; filters = dn; score = bear
    else:
        direction = "WAIT"; filters = [False]*5; score = max(bull, bear)

    raw = (abs(e9v-e21v)/e21v*800 + abs(price-s20v)/s20v*600
           + abs(rsi-50)*.8 + min(abs(mv-ms)*500, 30))
    st_ = round(min(99., max(20., raw)), 1)
    if direction == "WAIT":
        st_ = round(min(38., st_), 1)

    return {
        "direction": direction, "strength": st_, "score": score,
        "price": price, "ema9": round(e9v,2), "ema21": round(e21v,2),
        "sma20": round(s20v,2), "rsi": rsi, "atr": atr, "macd": round(mv,4),
        "f_ema": filters[0], "f_ema2": filters[1],
        "f_rsi": filters[2], "f_sma":  filters[3], "f_macd": filters[4],
    }


# ══════════════════════════════════════════════════════════
# الواجهة
# ══════════════════════════════════════════════════════════
clock = datetime.now().strftime("%H:%M:%S")

st.markdown(f"""
<div class="hdr">
  <span class="hdr-icon">&#127919;</span>
  <div class="hdr-title">SET DIRECTION</div>
  <div class="hdr-sub">TREND TRACKER &#8226; GOLD ENGINE</div>
</div>
<div class="timebar">
  <span class="tb-label">&#128337; Auto Refresh 60s</span>
  <div class="tb-dot"></div>
  <span class="tb-clock">{clock}</span>
</div>
""", unsafe_allow_html=True)

# ── السوق مغلق ──
if not is_market_open():
    st.markdown("""
<div class="closed-card">
  <span class="closed-icon">&#128274;</span>
  <span class="closed-title">MARKET CLOSED</span>
  <span class="closed-desc">سوق الذهب مغلق &#8212; عطلة نهاية الاسبوع</span>
  <div class="csched">
    <div class="cs-row">
      <span class="cs-day">&#9203; يفتح</span>
      <span class="cs-time">Monday 00:00 UTC</span>
      <span class="badge-open">OPEN</span>
    </div>
    <div class="cs-row">
      <span class="cs-day">&#128197; Sat &amp; Sun</span>
      <span class="cs-time">مغلق بالكامل</span>
      <span class="badge-close">CLOSED</span>
    </div>
    <div class="cs-row">
      <span class="cs-day">&#11088; Best Time</span>
      <span class="cs-time">London 3&#8211;6 PM UTC</span>
      <span class="badge-open">BEST</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
    st.markdown('<div class="sig">Developed by Ghost &#160;|&#160; Set Direction Engine</div>',
                unsafe_allow_html=True)
    st.stop()

# ── زر واحد فقط ──
if st.button(f"REFRESH  {clock}", use_container_width=True):
    st.session_state.last_run = 0
    st.rerun()

st.markdown("<div style='height:.7rem'></div>", unsafe_allow_html=True)

# ── تحليل تلقائي كل 60 ثانية ──
now = _time.time()
if (now - st.session_state.last_run) >= 60 or st.session_state.result is None:
    st.session_state.last_run = now
    with st.spinner("Scanning gold market..."):
        df = load_gold()
    if not df.empty and len(df) >= 60:
        new_res = analyze(df)
        prev_d  = st.session_state.prev_dir
        st.session_state.result   = new_res
        st.session_state.prev_dir = new_res["direction"]
        if prev_d is not None and prev_d != new_res["direction"]:
            st.rerun()

# ── عرض النتائج ──
if st.session_state.result:
    res = st.session_state.result
    d   = res["direction"]

    if d == "UP":
        cls, icon, word, desc = "up", "&#128200;", "BULLISH", "الذهب في اتجاه صاعد"
        bc, bg = "#00e676", "rgba(0,230,118,.55)"
    elif d == "DOWN":
        cls, icon, word, desc = "down", "&#128201;", "BEARISH", "الذهب في اتجاه هابط"
        bc, bg = "#ff1744", "rgba(255,23,68,.55)"
    else:
        cls, icon, word, desc = "wait", "&#9203;", "WAIT", "لا توافق بين الفلاتر"
        bc, bg = "#ffab00", "rgba(255,171,0,.55)"

    rsi_c = "#00e676" if res["rsi"] > 55 else ("#ff1744" if res["rsi"] < 45 else "#aaa")
    ts    = datetime.now().strftime("%H:%M:%S")
    pp    = f"{res['price']:,.2f}"
    pe9   = f"{res['ema9']:,.2f}"
    p21   = f"{res['ema21']:,.2f}"
    ps    = f"{res['sma20']:,.2f}"
    pr    = f"{res['rsi']}"
    pa    = f"{res['atr']:,.2f}"
    pm    = f"{res['macd']:+.4f}"
    pst   = f"{res['strength']:.1f}"
    psc   = f"{res['score']}/5"

    st.markdown(f"""
<div class="rc {cls}">
  <span class="rc-icon">{icon}</span>
  <span class="rc-word {cls}">{word}</span>
  <span class="rc-desc">{desc}</span>
  <div class="rc-time">LAST UPDATE: {ts}</div>
</div>
""", unsafe_allow_html=True)

    def b(ok, lbl):
        c2 = "ok" if ok else "fail"
        i2 = "&#9989;" if ok else "&#10060;"
        return (f'<div class="flc {c2}"><span class="fli">{i2}</span>'
                f'<span class="fll">{lbl}</span></div>')

    score_cls = "ok" if res["score"] >= 4 else "fail"
    score_ico = "&#127919;" if res["score"] >= 4 else "&#9646;"

    st.markdown(
        '<div class="gc" style="padding:1.2rem;">'
        '<div style="font-family:\'Orbitron\',monospace;font-size:.58rem;color:var(--dim);'
        'letter-spacing:2.5px;text-align:center;margin-bottom:.75rem;">SIGNAL FILTERS</div>'
        '<div class="flg">'
        + b(res["f_ema"],  "EMA 9/21")
        + b(res["f_ema2"], "EMA 21/50")
        + b(res["f_rsi"],  "RSI")
        + b(res["f_sma"],  "SMA 20")
        + b(res["f_macd"], "MACD")
        + f'<div class="flc {score_cls}"><span class="fli">{score_ico}</span>'
          f'<span class="fll">{psc}</span></div>'
        + '</div></div>',
        unsafe_allow_html=True)

    st.markdown(f"""
<div class="gc">
  <div class="pr">
    <span class="pl">Gold Price XAU/USD</span>
    <span class="pv">{pp}</span>
  </div>
  <div class="ig">
    <div class="ic"><span class="il">EMA 9</span><span class="iv gold">{pe9}</span></div>
    <div class="ic"><span class="il">EMA 21</span><span class="iv gold">{p21}</span></div>
    <div class="ic"><span class="il">SMA 20</span><span class="iv">{ps}</span></div>
    <div class="ic"><span class="il">RSI 14</span><span class="iv" style="color:{rsi_c};">{pr}</span></div>
    <div class="ic"><span class="il">MACD</span><span class="iv" style="color:{bc};">{pm}</span></div>
    <div class="ic"><span class="il">ATR</span><span class="iv">{pa}</span></div>
  </div>
  <div class="bh">
    <span class="bl">Signal Strength</span>
    <span class="bp" style="color:{bc};">{pst}%</span>
  </div>
  <div class="bt">
    <div class="bf" style="width:{pst}%;background:linear-gradient(90deg,{bc}44,{bc});box-shadow:0 0 12px {bg};"></div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="sig">Developed by Ghost &#160;|&#160; Set Direction Engine</div>',
            unsafe_allow_html=True)

# تحديث تلقائي كل 60 ثانية
_time.sleep(60)
st.rerun()
