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

INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Font Flow — Stylish Text Generator & Aesthetic Fonts</title>
    <meta name="description" content="Create unique nicknames and stylish text for Discord, Telegram, and Social Media. Copy and paste aesthetic fonts, fancy letters, and cool symbols.">
    
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-P4Q7YLZLBC"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-P4Q7YLZLBC');
    </script>
    
    <meta name="google-site-verification" content="OO6lpx6rkPkflDspe23xGNja4sRaQ3yb0Z3JoKuy5kE" />
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
        
        .ad-box { width: 100%; min-height: 50px; margin: 10px 0; border-radius: 10px; background: rgba(255,255,255,0.01); overflow: hidden; }

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
            backdrop-filter: blur(5px);
        }
        .card:hover { transform: translateY(-2px); border-color: var(--p); background: rgba(255,255,255,0.05); }
        .card span { font-size: 1.2rem; text-align: left; flex: 1; padding-right: 15px; overflow-wrap: anywhere; }
        .copy-btn { 
            background: rgba(255,255,255,0.08); color: #fff; padding: 8px 16px; 
            border-radius: 10px; font-weight: 700; font-size: 0.7rem; 
            text-transform: uppercase; transition: 0.3s; min-width: 85px; text-align: center;
        }
        .card:hover .copy-btn { background: var(--p); color: #000; }
        .copied .copy-btn { background: var(--s) !important; color: #fff !important; }

        /* SEO CONTENT BLOCK */
        .seo-info { margin-top: 50px; text-align: left; padding: 25px; background: rgba(255,255,255,0.02); border-radius: 20px; border: 1px solid rgba(255,255,255,0.05); }
        .seo-info h2 { color: var(--p); font-size: 1.2rem; margin-top: 20px; }
        .seo-info p, .seo-info li { color: #888; font-size: 0.9rem; line-height: 1.6; }

        /* PRIVACY POPUP */
        #privacy-modal {
            position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
            width: 90%; max-width: 450px; background: #121212; border: 1px solid var(--p);
            padding: 20px; border-radius: 15px; z-index: 1000; box-shadow: 0 10px 40px rgba(0,0,0,0.8);
            display: none; animation: slideUp 0.4s ease-out;
        }
        @keyframes slideUp { from { transform: translate(-50%, 100%); } to { transform: translate(-50%, 0); } }
        #privacy-modal p { font-size: 0.85rem; color: #ccc; margin: 0 0 15px; }
        #privacy-modal a { color: var(--p); text-decoration: none; font-weight: bold; }
        #privacy-modal button { 
            width: 100%; padding: 12px; border: none; border-radius: 10px; 
            background: var(--p); color: #000; font-weight: bold; cursor: pointer; transition: 0.3s;
        }
        #privacy-modal button:hover { background: #fff; }

        footer { margin-top: 40px; padding-bottom: 20px; font-size: 0.8rem; opacity: 0.6; }
        footer a { color: #aaa; text-decoration: none; border-bottom: 1px solid transparent; transition: 0.3s; }
        footer a:hover { color: var(--p); border-bottom-color: var(--p); }
    </style>
</head>
<body>
    <div class="bg-blobs"><div class="blob blob1"></div><div class="blob blob2"></div></div>
    
    <div id="privacy-modal">
        <p>We care about your privacy. We use cookies to improve your experience and show relevant ads. By continuing, you agree to our <a href="/privacy">Privacy Policy</a>.</p>
        <button onclick="acceptPrivacy()">I Understand</button>
    </div>

    <div class="container">
        <h1>FONT FLOW</h1>
        <div class="description">Elevate your style for social media and games</div>
        
        <textarea id="input" placeholder="Type your text here..."></textarea>
        
        <div class="ad-box">
            <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-2712778222245542" data-ad-slot="auto" data-ad-format="auto" data-full-width-responsive="true"></ins>
            <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
        </div>

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

        <div class="seo-info">
            <h2>About Font Flow Aesthetic Text</h2>
            <p>Font Flow is more than just a font generator; it's a creative tool designed to help you express your unique identity across the digital landscape. In an era where everyone uses the same standard fonts, our platform allows you to stand out.</p>
            <h2>How it works?</h2>
            <p>Our algorithm takes your standard input and maps it to a vast library of <strong>Unicode characters</strong>. This means the fonts you generate here aren't just "styling" — they are actual characters that can be read by almost any app, including:</p>
            <ul>
                <li>Discord profiles and server names</li>
                <li>Telegram bios and channel descriptions</li>
                <li>Instagram bios and captions</li>
                <li>TikTok usernames and nicknames</li>
            </ul>
            <p>Simply type your text, explore dozens of artistic variations like <em>Italic</em>, <strong>Bold</strong>, or Ⓐⓔⓢⓣⓗⓔⓣⓘⓒ, and click to copy. No installation or registration required.</p>
        </div>

        <footer>
            © 2026 Font Flow | <a href="/privacy">Privacy Policy</a>
        </footer>
    </div>

    <script>
        // Privacy Logic
        if (!localStorage.getItem('privacy_accepted')) {
            document.getElementById('privacy-modal').style.display = 'block';
        }
        function acceptPrivacy() {
            localStorage.setItem('privacy_accepted', 'true');
            document.getElementById('privacy-modal').style.display = 'none';
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

# PRIVACY_HTML оставляем без изменений, как в твоем коде выше
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
        h1 { color: #00ff88; font-family: sans-serif; }
        h2 { color: #fff; margin-top: 30px; border-left: 4px solid #bd00ff; padding-left: 15px; }
        .back-link { display: inline-block; margin-top: 40px; color: #00ff88; text-decoration: none; font-weight: bold; border: 1px solid #00ff88; padding: 10px 20px; border-radius: 8px; }
    </style>
</head>
<body>
    <h1>Privacy Policy for Font Flow</h1>
    <p>Last updated: March 21, 2026</p>
    <p>Your privacy is critically important to us. This document outlines how we collect data.</p>
    <h2>1. General Information</h2>
    <p>Font Flow is a free tool. We do not require registration or personal details.</p>
    <h2>2. Log Files</h2>
    <p>We use standard log files (IP, browser type) for site analysis.</p>
    <a href="/" class="back-link">← Back to Home</a>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
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
