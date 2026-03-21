from flask import Flask, render_template_string, request
import os
import json

app = Flask(__name__)

# --- ЛОГИКА ДЛЯ НОВЫХ ШРИФТОВ ---
def get_dynamic_fonts(text):
    try:
        base_path = os.path.dirname(__file__)
        json_path = os.path.join(base_path, 'fonts.json')
        if not os.path.exists(json_path):
            return []
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        results = []
        for name, mapping in data.items():
            new_text = "".join([mapping.get(char.lower(), char) for char in text])
            results.append({'name': name, 'text': new_text})
        return results
    except Exception as e:
        print(f"Font error: {e}")
        return []

# Общая иконка
FAVICON = '<link rel="icon" href="data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 100 100\'><text y=\'.9em\' font-size=\'90\'>🚀</text></svg>">'

INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Font Flow — Stylish Text Generator & Aesthetic Fonts</title>
    """ + FAVICON + """
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2712778222245542" crossorigin="anonymous"></script>
    <link href="https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Inter:wght@400;600;900&display=swap" rel="stylesheet">
    <style>
        :root { --p: #00ff88; --s: #bd00ff; --bg: #080808; }
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        body {
            background: var(--bg); color: #fff; font-family: 'Inter', sans-serif;
            margin: 0; min-height: 100vh; display: flex; flex-direction: column; align-items: center;
            padding: 20px; overflow-x: hidden;
        }
        .bg-blobs {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            z-index: -1; overflow: hidden; filter: blur(80px); opacity: 0.3;
        }
        .blob { position: absolute; width: 300px; height: 300px; border-radius: 50%; animation: move 20s infinite alternate; }
        .blob1 { background: var(--p); top: -10%; left: -10%; }
        .blob2 { background: var(--s); bottom: -10%; right: -10%; animation-delay: -5s; }
        @keyframes move { from { transform: translate(0,0); } to { transform: translate(100px, 100px); } }
        
        .container { width: 100%; max-width: 550px; text-align: center; z-index: 1; }
        h1 {
            font-family: 'Syncopate', sans-serif; font-size: clamp(2rem, 10vw, 2.5rem);
            background: linear-gradient(90deg, var(--p), var(--s));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin-bottom: 8px; filter: drop-shadow(0 0 15px rgba(0,255,136,0.4));
        }
        .description { color: #aaa; font-size: 0.9rem; margin-bottom: 25px; opacity: 0.8; }
        
        textarea {
            width: 100%; padding: 20px; border-radius: 15px; 
            background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1);
            color: #fff; font-size: 1.1rem; outline: none; transition: 0.4s;
            backdrop-filter: blur(10px);
        }
        textarea:focus { border-color: var(--p); background: rgba(255,255,255,0.06); }
        
        .results { margin-top: 25px; display: grid; gap: 12px; width: 100%; }
        .card {
            background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05);
            padding: 16px 20px; border-radius: 14px; display: flex; justify-content: space-between;
            align-items: center; cursor: pointer; transition: 0.3s;
        }
        .card:hover { transform: translateY(-2px); border-color: var(--p); background: rgba(255,255,255,0.05); }
        .card:active { transform: scale(0.98); }
        
        .copy-btn { 
            background: rgba(255,255,255,0.08); color: #fff; padding: 8px 16px; 
            border-radius: 10px; font-weight: 700; font-size: 0.7rem; transition: 0.3s;
        }
        .card:hover .copy-btn { background: var(--p); color: #000; }

        /* MODAL POPUP */
        #privacy-modal {
            position: fixed; bottom: -100%; left: 50%; transform: translateX(-50%);
            width: 90%; max-width: 400px; background: #111; border: 1px solid var(--p);
            border-radius: 20px; padding: 25px; z-index: 9999;
            box-shadow: 0 10px 40px rgba(0,0,0,0.8); transition: bottom 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        #privacy-modal.show { bottom: 30px; }
        #privacy-modal h3 { margin-top: 0; color: var(--p); font-size: 1.2rem; }
        #privacy-modal p { font-size: 0.85rem; color: #ccc; line-height: 1.4; }
        .modal-btns { display: flex; gap: 10px; margin-top: 20px; }
        .btn-accept { 
            flex: 2; background: linear-gradient(90deg, var(--p), var(--s)); border: none;
            color: #000; padding: 12px; border-radius: 10px; font-weight: bold; cursor: pointer;
            transition: transform 0.2s;
        }
        .btn-decline { 
            flex: 1; background: transparent; border: 1px solid #444; color: #888;
            padding: 12px; border-radius: 10px; cursor: pointer; transition: 0.2s;
        }
        .btn-accept:active, .btn-decline:active { transform: scale(0.9); }
        .btn-decline:hover { border-color: #666; color: #fff; }

        footer { margin-top: 40px; padding-bottom: 20px; font-size: 0.8rem; opacity: 0.6; }
        footer a { color: #aaa; text-decoration: none; transition: 0.3s; }
        footer a:hover { color: var(--p); }
    </style>
</head>
<body>
    <div id="privacy-modal">
        <h3>Privacy Policy</h3>
        <p>We use cookies to improve your experience and show relevant ads. By clicking "Accept", you agree to our <a href="/privacy" style="color:var(--p)">Privacy Policy</a>.</p>
        <div class="modal-btns">
            <button class="btn-accept" onclick="acceptPrivacy()">Accept</button>
            <button class="btn-decline" onclick="closeModal()">Decline</button>
        </div>
    </div>

    <div class="bg-blobs"><div class="blob blob1"></div><div class="blob blob2"></div></div>
    <div class="container">
        <h1>FONT FLOW</h1>
        <div class="description">Elevate your style for social media and games</div>
        <textarea id="input" placeholder="Type your text here..."></textarea>
        
        <div id="output" class="results">
            {% if extra_fonts %}
                {% for font in extra_fonts %}
                <div class="card" onclick="copyDynamic(this, '{{ font.text }}')">
                    <span>{{ font.text }}</span>
                    <div class='copy-btn'>COPY</div>
                </div>
                {% endfor %}
            {% endif %}
        </div>

        <footer>
            © 2026 Font Flow | <a href="/privacy">Privacy Policy</a>
        </footer>
    </div>

    <script>
        // Проверка согласия
        window.onload = function() {
            if (!localStorage.getItem('privacyAccepted')) {
                setTimeout(() => {
                    document.getElementById('privacy-modal').classList.add('show');
                }, 1000);
            }
        }

        function acceptPrivacy() {
            localStorage.setItem('privacyAccepted', 'true');
            closeModal();
        }

        function closeModal() {
            document.getElementById('privacy-modal').classList.remove('show');
        }

        const FONTS = {
            "Italic": "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻",
            "Bold": "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳",
            "Monospace": "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄傳ＷＸＹ𝚉𝚊𝚋𝚌𝚍ｅ𝚏𝚐ｈ𝚒𝚓𝚔𝚕𝕞𝚗𝚘𝚙𝚚𝚛𝘴𝚝𝚞𝚟𝚠𝚡𝚢𝚣",
            "Bubbles": "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ",
            "Small Caps": "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ",
            "Upside": "ɐqɔpǝɟƃɥᴉɾʞꞁɯuodbɹsʇnʌʍxʎzⱯᗷᑐᗡEᖵᘐHIᘀKꞀWNOᗡᑐᖴS⊥∩ΛM᙭⅄Z"
        };
        const alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
        const input = document.getElementById('input');
        const output = document.getElementById('output');

        function copyDynamic(el, text) {
            navigator.clipboard.writeText(text);
            el.classList.add('copied');
            el.querySelector('.copy-btn').innerText = "DONE!";
            setTimeout(() => {
                el.classList.remove('copied');
                el.querySelector('.copy-btn').innerText = "COPY";
            }, 1200);
        }

        input.oninput = function() {
            const val = input.value;
            if(!val) { output.innerHTML = ""; return; }
            let oldContent = "";
            for (const key in FONTS) {
                let res = "";
                let textToProcess = (key === "Upside") ? val.split("").reverse().join("") : val;
                for(let c of textToProcess) {
                    let i = alpha.indexOf(c);
                    res += (i !== -1) ? FONTS[key][i] : c;
                }
                oldContent += `<div class='card' onclick="copyDynamic(this, '${res}')"><span>${res}</span><div class='copy-btn'>COPY</div></div>`;
            }
            output.innerHTML = oldContent;
        };
    </script>
</body>
</html>
"""

PRIVACY_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Privacy Policy - Font Flow</title>
    """ + FAVICON + """
    <style>
        body { background: #080808; color: #ccc; font-family: sans-serif; padding: 40px; line-height: 1.6; max-width: 800px; margin: 0 auto; }
        h1 { color: #00ff88; }
        h2 { color: #fff; margin-top: 30px; border-left: 4px solid #bd00ff; padding-left: 15px; }
        .back-link { 
            display: inline-block; margin-top: 40px; color: #00ff88; text-decoration: none; 
            font-weight: bold; transition: 0.3s; padding: 10px 20px; border: 1px solid #00ff88; border-radius: 8px;
        }
        .back-link:hover { background: #00ff88; color: #000; transform: translateY(-2px); }
        .back-link:active { transform: scale(0.95); }
    </style>
</head>
<body>
    <h1>Privacy Policy</h1>
    <p>Last updated: March 2026</p>
    <p>We prioritize your privacy. Font Flow does not collect personal data from our users.</p>
    <h2>1. Data Usage</h2>
    <p>All text generated is processed locally and not stored on our servers.</p>
    <h2>2. Cookies</h2>
    <p>We use Google AdSense and Analytics, which use cookies to provide a better service.</p>
    <a href="/" class="back-link">← Back to Home</a>
</body>
</html>
"""

@app.route('/')
def index():
    user_text = request.args.get('text', '')
    extra_fonts = get_dynamic_fonts(user_text) if user_text else []
    return render_template_string(INDEX_HTML, extra_fonts=extra_fonts)

@app.route('/privacy')
def privacy():
    return render_template_string(PRIVACY_HTML)

@app.route('/ads.txt')
def ads_txt():
    return "google.com, pub-2712778222245542, DIRECT, f08c47fec0942fa0", 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
