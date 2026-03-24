from flask import Flask, render_template_string, request
import os
import json

app = Flask(__name__)

# --- ПОЛНАЯ ЛОГИКА ШРИФТОВ ---
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

# --- ОБЩИЕ СТИЛИ С АНИМАЦИЯМИ ДЛЯ ВСЕХ СТРАНИЦ ---
COMMON_STYLE = """
<style>
    :root { --p: #00ff88; --s: #bd00ff; --bg: #080808; }
    * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; outline: none; }
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
    
    /* Анимация появления контента */
    .fade-in { animation: fadeIn 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

    h1 {
        font-family: 'Syncopate', sans-serif; font-size: clamp(2rem, 10vw, 2.5rem);
        background: linear-gradient(90deg, var(--p), var(--s));
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 8px; filter: drop-shadow(0 0 15px rgba(0,255,136,0.4));
    }

    .content-box { 
        background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); 
        padding: 25px; border-radius: 20px; text-align: left; margin-top: 20px;
        backdrop-filter: blur(10px); transition: 0.3s;
    }
    .content-box:hover { border-color: rgba(0,255,136,0.2); background: rgba(255,255,255,0.03); }

    .back-btn {
        display: inline-block; margin-top: 30px; padding: 12px 25px; border: 1px solid var(--p);
        color: var(--p); text-decoration: none; border-radius: 12px; font-weight: bold;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .back-btn:hover { background: var(--p); color: #000; transform: translateY(-3px); box-shadow: 0 5px 20px rgba(0,255,136,0.3); }
    .back-btn:active { transform: scale(0.92); }

    footer { margin-top: 60px; padding: 20px 0; width: 100%; border-top: 1px solid rgba(255,255,255,0.05); text-align: center; }
    footer a { 
        color: #666; text-decoration: none; margin: 0 12px; font-size: 0.85rem; 
        transition: all 0.3s ease; display: inline-block;
    }
    footer a:hover { color: var(--p); transform: translateY(-2px); }
    footer a:active { transform: scale(0.9); }
</style>
"""

INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Font Flow — Stylish Text Generator</title>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-P4Q7YLZLBC"></script>
    <script> window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', 'G-P4Q7YLZLBC'); </script>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2712778222245542" crossorigin="anonymous"></script>
    <link href="https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Inter:wght@400;600;900&display=swap" rel="stylesheet">
    """ + FAVICON + COMMON_STYLE + """
    <style>
        textarea {
            width: 100%; padding: 20px; border-radius: 15px; background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.1); color: #fff; font-size: 1.1rem; outline: none; transition: 0.4s;
            backdrop-filter: blur(10px);
        }
        textarea:focus { border-color: var(--p); background: rgba(255,255,255,0.06); box-shadow: 0 0 20px rgba(0,255,136,0.1); }

        .results { margin-top: 25px; display: grid; gap: 12px; width: 100%; }
        .card {
            background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05);
            padding: 16px 20px; border-radius: 14px; display: flex; justify-content: space-between;
            align-items: center; cursor: pointer; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .card:hover { transform: translateX(8px); border-color: var(--p); background: rgba(255,255,255,0.05); }
        .card:active { transform: scale(0.96); }
        
        .copy-btn { 
            background: rgba(255,255,255,0.08); color: #fff; padding: 8px 16px; 
            border-radius: 10px; font-weight: 700; font-size: 0.7rem; 
            text-transform: uppercase; transition: 0.3s; min-width: 85px; text-align: center;
        }
        .card:hover .copy-btn { background: var(--p); color: #000; }
        .copied .copy-btn { background: var(--s) !important; color: #fff !important; }

        .strike span { text-decoration: line-through; }
        .underline span { text-decoration: underline; }
    </style>
</head>
<body class="fade-in">
    <div class="bg-blobs"><div class="blob blob1"></div><div class="blob blob2"></div></div>
    <div class="container">
        <h1>FONT FLOW</h1>
        <div style="color:#aaa; font-size:0.9rem; margin-bottom:25px;">Stylish fonts for social media and games</div>
        
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

        <div class="content-box" style="margin-top:50px;">
            <h2 style="color:var(--p); font-size:1.1rem; margin-top:0;">What is Font Flow?</h2>
            <p style="color:#888; font-size:0.85rem; line-height:1.6;">Font Flow is a powerful aesthetic text generator. Use fancy letters and cool symbols for Discord, Telegram, or Instagram. Our tool uses Unicode characters to work across all modern platforms.</p>
        </div>

        <footer>
            <a href="/">Home</a>
            <a href="/about">About</a>
            <a href="/contact">Contact</a>
            <a href="/privacy">Privacy</a>
            <p style="opacity: 0.3; margin-top: 15px; font-size: 0.7rem;">© 2026 Font Flow Project</p>
        </footer>
    </div>

    <script>
        const FONTS = {
            "Italic": "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻",
            "Bold": "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳",
            "Monospace": "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅Ｗ𝚇𝚈𝚉𝚊𝚋𝚌𝚍ｅ𝚏𝚐ｈ𝚒𝚓𝚔𝚕𝕞𝚗𝚘𝚙𝚚𝚛𝘴𝚝𝚞𝚠𝚡𝚢𝚣",
            "Bubbles": "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ",
            "Small Caps": "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ",
            "Upside": "ɐqɔpǝɟƃɥᴉɾʞꞁɯuodbɹsʇnʌʍxʎzⱯᗷᑐᗡEᖵᘐHIᘀKꞀWNOᗡᑐᖴS⊥∩ΛM᙭⅄Z",
            "Script": "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓓𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃",
            "Fraktur": "𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ𝔞𝔟𝔠𝔡𝔢𝔣𝔫𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷"
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
            }, 1000);
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
            oldContent += `<div class='card strike' onclick="copyDynamic(this, '${val}')"><span>${val}</span><div class='copy-btn'>COPY</div></div>`;
            oldContent += `<div class='card underline' onclick="copyDynamic(this, '${val}')"><span>${val}</span><div class='copy-btn'>COPY</div></div>`;
            output.innerHTML = oldContent;
        };
    </script>
