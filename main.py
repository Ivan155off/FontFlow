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

COMMON_STYLE = """
<style>
    :root { --p: #00ff88; --s: #bd00ff; --bg: #080808; }
    * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; outline: none; }
    body {
        background: var(--bg); color: #fff; font-family: 'Inter', sans-serif;
        margin: 0; min-height: 100vh; display: flex; flex-direction: column; align-items: center;
        padding: 15px; overflow-x: hidden;
    }
    .bg-blobs {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        z-index: -1; overflow: hidden; filter: blur(80px); opacity: 0.3;
    }
    .blob { position: absolute; width: 300px; height: 300px; border-radius: 50%; animation: move 20s infinite alternate; }
    .blob1 { background: var(--p); top: -10%; left: -10%; }
    .blob2 { background: var(--s); bottom: -10%; right: -10%; animation-delay: -5s; }
    @keyframes move { from { transform: translate(0,0); } to { transform: translate(100px, 100px); } }
    
    .container { width: 100%; max-width: 550px; text-align: center; z-index: 1; padding: 0 10px; }
    .fade-in { animation: fadeIn 0.8s cubic-bezier(0.4, 0, 0.2, 1) forwards; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }

    h1 {
        font-family: 'Syncopate', sans-serif; font-size: clamp(1.8rem, 8vw, 2.8rem);
        background: linear-gradient(90deg, var(--p), var(--s));
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 8px; filter: drop-shadow(0 0 15px rgba(0,255,136,0.4));
    }
    .content-box { 
        background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); 
        padding: 25px 20px; border-radius: 24px; text-align: left; margin-top: 25px;
        backdrop-filter: blur(12px); transition: all 0.4s ease;
    }
    
    .back-btn, footer a {
        display: inline-block;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .back-btn:active, footer a:active {
        transform: scale(0.9) !important;
        opacity: 0.7;
    }

    .back-btn {
        margin-top: 35px; padding: 14px 28px; border: 1px solid var(--p);
        color: var(--p); text-decoration: none; border-radius: 14px; font-weight: 900;
        text-transform: uppercase;
    }
    .back-btn:hover { background: var(--p); color: #000; transform: translateY(-4px); box-shadow: 0 8px 20px rgba(0,255,136,0.2); }

    footer { margin-top: 40px; padding-bottom: 20px; font-size: 0.8rem; opacity: 0.6; }
    
    /* ОБНОВЛЕННАЯ АНИМАЦИЯ ДЛЯ ССЫЛОК В ФУТЕРЕ */
    footer a { color: #aaa; text-decoration: none; margin: 0 10px; }
    footer a:hover { 
        color: var(--p); 
        transform: scale(1.15); /* Увеличиваем при наведении */
        text-shadow: 0 0 10px rgba(0,255,136,0.5);
    }

    @media (max-width: 768px) {
        body { padding: 10px; }
        .container { max-width: 100%; padding: 0 5px; }
        .content-box { padding: 20px 15px; margin-top: 20px; }
        h1 { font-size: clamp(1.5rem, 7vw, 2.2rem); margin-bottom: 15px; }
    }
</style>
"""

INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Font Flow — Stylish Text Generator & Aesthetic Fonts</title>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2712778222245542" crossorigin="anonymous"></script>
    <link href="https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Inter:wght@400;600;900&display=swap" rel="stylesheet">
    """ + FAVICON + COMMON_STYLE + """
    <style>
        textarea {
            width: 100%; padding: 22px; border-radius: 18px; background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.1); color: #fff; font-size: 1.15rem; outline: none; transition: 0.4s;
            backdrop-filter: blur(10px); resize: vertical; min-height: 120px;
        }
        textarea:focus { border-color: var(--p); background: rgba(255,255,255,0.07); box-shadow: 0 0 30px rgba(0,255,136,0.15); }
        .ad-slot { width: 100%; min-height: 90px; margin: 20px 0; background: rgba(255,255,255,0.01); border-radius: 12px; overflow: hidden; }
        .results { margin-top: 25px; display: grid; gap: 14px; width: 100%; }
        
        .card {
            background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05);
            padding: 18px 24px; border-radius: 16px; display: flex; justify-content: space-between;
            align-items: center; cursor: pointer; transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .card:hover { transform: translateY(-2px); border-color: var(--p); background: rgba(255,255,255,0.04); }
        .card:active { transform: scale(0.98); }
        
        .card span { font-size: 1.25rem; text-align: left; word-break: break-word; }
        
        .copy-btn { 
            background: rgba(255,255,255,0.08); color: #fff; padding: 10px 18px; 
            border-radius: 12px; font-weight: 800; font-size: 0.75rem;
            transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            min-width: 85px; text-align: center;
        }
        .card:hover .copy-btn { background: var(--p); color: #000; }
        
        .copied .copy-btn { 
            background: var(--s) !important; 
            color: #fff !important;
            transform: scale(1.1);
            box-shadow: 0 0 20px var(--s);
        }

        .underline span { text-decoration: underline; }
        .strikethrough span { text-decoration: line-through; }
        
        @media (max-width: 768px) {
            .card { padding: 16px 20px; flex-direction: column; text-align: center; gap: 12px; }
            .card span { font-size: 1.1rem; }
        }
    </style>
</head>
<body class="fade-in">
    <div class="bg-blobs"><div class="blob blob1"></div><div class="blob blob2"></div></div>
    <div class="container">
        <h1>FONT FLOW</h1>
        <p style="color:#aaa; margin-bottom:25px;">Stylish text for social media and games</p>
        
        <textarea id="input" placeholder="Type or paste your text..."></textarea>
        
        <div class="ad-slot">
            <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-2712778222245542" data-ad-slot="auto" data-ad-format="auto" data-full-width-responsive="true"></ins>
            <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
        </div>

        <div id="output" class="results"></div>
        
        <footer>
            <a href="/about">About</a>
            <a href="/contact">Contact</a>
            <a href="/privacy">Privacy</a>
            <p style="opacity: 0.3; margin-top: 15px; font-size: 0.75rem;">© 2026 Font Flow</p>
        </footer>
    </div>
    <script>
        const FONTS = {
            "Italic": "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻",
            "Bold": "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳",
            "Monospace": "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂ＴＵＶＷＸＹ𝚉𝚊𝚋𝚌𝚍ｅｆ𝚐ｈ𝚒𝚓𝚔𝚕𝕞𝚗𝚘𝚙𝚚𝚛𝘴𝘵𝚞𝚠𝚡𝚢𝚣",
            "Bubbles": "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ",
            "Small Caps": "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ",
            "Upside": "ɐqɔpǝɟƃɥᴉɾʞꞁɯuodbɹsʇnʌʍxʎzⱯᗷᑐᗡEᖵᘐHIᘀKꞀWNOᗡᑐᖴS⊥∩ΛM᙭⅄Z",
            "Script": "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓓𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓸𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃",
            "Fraktur": "𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ𝔞𝔟𝔠𝔡𝔢𝔣𝔫𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷"
        };
        const alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
        const input = document.getElementById('input');
        const output = document.getElementById('output');

        function copyDynamic(el, text) {
            navigator.clipboard.writeText(text);
            el.classList.add('copied');
            const btn = el.querySelector('.copy-btn');
            btn.innerText = "COPIED!";
            setTimeout(() => { 
                el.classList.remove('copied'); 
                btn.innerText = "COPY"; 
            }, 1200);
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
                content += `<div class='card' onclick="copyDynamic(this, '${res.replace(/'/g, "\\'")}')"><span>${res}</span><div class='copy-btn'>COPY</div></div>`;
            }
            content += `<div class='card strikethrough' onclick="copyDynamic(this, '${val.replace(/'/g, "\\'")}')"><span>${val}</span><div class='copy-btn'>COPY</div></div>`;
            content += `<div class='card underline' onclick="copyDynamic(this, '${val.replace(/'/g, "\\'")}')"><span>${val}</span><div class='copy-btn'>COPY</div></div>`;
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
    <link href="https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Inter:wght@400;600;900&display=swap" rel="stylesheet">
    """ + FAVICON + COMMON_STYLE + """
</head>
<body class="fade-in">
    <div class="bg-blobs"><div class="blob blob1"></div><div class="blob blob2"></div></div>
    <div class="container">
        <h1>ABOUT US</h1>
        <div class="content-box">
            <p>Welcome to <strong>Font Flow</strong>. I am a student from <strong>Ukraine</strong> who is passionate about coding and creating visual tools.</p>
            <p>I started this project to learn modern web technologies like <strong>Python, Flask, and JavaScript</strong>. My goal was to create a clean, fast, and free generator for everyone.</p>
            <p>I believe in simple tools that respect user privacy. Font Flow is a part of my journey to becoming a professional developer.</p>
        </div>
        <a href="/" class="back-btn">← Back to home</a>
        <footer>
            <a href="/contact">Contact</a>
            <a href="/privacy">Privacy</a>
            <p style="opacity: 0.3; margin-top: 15px; font-size: 0.75rem;">© 2026 Font Flow</p>
        </footer>
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
    <link href="https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Inter:wght@400;600;900&display=swap" rel="stylesheet">
    """ + FAVICON + COMMON_STYLE + """
</head>
<body class="fade-in">
    <div class="bg-blobs"><div class="blob blob1"></div><div class="blob blob2"></div></div>
    <div class="container">
        <h1>CONTACT</h1>
        <div class="content-box" style="text-align: center;">
            <p>Feedback or business inquiries?</p>
            <p style="color: var(--p); font-weight: 900; font-size: clamp(1.1rem, 4vw, 1.25rem); margin: 25px 0; word-break: break-all;">fontflow.help@gmail.com</p>
            <p style="font-size: 0.85rem; color: #777;">I usually respond within 24 hours.</p>
        </div>
        <a href="/" class="back-btn">← Back to home</a>
        <footer>
            <a href="/about">About</a>
            <a href="/privacy">Privacy</a>
            <p style="opacity: 0.3; margin-top: 15px; font-size: 0.75rem;">© 2026 Font Flow</p>
        </footer>
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
    <link href="https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Inter:wght@400;600;900&display=swap" rel="stylesheet">
    """ + FAVICON + COMMON_STYLE + """
    <style>
        h2 { color: var(--p); font-size: clamp(1.1rem, 3.5vw, 1.3rem); margin: 30px 0 20px 0; border-bottom: 1px solid rgba(0,255,136,0.1); padding-bottom: 10px; }
        p, li { color: #aaa; font-size: clamp(0.85rem, 2.5vw, 0.95rem); line-height: 1.7; margin-bottom: 15px; }
        strong { color: #fff; }
        ul { padding-left: 20px; text-align: left; margin: 10px 0; }
        @media (min-width: 769px) { .container { max-width: 800px; } }
    </style>
</head>
<body class="fade-in">
    <div class="bg-blobs"><div class="blob blob1"></div><div class="blob blob2"></div></div>
    <div class="container">
        <h1 style="text-align: center;">PRIVACY POLICY</h1>
        <div class="content-box">
            <p><i>Last Updated: March 25, 2026</i></p>
            <p>At <strong>Font Flow</strong>, we are committed to protecting the privacy of our visitors. This policy document outlines the types of information we handle.</p>
            <h2>1. Our Mission: Zero Data Collection</h2>
            <p>We believe your data is your business. Font Flow is designed as a client-side tool. This means all font transformations happen <strong>locally in your browser</strong>. We do not upload your text to our servers, we do not store it, and we do not share it.</p>
            <h2>2. Children's Online Privacy Protection</h2>
            <p>Protecting children's safety online is our absolute priority. Font Flow is designed to be a safe, clean utility for users of all ages.</p>
            <h2>3. Log Files and Analytics</h2>
            <p>Font Flow follows a standard procedure of using log files. We use <strong>Google Analytics</strong> to anonymously monitor traffic.</p>
            <h2>4. Third-Party Ads (Google AdSense)</h2>
            <p>To keep Font Flow free, we use Google AdSense. Google may use cookies to serve ads based on your visit.</p>
            <h2>5. Contact Us</h2>
            <p>If you have any questions regarding this detailed Privacy Policy, please reach us at <strong>fontflow.help@gmail.com</strong>.</p>
        </div>
        <div style="text-align: center;"><a href="/" class="back-btn">← Back to home</a></div>
        <footer>
            <a href="/about">About</a>
            <a href="/contact">Contact</a>
            <p style="opacity: 0.3; margin-top: 15px; font-size: 0.75rem;">© 2026 Font Flow</p>
        </footer>
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
