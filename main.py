from flask import Flask, render_template_string, request
import os
import json

app = Flask(__name__)

# --- ЛОГИКА ДЛЯ НОВЫХ ШРИФТОВ ---
def get_dynamic_fonts(text):
    try:
        base_path = os.path.dirname(__file__)
        json_path = os.path.join(base_path, 'fonts.json')
        if not os.path.exists(json_path): return []
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        results = []
        for name, mapping in data.items():
            new_text = "".join([mapping.get(char.lower(), char) for char in text])
            results.append({'name': name, 'text': new_text})
        return results
    except:
        return []

FAVICON = """
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🚀</text></svg>">
"""

INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Font Flow — Premium Aesthetic Text Tool</title>
    <meta name="description" content="Generate stylish fonts, nicknames and aesthetic symbols. Dark mode, character counter and more.">
    
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-P4Q7YLZLBC"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-P4Q7YLZLBC');
    </script>
    
    """ + FAVICON + """
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2712778222245542" crossorigin="anonymous"></script>
    <link href="https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Inter:wght@400;600;900&display=swap" rel="stylesheet">
    
    <style>
        :root { 
            --p: #00ff88; --s: #bd00ff; --bg: #080808; --card: rgba(255,255,255,0.03); 
            --text: #ffffff; --sub: #888888; --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        body.light-mode {
            --bg: #f5f5f7; --card: #ffffff; --text: #1d1d1f; --sub: #6e6e73;
        }

        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; transition: background var(--transition), color var(--transition); }
        
        body {
            background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif;
            margin: 0; min-height: 100vh; display: flex; flex-direction: column; align-items: center;
            padding: 20px; overflow-x: hidden;
        }

        /* --- Анимированный фон --- */
        .bg-blobs {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            z-index: -1; overflow: hidden; filter: blur(80px); opacity: 0.3;
            display: block;
        }
        body.no-anim .blob { animation: none !important; }
        body.hide-bg .bg-blobs { display: none; }

        .blob { position: absolute; width: 400px; height: 400px; border-radius: 50%; animation: move 20s infinite alternate; }
        .blob1 { background: var(--p); top: -10%; left: -10%; }
        .blob2 { background: var(--s); bottom: -10%; right: -10%; animation-delay: -5s; }
        @keyframes move { from { transform: translate(0,0); } to { transform: translate(150px, 150px); } }

        /* --- Хедер и Настройки --- */
        .header { width: 100%; max-width: 550px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; z-index: 10; }
        .settings-trigger { 
            background: var(--card); border: 1px solid rgba(255,255,255,0.1); 
            width: 45px; height: 45px; border-radius: 12px; display: flex; align-items: center; justify-content: center;
            cursor: pointer; font-size: 1.2rem; transition: var(--transition);
        }
        .settings-trigger:hover { transform: rotate(45deg); border-color: var(--p); }

        .settings-panel {
            position: fixed; top: 80px; right: -300px; width: 280px; 
            background: var(--card); backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.1); border-radius: 20px;
            padding: 20px; z-index: 100; transition: var(--transition);
            box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        }
        .settings-panel.active { right: 20px; }
        .setting-item { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
        .setting-item label { font-size: 0.9rem; font-weight: 600; }

        /* --- Переключатель (Toggle) --- */
        .switch { position: relative; display: inline-block; width: 44px; height: 24px; }
        .switch input { opacity: 0; width: 0; height: 0; }
        .slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #333; transition: .4s; border-radius: 34px; }
        .slider:before { position: absolute; content: ""; height: 18px; width: 18px; left: 3px; bottom: 3px; background-color: white; transition: .4s; border-radius: 50%; }
        input:checked + .slider { background-color: var(--p); }
        input:checked + .slider:before { transform: translateX(20px); }

        /* --- Контейнер --- */
        .container { width: 100%; max-width: 550px; text-align: center; z-index: 1; }
        h1 { font-family: 'Syncopate', sans-serif; font-size: 2.2rem; background: linear-gradient(90deg, var(--p), var(--s)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; }
        
        .input-wrapper { position: relative; margin-top: 25px; }
        textarea {
            width: 100%; padding: 20px; border-radius: 18px; 
            background: var(--card); border: 1px solid rgba(255,255,255,0.05);
            color: var(--text); font-size: 1.1rem; outline: none; transition: var(--transition);
            min-height: 120px; resize: none;
        }
        textarea:focus { border-color: var(--p); box-shadow: 0 0 20px rgba(0,255,136,0.1); }
        
        .char-counter { position: absolute; bottom: 12px; right: 15px; font-size: 0.75rem; color: var(--sub); font-weight: 700; }

        .results { margin-top: 25px; display: grid; gap: 12px; width: 100%; }
        .card {
            background: var(--card); border: 1px solid rgba(255,255,255,0.05);
            padding: 16px 20px; border-radius: 14px; display: flex; justify-content: space-between;
            align-items: center; cursor: pointer; transition: 0.2s;
        }
        .card:hover { transform: scale(1.02); border-color: var(--s); }
        .card span { font-size: 1.2rem; text-align: left; flex: 1; padding-right: 10px; overflow-wrap: anywhere; }
        .copy-btn { font-size: 0.7rem; font-weight: 800; color: var(--sub); text-transform: uppercase; }
        .card:hover .copy-btn { color: var(--p); }

        .seo-box { margin-top: 40px; text-align: left; font-size: 0.85rem; color: var(--sub); line-height: 1.6; }
        footer { margin-top: 40px; padding: 20px; font-size: 0.8rem; opacity: 0.6; }
        footer a { color: var(--text); text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <div class="bg-blobs" id="blobs"><div class="blob blob1"></div><div class="blob blob2"></div></div>
    
    <div class="header">
        <h1>FONT FLOW</h1>
        <div class="settings-trigger" onclick="toggleSettings()">⚙️</div>
    </div>

    <div class="settings-panel" id="settings">
        <h3 style="margin-top:0">Settings</h3>
        <div class="setting-item">
            <label>Light Mode</label>
            <label class="switch">
                <input type="checkbox" id="themeToggle" onchange="updateSettings()">
                <span class="slider"></span>
            </label>
        </div>
        <div class="setting-item">
            <label>Animated BG</label>
            <label class="switch">
                <input type="checkbox" id="bgToggle" checked onchange="updateSettings()">
                <span class="slider"></span>
            </label>
        </div>
        <div class="setting-item">
            <label>Smooth Motion</label>
            <label class="switch">
                <input type="checkbox" id="animToggle" checked onchange="updateSettings()">
                <span class="slider"></span>
            </label>
        </div>
        <button onclick="toggleSettings()" style="width:100%; background: var(--p); border:none; padding:8px; border-radius:8px; cursor:pointer; font-weight:bold">Save & Close</button>
    </div>

    <div class="container">
        <div class="input-wrapper">
            <textarea id="input" placeholder="Enter your text here..."></textarea>
            <div class="char-counter" id="counter">0</div>
        </div>

        <div id="output" class="results"></div>

        <div class="seo-box">
            <h2 style="color:var(--text); font-size: 1rem">Aesthetic Font Changer</h2>
            <p>Font Flow is more than a simple generator. It's a professional tool for creating <strong>cool nicknames</strong> and <strong>stylish text</strong> for gaming profiles and social bios. Our tool supports symbols, fancy letters, and custom text decorations.</p>
        </div>

        <footer>
            © 2026 Font Flow | <a href="/privacy">Privacy Policy</a>
        </footer>
    </div>

    <script>
        const FONTS = {
            "Bold": "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳",
            "Italic": "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻",
            "Monospace": "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄傳ＷＸＹ𝚉𝚊𝚋𝚌𝚍ｅ𝚏𝚐ｈ𝚒𝚓𝚔𝚕𝕞𝚗𝚘𝚙𝚚𝚛𝘴𝚝𝚞𝚟𝚠𝚡𝚢𝚣",
            "Bubbles": "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ"
        };
        const alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
        const DECORATIONS = [
            {l: "꧁༺ ", r: " ༻꧂"}, {l: "｡☆✼★ ", r: " ★✼☆｡"}, {l: "⚡ ", r: " ⚡"}, {l: "✿ ", r: " ✿"}
        ];

        const input = document.getElementById('input');
        const output = document.getElementById('output');
        const counter = document.getElementById('counter');

        function toggleSettings() { document.getElementById('settings').classList.toggle('active'); }

        function updateSettings() {
            const isLight = document.getElementById('themeToggle').checked;
            const isBg = document.getElementById('bgToggle').checked;
            const isAnim = document.getElementById('animToggle').checked;

            document.body.classList.toggle('light-mode', isLight);
            document.body.classList.toggle('hide-bg', !isBg);
            document.body.classList.toggle('no-anim', !isAnim);

            localStorage.setItem('ff_settings', JSON.stringify({isLight, isBg, isAnim}));
        }

        // Загрузка настроек
        (function loadSettings() {
            const saved = JSON.parse(localStorage.getItem('ff_settings') || '{}');
            if(saved.isLight) { document.getElementById('themeToggle').checked = true; }
            if(saved.isBg === false) { document.getElementById('bgToggle').checked = false; }
            if(saved.isAnim === false) { document.getElementById('animToggle').checked = false; }
            updateSettings();
        })();

        input.oninput = function() {
            const val = input.value;
            counter.innerText = val.length;
            if(!val) { output.innerHTML = ""; return; }
            
            let html = "";
            
            // Украшения
            DECORATIONS.forEach(d => {
                const res = d.l + val + d.r;
                html += createCard(res);
            });

            // Шрифты
            for (const key in FONTS) {
                let res = "";
                for(let c of val) {
                    let i = alpha.indexOf(c);
                    res += (i !== -1) ? FONTS[key][i] : c;
                }
                html += createCard(res);
            }
            output.innerHTML = html;
        };

        function createCard(text) {
            return `<div class="card" onclick="copyText(this, '${text}')"><span>${text}</span><div class="copy-btn">Copy</div></div>`;
        }

        function copyText(el, text) {
            navigator.clipboard.writeText(text);
            const btn = el.querySelector('.copy-btn');
            btn.innerText = "COPIED!";
            btn.style.color = "var(--p)";
            setTimeout(() => { btn.innerText = "COPY"; btn.style.color = "var(--sub)"; }, 1000);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/privacy')
def privacy():
    return render_template_string(PRIVACY_HTML)

@app.route('/ads.txt')
def ads_txt():
    return "google.com, pub-2712778222245542, DIRECT, f08c47fec0942fa0", 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
