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

# --- ОБЩИЕ СТИЛИ (АНИМАЦИИ И ДИЗАЙН СОХРАНЕНЫ) ---
COMMON_STYLE = """
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
    .fade-in { animation: fadeIn 0.8s cubic-bezier(0.4, 0, 0.2, 1) forwards; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }

    h1 {
        font-family: 'Syncopate', sans-serif; font-size: clamp(2rem, 10vw, 2.5rem);
        background: linear-gradient(90deg, var(--p), var(--s));
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 8px; filter: drop-shadow(0 0 15px rgba(0,255,136,0.4));
    }
    .content-box { 
        background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); 
        padding: 30px; border-radius: 24px; text-align: left; margin-top: 25px;
        backdrop-filter: blur(12px); transition: all 0.4s ease;
    }
    .back-btn {
        display: inline-block; margin-top: 35px; padding: 14px 28px; border: 1px solid var(--p);
        color: var(--p); text-decoration: none; border-radius: 14px; font-weight: 900;
        text-transform: uppercase; transition: all 0.3s ease;
    }
    .back-btn:hover { background: var(--p); color: #000; transform: translateY(-3px); }

    footer { margin-top: 40px; padding-bottom: 20px; font-size: 0.8rem; opacity: 0.6; }
    footer a { color: #aaa; text-decoration: none; margin: 0 10px; transition: 0.3s; }
    footer a:hover { color: var(--p); }
</style>
"""

INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Font Flow — Stylish Text Generator</title>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2712778222245542" crossorigin="anonymous"></script>
    <link href="https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Inter:wght@400;600;900&display=swap" rel="stylesheet">
    """ + FAVICON + COMMON_STYLE + """
    <style>
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
        .copy-btn { background: rgba(255,255,255,0.08); color: #fff; padding: 8px 16px; border-radius: 10px; font-weight: 700; font-size: 0.7rem; }
        .card:hover .copy-btn { background: var(--p); color: #000; }
        .copied .copy-btn { background: var(--s) !important; color: #fff !important; }
        .underline span { text-decoration: underline; }
        .strikethrough span { text-decoration: line-through; }
    </style>
</head>
<body class="fade-in">
    <div class="bg-blobs"><div class="blob blob1"></div><div class="blob blob2"></div></div>
    <div class="container">
        <h1>FONT FLOW</h1>
        <p style="color:#888; margin-bottom:25px;">Elevate your style for social media and games</p>
        <textarea id="input" placeholder="Type your text here..."></textarea>
        <div id="output" class="results"></div>
        <footer>
            <a href="/about">About</a>
            <a href="/contact">Contact</a>
            <a href="/privacy">Privacy</a>
            <p style="margin-top:15px;">© 2026 Font Flow</p>
        </footer>
    </div>
    <script>
        const FONTS = {
            "Italic": "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻",
            "Bold": "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳",
            "Monospace": "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂ＴＵＶＷＸＹ𝚉𝚊𝚋𝚌𝚍ｅｆ𝚐ｈ𝚒𝚓𝚔𝚕𝕞𝚗𝚘𝚙𝚚𝚛𝘴𝚝𝚞𝚠𝚡𝚢𝚣",
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
            el.querySelector('.copy-btn').innerText = "DONE!";
            setTimeout(() => {
                el.classList.remove('copied');
                el.querySelector('.copy-btn').innerText = "COPY";
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
                    res += (i !== -1) ? FONTS[key][i] : c;
                }
                content += `<div class='card' onclick="copyDynamic(this, '${res}')"><span>${res}</span><div class='copy-btn'>COPY</div></div>`;
            }
            content += `<div class='card strikethrough' onclick="copyDynamic(this, '${val}')"><span>${val}</span><div class='copy-btn'>COPY</div></div>`;
            content += `<div class='card underline' onclick="copyDynamic(this, '${val}')"><span>${val}</span><div class='copy-btn'>COPY</div></div>`;
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
    <meta charset="UTF-8"><title>About Us - Font Flow</title>
    """ + FAVICON + COMMON_STYLE + """
</head>
<body class="fade-in">
    <div class="container">
        <h1>ABOUT US</h1>
        <div class="content-box">
            <p>Welcome to <strong>Font Flow</strong>. I am a student from <strong>Ukraine</strong> who is passionate about coding and digital tools.</p>
            <p>I started this project to learn <strong>Python and JavaScript</strong>. My goal was to create a clean, fast, and free generator for everyone.</p>
            <p>I believe in simple tools that respect user privacy. Font Flow is a result of my work to become a developer.</p>
        </div>
        <a href="/" class="back-btn">← Back to App</a>
    </div>
</body>
</html>
"""

CONTACT_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><title>Contact - Font Flow</title>
    """ + FAVICON + COMMON_STYLE + """
</head>
<body class="fade-in">
    <div class="container">
        <h1>CONTACT</h1>
        <div class="content-box" style="text-align: center;">
            <p>Suggestions or feedback?</p>
            <p style="color: var(--p); font-weight: 900; font-size: 1.2rem; margin: 20px 0;">support@fontflow.onrender.com</p>
            <p style="font-size: 0.8rem; color: #777;">I usually reply within 48 hours.</p>
        </div>
        <a href="/" class="back-btn">← Back to App</a>
    </div>
</body>
</html>
"""

PRIVACY_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><title>Privacy Policy - Font Flow</title>
    """ + FAVICON + COMMON_STYLE + """
    <style>
        h2 { color: var(--p); font-size: 1.2rem; margin-top: 25px; border-bottom: 1px solid rgba(0,255,136,0.1); padding-bottom: 5px; }
        p, li { color: #aaa; font-size: 0.9rem; line-height: 1.6; }
        ul { padding-left: 20px; text-align: left; }
    </style>
</head>
<body class="fade-in">
    <div class="container" style="max-width: 800px; text-align: left;">
        <h1 style="text-align: center;">PRIVACY POLICY</h1>
        <div class="content-box">
            <p><i>Last Updated: March 24, 2026</i></p>
            
            <h2>1. Zero-Data Collection</h2>
            <p>Font Flow works 100% on your device. We do not upload your text to any server. What you type stays in your browser.</p>

            <h2>2. Children's Privacy (COPPA Focus)</h2>
            <p>Protecting children is our top priority. Our site is safe for users of all ages:</p>
            <ul>
                <li><strong>No Accounts:</strong> We never ask for names, age, or emails.</li>
                <li><strong>No Tracking:</strong> We don't build profiles or track children's behavior.</li>
                <li><strong>Safe Environment:</strong> There is no chat or user-to-user interaction, making it 100% safe.</li>
            </ul>

            <h2>3. Third-Party Ads</h2>
            <p>We use Google AdSense. Google may use cookies to show ads based on your interests. You can turn off cookies in your browser at any time.</p>

            <h2>4. Analytics</h2>
            <p>We use Google Analytics to see how many people visit us. All data is anonymous and helps us improve the site.</p>

            <h2>5. Log Files</h2>
            <p>Like all sites, we use log files for security. This includes IP addresses and browser types, but they are not linked to your identity.</p>

            <h2>6. GDPR Compliance</h2>
            <p>For users in Europe: we don't collect personal data, so there is nothing to delete. You are always anonymous.</p>

            <h2>7. Security</h2>
            <p>We use SSL encryption to keep your connection to Font Flow safe.</p>

            <h2>8. Contact</h2>
            <p>If you have any privacy questions, email us at <strong>support@fontflow.onrender.com</strong>.</p>
        </div>
        <div style="text-align: center;"><a href="/" class="back-btn">← Back to App</a></div>
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
