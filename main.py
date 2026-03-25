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
    except Exception as e:
        print(f"Font error: {e}")
        return []

FAVICON = '<link rel="icon" href="data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 100 100\'><text y=\'.9em\' font-size=\'90\'>🚀</text></svg>">'

# ОБЩИЕ СТИЛИ С АДАПТИВНОСТЬЮ
COMMON_STYLE = """
<style>
    :root { --p: #00ff88; --s: #bd00ff; --bg: #080808; }
    * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; outline: none; }
    
    html, body { 
        width: 100%;
        overflow-x: hidden; /* Запрещаем горизонтальный скролл */
    }

    body {
        background: var(--bg); color: #fff; font-family: 'Inter', sans-serif;
        margin: 0; min-height: 100vh; display: flex; flex-direction: column; align-items: center;
        padding: 15px; /* Уменьшили паддинг для мобилок */
    }

    .bg-blobs {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        z-index: -1; overflow: hidden; filter: blur(80px); opacity: 0.2;
    }
    .blob { position: absolute; width: 250px; height: 250px; border-radius: 50%; animation: move 20s infinite alternate; }
    .blob1 { background: var(--p); top: -5%; left: -5%; }
    .blob2 { background: var(--s); bottom: -5%; right: -5%; animation-delay: -5s; }
    @keyframes move { from { transform: translate(0,0); } to { transform: translate(50px, 50px); } }
    
    .container { 
        width: 100%; 
        max-width: 600px; 
        text-align: center; 
        z-index: 1;
        padding: 0 5px;
    }

    .fade-in { animation: fadeIn 0.6s ease-out forwards; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

    h1 {
        font-family: 'Syncopate', sans-serif; 
        font-size: clamp(1.8rem, 8vw, 2.8rem); /* Адаптивный размер текста */
        background: linear-gradient(90deg, var(--p), var(--s));
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }

    .content-box { 
        background: rgba(255,255,255,0.03); 
        border: 1px solid rgba(255,255,255,0.08); 
        padding: clamp(15px, 5vw, 30px); 
        border-radius: 20px; 
        text-align: left; 
        margin-top: 20px;
        backdrop-filter: blur(15px);
        width: 100%;
        word-wrap: break-word; /* Чтобы длинные слова не ломали верстку */
    }

    .back-btn {
        display: inline-block; 
        margin-top: 30px; 
        padding: 12px 24px; 
        border: 1px solid var(--p);
        color: var(--p); 
        text-decoration: none; 
        border-radius: 12px; 
        font-weight: 800;
        text-transform: uppercase; 
        transition: 0.3s;
        font-size: 0.9rem;
    }
    .back-btn:hover { background: var(--p); color: #000; }

    footer { margin-top: 40px; padding-bottom: 20px; font-size: 0.8rem; opacity: 0.5; }
    footer a { color: #fff; text-decoration: none; margin: 0 10px; }

    /* Оптимизация для очень маленьких экранов */
    @media (max-width: 360px) {
        body { padding: 10px; }
        .back-btn { width: 100%; text-align: center; }
    }
</style>
"""

INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <title>Font Flow — Stylish Text Generator</title>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2712778222245542" crossorigin="anonymous"></script>
    <link href="https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Inter:wght@400;600;900&display=swap" rel="stylesheet">
    """ + FAVICON + COMMON_STYLE + """
    <style>
        textarea {
            width: 100%; padding: 18px; border-radius: 16px; background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1); color: #fff; font-size: 1rem; transition: 0.3s;
            resize: none; min-height: 120px;
        }
        textarea:focus { border-color: var(--p); background: rgba(255,255,255,0.08); }
        .ad-slot { width: 100%; min-height: 90px; margin: 15px 0; border-radius: 10px; overflow: hidden; }
        .results { display: grid; gap: 12px; width: 100%; margin-top: 10px; }
        .card {
            background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06);
            padding: 15px 20px; border-radius: 14px; display: flex; justify-content: space-between;
            align-items: center; cursor: pointer; transition: 0.2s; gap: 10px;
        }
        .card:active { transform: scale(0.98); background: rgba(255,255,255,0.05); }
        .card span { font-size: 1.15rem; word-break: break-all; text-align: left; }
        .copy-btn { 
            background: rgba(255,255,255,0.1); color: #fff; padding: 8px 14px; 
            border-radius: 8px; font-weight: 800; font-size: 0.7rem; min-width: 60px; text-align: center;
        }
        .copied .copy-btn { background: var(--p) !important; color: #000 !important; }
    </style>
</head>
<body class="fade-in">
    <div class="bg-blobs"><div class="blob blob1"></div><div class="blob blob2"></div></div>
    <div class="container">
        <h1>FONT FLOW</h1>
        <p style="color:#888; margin-bottom:20px; font-size: 0.9rem;">Stylish text for social media</p>
        
        <textarea id="input" placeholder="Type your text here..."></textarea>
        
        <div class="ad-slot">
            <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-2712778222245542" data-ad-slot="auto" data-ad-format="auto" data-full-width-responsive="true"></ins>
            <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
        </div>

        <div id="output" class="results"></div>
        
        <footer>
            <a href="/about">About</a> • <a href="/contact">Contact</a> • <a href="/privacy">Privacy</a>
            <p style="margin-top:15px; opacity: 0.3;">© 2026 Font Flow</p>
        </footer>
    </div>
    <script>
        const FONTS = {
            "Italic": "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘭𝘮𝘯ｵ𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻",
            "Bold": "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳",
            "Monospace": "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂ＴＵＶＷＸＹ𝚉𝚊𝚋𝚌𝚍ｅｆ𝚐ｈ𝚒𝚓𝚔𝚕𝕞𝚗𝚘𝚙𝚚𝚛𝘴𝘵𝚞𝚠𝚡𝚢𝚣",
            "Bubbles": "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ",
            "Small Caps": "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ",
            "Upside": "ɐqɔpǝɟƃɥᴉɾʞꞁɯuodbɹsʇnʌʍxʎzⱯᗷᑐᗡEᖵᘐHIᘀKꞀWNOᗡᑐᖴS⊥∩ΛM᙭⅄Z"
        };
        const alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
        const input = document.getElementById('input');
        const output = document.getElementById('output');

        function copyDynamic(el, text) {
            navigator.clipboard.writeText(text);
            el.classList.add('copied');
            el.querySelector('.copy-btn').innerText = "DONE";
            setTimeout(() => { el.classList.remove('copied'); el.querySelector('.copy-btn').innerText = "COPY"; }, 1000);
        }

        input.oninput = function() {
            const val = input.value;
            if(!val) { output.innerHTML = ""; return; }
            let content = "";
            for (const key in FONTS) {
                let res = "";
                let textToProcess = (key === "Upside") ? val.split("").reverse().join("") : val;
                for(let c of textToProcess) {
                    let i = alpha.indexOf(c);
                    res += (i !== -1 && FONTS[key][i]) ? FONTS[key][i] : c;
                }
                content += `<div class='card' onclick="copyDynamic(this, '${res}')"><span>${res}</span><div class='copy-btn'>COPY</div></div>`;
            }
            output.innerHTML = content;
        };
    </script>
</body>
</html>
"""

ABOUT_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About Us - Font Flow</title>
    """ + FAVICON + COMMON_STYLE + """
</head>
<body class="fade-in">
    <div class="container">
        <h1>ABOUT US</h1>
        <div class="content-box">
            <p>Welcome to <strong>Font Flow</strong>. I am a student from <strong>Ukraine</strong> who is passionate about coding.</p>
            <p>I created this project to learn <strong>Python and JavaScript</strong>. My goal was to create a clean, fast, and free generator for everyone.</p>
        </div>
        <a href="/" class="back-btn">← Back to home</a>
    </div>
</body>
</html>
"""

CONTACT_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact - Font Flow</title>
    """ + FAVICON + COMMON_STYLE + """
</head>
<body class="fade-in">
    <div class="container">
        <h1>CONTACT</h1>
        <div class="content-box" style="text-align: center;">
            <p>Suggestions or feedback?</p>
            <p style="color: var(--p); font-weight: 900; font-size: 1.2rem; margin: 20px 0;">fontflow.help@gmail.com</p>
        </div>
        <a href="/" class="back-btn">← Back to home</a>
    </div>
</body>
</html>
"""

PRIVACY_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Privacy Policy - Font Flow</title>
    """ + FAVICON + COMMON_STYLE + """
    <style>
        h2 { color: var(--p); font-size: 1.2rem; margin-top: 25px; }
        p, li { color: #aaa; font-size: 0.9rem; line-height: 1.6; }
    </style>
</head>
<body class="fade-in">
    <div class="container">
        <h1>PRIVACY POLICY</h1>
        <div class="content-box">
            <p><i>Last Updated: March 25, 2026</i></p>
            <h2>1. Data Usage</h2>
            <p>Font Flow is a client-side tool. All font transformations happen locally in your browser. We do not store or share your text.</p>
            <h2>2. Advertising</h2>
            <p>We use Google AdSense to show ads. Google may use cookies to serve ads based on your interests.</p>
            <h2>3. Contact</h2>
            <p>Questions? Reach us at <strong>fontflow.help@gmail.com</strong>.</p>
        </div>
        <a href="/" class="back-btn">← Back to home</a>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    user_text = request.args.get('text', '')
    extra_fonts = get_dynamic_fonts(user_text) if user_text else []
    return render_template_string(INDEX_HTML, extra_fonts=extra_fonts)

@app.route('/about')
def about(): return render_template_string(ABOUT_HTML)

@app.route('/contact')
def contact(): return render_template_string(CONTACT_HTML)

@app.route('/privacy')
def privacy(): return render_template_string(PRIVACY_HTML)

@app.route('/ads.txt')
def ads_txt():
    return "google.com, pub-2712778222245542, DIRECT, f08c47fec0942fa0", 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
