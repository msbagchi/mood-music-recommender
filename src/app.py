import streamlit as st
import sys
import os
import plotly.graph_objects as go

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loader import load_spotify_data
from emotion_detector import EmotionDetector
from recommender import MoodRecommender

st.set_page_config(
    page_title="MoodTunes",
    page_icon="🎵",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;900&display=swap');
*, body, .stApp { font-family: 'Outfit', sans-serif !important; }

.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

#cursor-dot {
    width: 14px; height: 14px;
    background: #7297f4;
    border-radius: 50%;
    position: fixed;
    top: -100px; left: -100px;
    pointer-events: none;
    z-index: 999999;
    transform: translate(-50%, -50%);
    box-shadow: 0 0 12px #7297f4, 0 0 28px #7297f4, 0 0 55px rgba(114,151,244,0.6);
    transition: width 0.15s, height 0.15s;
}
#cursor-ring {
    width: 44px; height: 44px;
    border: 2px solid rgba(114,151,244,0.8);
    border-radius: 50%;
    position: fixed;
    top: -100px; left: -100px;
    pointer-events: none;
    z-index: 999998;
    transform: translate(-50%, -50%);
    box-shadow: 0 0 10px rgba(114,151,244,0.4);
}
.moodbubble {
    position: fixed;
    border-radius: 50%;
    pointer-events: none;
    z-index: 999996;
    transform: translate(-50%, -50%);
    animation: bubbleFloat 1.2s ease-out forwards;
    border: 1.5px solid rgba(114,151,244,0.7);
    background: transparent;
}
@keyframes bubbleFloat {
    0%   { opacity: 0.9; transform: translate(-50%,-50%) scale(1); }
    40%  { opacity: 0.6; }
    100% { opacity: 0;   transform: translate(-50%,-50%) scale(2.5) translateY(-20px); }
}
.moodburst {
    position: fixed;
    border-radius: 50%;
    pointer-events: none;
    z-index: 999995;
    transform: translate(-50%, -50%);
    border: 1.5px solid rgba(114,151,244,0.8);
    background: rgba(114,151,244,0.15);
    transition: all 0.6s ease-out;
    opacity: 1;
}

