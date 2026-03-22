from flask import Flask, render_template_string, request
import os
import json

app = Flask(__name__)

# --- ПОЛНАЯ ЛОГИКА ДЛЯ ВСЕХ ШРИФТОВ ---
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

FAVICON = '<link rel="icon" href="data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 100 100\'><text y=\'.9em\' font-size=\'90\'>🚀</text></svg>">'

INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Font Flow — Stylish Text Generator & Aesthetic Fonts</title>
    <meta name="description" content="Create unique nicknames and stylish text for Discord, Telegram, and Social Media.">
    
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
        .card span { font-size: 1.2rem; text-align: left; flex: 1; padding-right: 15px; overflow-wrap: anywhere; }
        
        .copy-btn { 
            background: rgba(255,255,255,0.08); color: #fff; padding: 8px 16px; 
            border-radius: 10px; font-weight: 700; font-size: 0.7rem; 
            text-transform: uppercase; transition: 0.3s; min-width: 85px; text-align: center;
        }
        .card:hover .copy-btn { background: var(--p); color: #000; }
        .copied .copy-btn { background: var(--s) !important; color: #fff !important; }

        .seo-content { margin-top: 40px; text-align: left; padding: 20px; background: rgba(255,255,255,0.02); border-radius: 15px; border: 1px solid rgba(255,255,255,0.05); }
        .seo-content h2 { color: var(--p); font-size: 1.1rem; margin-top: 15px; }
        .seo-content p { color: #888; font-size: 0.85rem; line-height: 1.5; }
        
        footer { margin-top: 40px; padding-bottom: 20px; font-size: 0.8rem; opacity: 0.6; }
        footer a { color: #aaa; text-decoration: none; border-bottom: 1px solid #444; transition: 0.3s; }
        footer a:hover { color: var(--p); border-bottom-color: var(--p); }
    </style>
</head>
<body>
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

        <div class="seo-content">
            <h2>What is Font Flow?</h2>
            <p>Font Flow is a powerful online aesthetic text generator. We provide a wide range of fancy letters and cool symbols that you can copy and paste into your Discord, Telegram, or Instagram profiles. Our tool uses Unicode characters to ensure your stylish nicknames work across all modern platforms.</p>
            <h2>How to generate fancy fonts?</h2>
            <p>Simply type your text in the box above. Our algorithm will instantly create font combinations, including italic, bold, monospace, and many aesthetic styles. Click "Copy" to use the result anywhere instantly!</p>
        </div>

        <footer>
            © 2026 Font Flow | <a href="/privacy">Privacy Policy</a>
        </footer>
    </div>

    <script>
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
        body { background: #080808; color: #aaa; font-family: 'Inter', sans-serif; line-height: 1.8; padding: 40px 20px; max-width: 850px; margin: 0 auto; }
        h1 { color: #00ff88; font-size: 2.2rem; border-bottom: 2px solid #1a1a1a; padding-bottom: 10px; }
        h2 { color: #fff; margin-top: 40px; border-left: 4px solid #00ff88; padding-left: 15px; font-size: 1.4rem; }
        .box { background: rgba(0,255,136,0.05); border: 1px solid rgba(0,255,136,0.2); padding: 20px; border-radius: 12px; margin: 25px 0; }
        .back-btn { display: inline-block; margin-bottom: 30px; color: #00ff88; text-decoration: none; font-weight: bold; border: 1px solid #00ff88; padding: 8px 18px; border-radius: 8px; transition: 0.3s; }
        .back-btn:hover { background: #00ff88; color: #000; }
        li { margin-bottom: 10px; }
    </style>
</head>
<body>
    <a href="/" class="back-btn">← Back to Home</a>
    <h1>Privacy Policy for Font Flow</h1>
    <p><strong>Last updated:</strong> March 22, 2026</p>

    <p>At Font Flow, we are committed to maintaining the trust and confidence of our visitors. This Privacy Policy details how we handle data in compliance with GDPR, CCPA, and COPPA.</p>

    <h2>1. Consent</h2>
    <p>By using our website, you hereby consent to our Privacy Policy and agree to its terms.</p>

    <h2>2. Information We Collect</h2>
    <p>We do not require any registration. We may collect information only when you contact us directly or via automated server logs (IP address, browser type, referring pages).</p>

    <h2>3. How We Use Information</h2>
    <p>We use the information to maintain the website, prevent fraud, analyze user behavior, and improve our font conversion algorithms.</p>

    <h2>4. Log Files</h2>
    <p>Font Flow follows a standard procedure of using log files. These files log visitors when they visit websites. This information is anonymous and used for technical administration.</p>

    <h2>5. Cookies and Web Beacons</h2>
    <p>We use cookies to store information about visitors' preferences and to customize our web page content based on browser type.</p>

    <h2>6. Google DART Cookie</h2>
    <p>Google uses DART cookies to serve ads to our users. You can opt out of these by visiting the Google ad privacy policy.</p>

    <h2>7. Advertising Partners</h2>
    <p>Our advertising partners (like Google AdSense) use cookies and web beacons to measure the effectiveness of their ads. We have no access to these third-party cookies.</p>

    <h2>8. GDPR Data Protection Rights</h2>
    <p>Users in the EU have the right to access, rectification, erasure, and restriction of processing of their data.</p>

    <h2>9. CCPA Privacy Rights</h2>
    <p>California consumers have the right to request disclosure of what data is collected and to request its deletion.</p>

    <div class="box">
        <h2>10. Children's Privacy (COPPA)</h2>
        <p>Font Flow does not knowingly collect any Personal Identifiable Information from children under the age of 13. If you believe your child has provided such info, contact us immediately for its removal.</p>
        <ul>
            <li>No accounts or social features for children.</li>
            <li>No tracking of personal identities.</li>
            <li>Safe Unicode-based text processing.</li>
        </ul>
    </div>

    <h2>11. Data Security</h2>
    <p>We use industry-standard security protocols. However, no internet transmission is 100% secure.</p>

    <h2>12. Contact Information</h2>
    <p>For any privacy-related questions, please contact the site administrator via the contact details provided on the main page.</p>

    <p style="text-align:center; margin-top:50px; opacity:0.5;">© 2026 Font Flow Project</p>
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