</body>
</html>
"""

ABOUT_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About - Font Flow</title>
    """ + FAVICON + COMMON_STYLE + """
</head>
<body class="fade-in">
    <div class="container">
        <h1>ABOUT US</h1>
        <div class="content-box">
            <p>Welcome to <strong>Font Flow</strong>. I am a student from <strong>Ukraine</strong> who is passionate about building tools that help people express themselves online.</p>
            <p>Living in <strong>Kharkiv</strong>, I spend my time learning Python and web technologies. This site is my first big step in creating useful web applications for the gaming and social media community.</p>
            <p>I believe that even a small tool like a font generator can make someone's digital experience more fun and personal.</p>
        </div>
        <a href="/" class="back-btn">← Back to Generator</a>
    </div>
</body>
</html>
"""

CONTACT_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact - Font Flow</title>
    """ + FAVICON + COMMON_STYLE + """
</head>
<body class="fade-in">
    <div class="container">
        <h1>CONTACT</h1>
        <div class="content-box" style="text-align: center;">
            <p>Have questions or suggestions?</p>
            <p>Feel free to reach out via email:</p>
            <p style="color: var(--p); font-weight: bold; font-size: 1.1rem; margin: 20px 0;">support@fontflow.onrender.com</p>
            <p style="font-size: 0.8rem; opacity: 0.7;">I try to reply to everyone as soon as possible.</p>
        </div>
        <a href="/" class="back-btn">← Back to Generator</a>
    </div>
</body>
</html>
"""

# ВЕРНУЛ ТЕКСТ PRIVACY POLICY ЧТОБЫ НЕ БЫЛО ОШИБКИ
PRIVACY_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Privacy Policy - Font Flow</title>
    """ + FAVICON + COMMON_STYLE + """
    <style>h2{color:var(--p); font-size:1.1rem; margin-top:20px;} li{margin-bottom:10px; color:#aaa; font-size:0.9rem;}</style>
</head>
<body class="fade-in">
    <div class="container">
        <h1>PRIVACY POLICY</h1>
        <div class="content-box">
            <p>At Font Flow, we take your privacy seriously. This policy explains what data we handle.</p>
            <h2>1. No Data Collection</h2>
            <p>The text you type in our generator is processed <strong>locally</strong> in your browser. We do not store your text on our servers.</p>
            <h2>2. Cookies and Ads</h2>
            <p>We use Google AdSense and Google Analytics. These services may use cookies to show relevant ads and analyze site traffic.</p>
            <h2>3. Children's Privacy</h2>
            <p>We do not knowingly collect personal data from children. Since we don't have accounts, your identity remains anonymous.</p>
        </div>
        <a href="/" class="back-btn">← Back to Generator</a>
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
