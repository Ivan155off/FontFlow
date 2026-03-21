from flask import Flask, render_template_string, request
import os
import json

app = Flask(__name__)

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

# Иконка-ракета
FAVICON = '<link rel="icon" href="data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 100 100\'><text y=\'.9em\' font-size=\'90\'>🚀</text></svg>">'

INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Font Flow — Stylish Text Generator</title>
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
        .bg-blobs { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; filter: blur(80px); opacity: 0.3; }
        .blob { position: absolute; width: 300px; height: 300px; border-radius: 50%; animation: move 20s infinite alternate; }
        .blob1 { background: var(--p); top: -10%; left: -10%; }
        .blob2 { background: var(--s); bottom: -10%; right: -10%; animation-delay: -5s; }
        @keyframes move { from { transform: translate(0,0); } to { transform: translate(100px, 100px); } }
        
        .container { width: 100%; max-width: 550px; text-align: center; z-index: 1; }
        h1 { font-family: 'Syncopate', sans-serif; font-size: 2.5rem; background: linear-gradient(90deg, var(--p), var(--s)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px; }
        
        textarea {
            width: 100%; padding: 20px; border-radius: 15px; background: rgba(255,255,255,0.03); 
            border: 1px solid rgba(255,255,255,0.1); color: #fff; font-size: 1.1rem; outline: none; transition: 0.4s;
        }
        textarea:focus { border-color: var(--p); background: rgba(255,255,255,0.06); }
        
        .results { margin-top: 25px; display: grid; gap: 12px; width: 100%; }
        .card {
            background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05);
            padding: 16px 20px; border-radius: 14px; display: flex; justify-content: space-between;
            align-items: center; cursor: pointer; transition: 0.3s;
        }
        .card:hover { transform: translateY(-2px); border-color: var(--p); }
        .card:active { transform: scale(0.98); }
        
        .copy-btn { background: rgba(255,255,255,0.08); color: #fff; padding: 8px 16px; border-radius: 10px; font-weight: 700; font-size: 0.7rem; }
        .card:hover .copy-btn { background: var(--p); color: #000; }

        /* MODAL */
        #privacy-modal {
            position: fixed; bottom: -100%; left: 50%; transform: translateX(-50%);
            width: 90%; max-width: 400px; background: #111; border: 1px solid var(--p);
            border-radius: 20px; padding: 25px; z-index: 9999; transition: bottom 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        #privacy-modal.show { bottom: 30px; }
        .btn-accept { background: var(--p); border: none; padding: 12px; border-radius: 10px; font-weight: bold; cursor: pointer; width: 100%; margin-top: 15px; }
        .btn-decline { background: transparent; border: 1px solid #444; color: #888; padding: 8px; border-radius: 8px; cursor: pointer; margin-top: 10px; width: 100%; font-size: 0.8rem; }
        
        footer { margin-top: 40px; padding-bottom: 20px; font-size: 0.8rem; opacity: 0.6; }
        footer a { color: #aaa; text-decoration: none; transition: 0.3s; }
        footer a:hover { color: var(--p); }
    </style>
</head>
<body>
    <div id="privacy-modal">
        <h3 style="color:var(--p);margin:0">Privacy First</h3>
        <p style="font-size:0.85rem;color:#ccc">We use cookies to improve your experience. By using Font Flow, you agree to our <a href="/privacy" style="color:var(--p)">Privacy Policy</a>.</p>
        <button class="btn-accept" onclick="acceptPrivacy()">Accept & Continue</button>
        <button class="btn-decline" onclick="closeModal()">Decline</button>
    </div>

    <div class="bg-blobs"><div class="blob blob1"></div><div class="blob blob2"></div></div>
    <div class="container">
        <h1>FONT FLOW</h1>
        <textarea id="input" placeholder="Type your text..."></textarea>
        <div id="output" class="results"></div>
        <div style="margin-top:30px; text-align:left; font-size:0.85rem; color:#666; background:rgba(255,255,255,0.02); padding:15px; border-radius:10px;">
            <p>Simply type your text in the box above. Our algorithm will instantly create font combinations, including italic, bold, monospace, and many aesthetic styles. Click "Copy" to use the result anywhere instantly!</p>
        </div>
        <footer>© 2026 Font Flow | <a href="/privacy">Privacy Policy</a></footer>
    </div>

    <script>
        window.onload = function() {
            if (!localStorage.getItem('privacyAccepted')) {
                setTimeout(() => { document.getElementById('privacy-modal').classList.add('show'); }, 1000);
            }
        }
        function acceptPrivacy() { localStorage.setItem('privacyAccepted', 'true'); closeModal(); }
        function closeModal() { document.getElementById('privacy-modal').classList.remove('show'); }

        const FONTS = {
            "Italic": "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻",
            "Bold": "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳",
            "Bubbles": "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ"
        };
        const alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
        const input = document.getElementById('input');
        const output = document.getElementById('output');

        function copyDynamic(el, text) {
            navigator.clipboard.writeText(text);
            const btn = el.querySelector('.copy-btn');
            btn.innerText = "DONE!";
            setTimeout(() => { btn.innerText = "COPY"; }, 1000);
        }

        input.oninput = function() {
            const val = input.value;
            if(!val) { output.innerHTML = ""; return; }
            let resHtml = "";
            for (const key in FONTS) {
                let res = "";
                for(let c of val) {
                    let i = alpha.indexOf(c);
                    res += (i !== -1) ? FONTS[key][i] : c;
                }
                resHtml += `<div class='card' onclick="copyDynamic(this, '${res}')"><span>${res}</span><div class='copy-btn'>COPY</div></div>`;
            }
            output.innerHTML = resHtml;
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
        .back-link { display: inline-block; margin-top: 30px; color: #00ff88; text-decoration: none; border: 1px solid #00ff88; padding: 10px 20px; border-radius: 8px; transition: 0.3s; }
        .back-link:hover { background: #00ff88; color: #000; }
        .back-link:active { transform: scale(0.95); }
    </style>
</head>
<body>
    <h1>Privacy Policy</h1>
    <p>Last updated: March 2026</p>
    <p>Font Flow respects your privacy. We do not store any text you enter. Data collection is limited to basic technical analytics provided by Google to improve our service.</p>
    <h2>Cookies</h2>
    <p>We use essential cookies to remember your privacy preferences and for Google AdSense.</p>
    <a href="/" class="back-link">← Back to Home</a>
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