.hero { text-align: center; padding: 3rem 1rem 1rem; }
.hero h1 {
    font-size: 4rem; font-weight: 900;
    background: linear-gradient(90deg, #7297f4, #a78bfa, #38bdf8, #34d399);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin-bottom: 0.5rem;
    animation: gradientShift 4s ease infinite; background-size: 300% 300%;
}
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.hero p { color: rgba(255,255,255,0.6); font-size: 1.2rem; font-weight: 300; }

.stTextInput input {
    background: rgba(255,255,255,0.07) !important;
    border: 1.5px solid rgba(114,151,244,0.5) !important;
    border-radius: 16px !important; color: white !important;
    font-size: 1.1rem !important; padding: 1rem 1.5rem !important;
    transition: all 0.3s !important;
}
.stTextInput input:focus {
    border-color: #7297f4 !important;
    box-shadow: 0 0 20px rgba(114,151,244,0.3) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #7297f4, #a78bfa) !important;
    color: white !important; border: none !important;
    border-radius: 50px !important; font-size: 1.1rem !important;
    font-weight: 700 !important; padding: 0.75rem 3rem !important;
    width: 100% !important; transition: all 0.3s !important;
    letter-spacing: 1px;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(114,151,244,0.5) !important;
}
.mood-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px; padding: 1.5rem;
    text-align: center; backdrop-filter: blur(10px);
}
.mood-card .label {
    color: rgba(255,255,255,0.5); font-size: 0.85rem;
    text-transform: uppercase; letter-spacing: 2px; margin-bottom: 0.5rem;
}
.mood-card .value {
    font-size: 1.8rem; font-weight: 700;
    background: linear-gradient(90deg, #7297f4, #a78bfa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.song-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px; padding: 1.2rem 1.5rem;
    margin-bottom: 1rem; transition: all 0.3s;
    backdrop-filter: blur(10px);
}
.song-card:hover {
    background: rgba(114,151,244,0.15);
    border-color: rgba(114,151,244,0.5);
    transform: translateX(6px);
}
.song-rank { font-size: 2rem; font-weight: 900; color: rgba(255,255,255,0.1); min-width: 50px; }
.song-name { font-size: 1.05rem; font-weight: 600; color: white; }
.song-artist { font-size: 0.9rem; color: rgba(255,255,255,0.5); margin-top: 2px; }
.song-badge {
    display: inline-block; background: rgba(114,151,244,0.2);
    border: 1px solid rgba(114,151,244,0.4); border-radius: 50px;
    padding: 2px 12px; font-size: 0.78rem; color: #7297f4; margin-right: 6px;
}
.section-title {
    font-size: 1.5rem; font-weight: 700; color: white;
    margin: 2rem 0 1rem; display: flex; align-items: center; gap: 10px;
}
.section-title::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, rgba(114,151,244,0.5), transparent);
}
[data-testid="stMetricValue"] { color: #7297f4 !important; font-size: 1.5rem !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { color: rgba(255,255,255,0.5) !important; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(114,151,244,0.4); border-radius: 3px; }
#MainMenu, footer, header { visibility: hidden; }
</style>

<!-- Cursor elements injected directly into Streamlit DOM -->
<div id="cursor-dot"></div>
<div id="cursor-ring"></div>

<script>
(function initCursor() {
    const dot  = document.getElementById('cursor-dot');
    const ring = document.getElementById('cursor-ring');

    if (!dot || !ring) {
        setTimeout(initCursor, 100);
        return;
    }

    let mx = -200, my = -200;
    let rx = -200, ry = -200;
    let hue = 220;
    let bubbleCount = 0;
    const bubbleSizes = [8,10,12,14,16,9,11,13];

    document.addEventListener('mousemove', (e) => {
        mx = e.clientX;
        my = e.clientY;
        dot.style.left = mx + 'px';
        dot.style.top  = my + 'px';
        spawnBubble(mx, my);
    });

    document.addEventListener('mousedown', (e) => {
        mx = e.clientX; my = e.clientY;
        dot.style.width  = '22px';
        dot.style.height = '22px';
        dot.style.boxShadow = '0 0 20px #7297f4, 0 0 50px #7297f4, 0 0 80px rgba(114,151,244,0.8)';
        for (let i = 0; i < 14; i++) spawnBurstBubble(mx, my);
    });

    document.addEventListener('mouseup', () => {
        dot.style.width  = '14px';
        dot.style.height = '14px';
        dot.style.boxShadow = '0 0 12px #7297f4, 0 0 28px #7297f4, 0 0 55px rgba(114,151,244,0.6)';
    });

    function animateRing() {
        rx += (mx - rx) * 0.1;
        ry += (my - ry) * 0.1;
        ring.style.left = rx + 'px';
        ring.style.top  = ry + 'px';
        hue = 220 + Math.sin(Date.now() * 0.002) * 15;
        const l = 65 + Math.sin(Date.now() * 0.003) * 10;
        ring.style.borderColor = `hsl(${hue},85%,${l}%)`;
        ring.style.boxShadow   = `0 0 12px hsl(${hue},85%,${l}%)`;
        requestAnimationFrame(animateRing);
    }
    animateRing();

    function spawnBubble(x, y) {
        if (bubbleCount > 22) return;
        bubbleCount++;
        const b   = document.createElement('div');
        b.className = 'moodbubble';
        const size = bubbleSizes[Math.floor(Math.random() * bubbleSizes.length)];
        const ox   = (Math.random() - 0.5) * 18;
        const oy   = (Math.random() - 0.5) * 18;
        const h    = 220 + Math.floor(Math.random() * 20 - 10);
        const s    = 80  + Math.floor(Math.random() * 15);
        const l    = 65  + Math.floor(Math.random() * 15);
        const dur  = (Math.random() * 0.5 + 0.8).toFixed(2);
        b.style.cssText = `
            left:${x+ox}px; top:${y+oy}px;
            width:${size}px; height:${size}px;
            border-color:hsl(${h},${s}%,${l}%);
            box-shadow:inset 0 0 6px rgba(114,151,244,0.3),0 0 8px rgba(114,151,244,0.2);
            animation-duration:${dur}s;
        `;
        document.body.appendChild(b);
        setTimeout(() => { b.remove(); bubbleCount--; }, 1300);
    }

    function spawnBurstBubble(x, y) {
        const b     = document.createElement('div');
        b.className = 'moodburst';
        const angle = Math.random() * Math.PI * 2;
        const dist  = Math.random() * 60 + 25;
        const size  = Math.random() * 18 + 8;
        const h     = 220 + Math.floor(Math.random() * 30 - 15);
        b.style.cssText = `
            left:${x}px; top:${y}px;
            width:${size}px; height:${size}px;
            border-color:hsl(${h},85%,70%);
            background:rgba(114,151,244,0.1);
            box-shadow:0 0 10px rgba(114,151,244,0.4);
        `;
        document.body.appendChild(b);
        setTimeout(() => {
            b.style.left      = `${x + Math.cos(angle)*dist}px`;
            b.style.top       = `${y + Math.sin(angle)*dist}px`;
            b.style.opacity   = '0';
            b.style.transform = 'translate(-50%,-50%) scale(0)';
        }, 10);
        setTimeout(() => b.remove(), 650);
    }
})();
</script>
""", unsafe_allow_html=True)


@st.cache_resource
def load_models():
    df = load_spotify_data()
    detector   = EmotionDetector()
    recommender = MoodRecommender(df)
    return detector, recommender

# ── Hero ──
st.markdown("""
<div class="hero">
    <h1>🎵 MoodTunes</h1>
    <p>Tell us how you feel — we'll find the perfect soundtrack for your soul</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col_input, _ = st.columns([2, 1])
with col_input:
    mood_text = st.text_input(
        "", placeholder="✨  I feel tired and sad...",
        label_visibility="collapsed"
    )

col_opt1, col_opt2, col_opt3 = st.columns([1, 1, 1])
with col_opt1:
    mode = st.radio("Mode", ["🪞 Match my mood", "🚀 Lift my mood"], horizontal=True)
with col_opt2:
    top_n = st.slider("Number of songs", 5, 20, 10)
with col_opt3:
    st.markdown("<br>", unsafe_allow_html=True)
    go_btn = st.button("🎧  Discover Songs", use_container_width=True)

recommend_mode = "mirror" if "Match" in mode else "lift"

if go_btn:
    if not mood_text.strip():
        st.warning("Please type how you're feeling first!")
    else:
        detector, recommender = load_models()

        with st.spinner("🔮 Reading your emotions..."):
            result     = detector.detect(mood_text)
            mood_label = detector.describe_mood(result['valence'], result['arousal'])

        st.markdown('<div class="section-title">✨ Your Mood Analysis</div>',
                    unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        for col, (label, value) in zip(
            [c1, c2, c3, c4],
            [("Mood",        mood_label),
             ("Valence",     result['valence']),
             ("Arousal",     result['arousal']),
             ("Top Emotion", result['emotions'][0]['label'].capitalize())]
        ):
            col.markdown(f"""
            <div class="mood-card">
                <div class="label">{label}</div>
                <div class="value">{value}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Emotion Map ──
        st.markdown('<div class="section-title">🧠 Emotion Map</div>',
                    unsafe_allow_html=True)

        fig = go.Figure()
        for x0,x1,y0,y1,color,label in [
            (0,  0.5, 0,   0.5, "rgba(99,102,241,0.15)",  "Sad & Low Energy"),
            (0.5,1,   0,   0.5, "rgba(52,211,153,0.15)",  "Calm & Content"),
            (0,  0.5, 0.5, 1,   "rgba(239,68,68,0.15)",   "Tense & Agitated"),
            (0.5,1,   0.5, 1,   "rgba(251,191,36,0.15)",  "Happy & Energetic"),
        ]:
            fig.add_shape(type="rect",x0=x0,x1=x1,y0=y0,y1=y1,
                          fillcolor=color,line=dict(width=0))
            fig.add_annotation(x=(x0+x1)/2,y=(y0+y1)/2,text=label,
                               font=dict(color="rgba(255,255,255,0.3)",size=11),
                               showarrow=False)

        for emo,(v,a) in {
            "Joy":(0.85,0.75),"Calm":(0.65,0.25),
            "Sad":(0.20,0.30),"Anger":(0.20,0.85),
            "Fear":(0.25,0.70),"Neutral":(0.50,0.50)
        }.items():
            fig.add_trace(go.Scatter(
                x=[v],y=[a],mode="markers+text",text=[emo],
                textposition="top center",
                marker=dict(size=8,color="rgba(255,255,255,0.3)"),
                textfont=dict(color="rgba(255,255,255,0.4)",size=10),
                showlegend=False,hoverinfo="skip"))

        fig.add_trace(go.Scatter(
            x=[result['valence']],y=[result['arousal']],
            mode="markers+text",text=["YOU ARE HERE"],
            textposition="top center",
            marker=dict(size=18,color="#7297f4",
                        line=dict(color="white",width=2),symbol="star"),
            textfont=dict(color="#7297f4",size=12,family="Outfit"),
            showlegend=False))

        if recommend_mode == "lift":
            tv = min(1.0, result['valence']+0.25)
            ta = min(1.0, result['arousal']+0.15)
            fig.add_trace(go.Scatter(
                x=[tv],y=[ta],mode="markers+text",text=["TARGET"],
                textposition="top center",
                marker=dict(size=14,color="#34d399",
                            line=dict(color="white",width=2),symbol="diamond"),
                textfont=dict(color="#34d399",size=11),showlegend=False))
            fig.add_annotation(
                x=result['valence'],y=result['arousal'],
                ax=tv,ay=ta,xref="x",yref="y",axref="x",ayref="y",
                showarrow=True,arrowhead=2,arrowcolor="#34d399",arrowwidth=2)

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.03)",
            xaxis=dict(title="Valence (Sadness → Happiness)",range=[0,1],
                       color="rgba(255,255,255,0.5)",
                       gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(title="Arousal (Calm → Energetic)",range=[0,1],
                       color="rgba(255,255,255,0.5)",
                       gridcolor="rgba(255,255,255,0.05)"),
            height=420,margin=dict(l=20,r=20,t=20,b=20),
            font=dict(family="Outfit"))
        st.plotly_chart(fig,use_container_width=True)

        # ── Songs ──
        with st.spinner("🎵 Finding your perfect songs..."):
            songs     = recommender.recommend(
                result['valence'],result['arousal'],
                mode=recommend_mode,top_n=top_n)
            precision = recommender.precision_at_k(
                result['valence'],result['arousal'],k=top_n)

        st.markdown(
            f'<div class="section-title">🎶 Your Playlist '
            f'<span style="font-size:0.9rem;color:rgba(255,255,255,0.4);font-weight:400">'
            f'Precision@{top_n}: {precision}</span></div>',
            unsafe_allow_html=True)

        left_col, right_col = st.columns([3, 2])

        with left_col:
            for _, row in songs.iterrows():
                query = f"{row['track_name']} {row['artists']}".replace(" ","+")
                yt    = f"https://www.youtube.com/results?search_query={query}"
                sp    = f"https://open.spotify.com/search/{row['track_name'].replace(' ','%20')}"
                st.markdown(f"""
                <div class="song-card">
                  <div style="display:flex;align-items:center;gap:16px">
                    <div class="song-rank">#{int(row['rank'])}</div>
                    <div style="flex:1">
                      <div class="song-name">{row['track_name']}</div>
                      <div class="song-artist">🎤 {row['artists']}</div>
                      <div style="margin-top:8px">
                        <span class="song-badge">💙 {row['valence']}</span>
                        <span class="song-badge">⚡ {row['energy']}</span>
                        <span class="song-badge">🥁 {row['tempo']} BPM</span>
                      </div>
                    </div>
                    <div style="display:flex;flex-direction:column;gap:8px">
                      <a href="{yt}" target="_blank"
                         style="background:rgba(255,0,0,0.2);
                                border:1px solid rgba(255,0,0,0.4);
                                color:#ff6b6b;padding:6px 14px;border-radius:50px;
                                text-decoration:none;font-size:0.82rem;font-weight:600;
                                white-space:nowrap">▶ YouTube</a>
                      <a href="{sp}" target="_blank"
                         style="background:rgba(30,215,96,0.15);
                                border:1px solid rgba(30,215,96,0.4);
                                color:#1ed760;padding:6px 14px;border-radius:50px;
                                text-decoration:none;font-size:0.82rem;font-weight:600;
                                white-space:nowrap">♫ Spotify</a>
                    </div>
                  </div>
                </div>""", unsafe_allow_html=True)

        with right_col:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.04);
                        border:1px solid rgba(255,255,255,0.1);
                        border-radius:20px;padding:1.5rem;margin-bottom:1rem">
              <div style="color:white;font-weight:700;font-size:1.1rem;
                          margin-bottom:1.2rem">📊 Playlist Stats</div>
              <div style="margin-bottom:1rem">
                <div style="color:rgba(255,255,255,0.5);font-size:0.8rem;
                            text-transform:uppercase;letter-spacing:1px">Avg Valence</div>
                <div style="color:#7297f4;font-size:1.4rem;font-weight:700">
                    {songs['valence'].mean():.2f}</div>
              </div>
              <div style="margin-bottom:1rem">
                <div style="color:rgba(255,255,255,0.5);font-size:0.8rem;
                            text-transform:uppercase;letter-spacing:1px">Avg Energy</div>
                <div style="color:#a78bfa;font-size:1.4rem;font-weight:700">
                    {songs['energy'].mean():.2f}</div>
              </div>
              <div style="margin-bottom:1rem">
                <div style="color:rgba(255,255,255,0.5);font-size:0.8rem;
                            text-transform:uppercase;letter-spacing:1px">Avg Tempo</div>
                <div style="color:#38bdf8;font-size:1.4rem;font-weight:700">
                    {songs['tempo'].mean():.0f} BPM</div>
              </div>
              <div>
                <div style="color:rgba(255,255,255,0.5);font-size:0.8rem;
                            text-transform:uppercase;letter-spacing:1px">Avg Danceability</div>
                <div style="color:#34d399;font-size:1.4rem;font-weight:700">
                    {songs['danceability'].mean():.2f}</div>
              </div>
            </div>""", unsafe_allow_html=True)

            emo_fig = go.Figure(go.Bar(
                x=[e['score']*100 for e in result['emotions']],
                y=[e['label'].capitalize() for e in result['emotions']],
                orientation='h',
                marker=dict(color=["#7297f4","#a78bfa","#38bdf8"],
                            line=dict(width=0)),
                text=[f"{e['score']*100:.1f}%" for e in result['emotions']],
                textposition='outside',
                textfont=dict(color="white",size=11)
            ))
            emo_fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=False,showticklabels=False,
                           color="rgba(255,255,255,0.3)"),
                yaxis=dict(color="rgba(255,255,255,0.7)"),
                height=180,margin=dict(l=0,r=60,t=10,b=10),
                font=dict(family="Outfit",color="white"))
            st.plotly_chart(emo_fig,use_container_width=True)