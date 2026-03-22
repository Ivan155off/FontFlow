from flask import Flask, render_template_string, request
import os
import json

app = Flask(__name__)

# --- ЛОГИКА ДЛЯ НОВЫХ ШРИФТОВ ---
def get_dynamic_fonts(text):
    try:
        base_path = os.path.dirname(__file__)
        json_path = os.path.join(base_path, 'fonts.json')
        
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

# Общая иконка для всех страниц
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
        .card:active { transform: scale(0.98); }
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
        footer a { 
            color: #aaa; text-decoration: none; display: inline-block; transition: all 0.3s ease; 
            border-bottom: 1px solid transparent;
        }
        footer a:hover { color: var(--p); border-bottom-color: var(--p); transform: translateY(-1px); }
        footer a:active { transform: scale(0.9); }

        /* --- ВСПЛЫВАЮЩЕЕ ОКНО (POPUP) --- */
        #privacy-popup {
            position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
            width: 90%; max-width: 400px; background: rgba(15, 15, 15, 0.95);
            border: 1px solid var(--p); border-radius: 15px; padding: 20px;
            z-index: 9999; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            backdrop-filter: blur(10px); display: none; text-align: center;
        }
        #privacy-popup p { font-size: 0.85rem; color: #ccc; margin-bottom: 15px; line-height: 1.4; }
        #privacy-popup a { color: var(--p); text-decoration: none; font-weight: bold; }
        #privacy-popup button {
            background: var(--p); color: #000; border: none; padding: 10px 25px;
            border-radius: 8px; font-weight: 900; cursor: pointer; transition: 0.3s;
        }
        #privacy-popup button:hover { background: #fff; transform: scale(1.05); }
    </style>
</head>
<body>
    <div class="bg-blobs"><div class="blob blob1"></div><div class="blob blob2"></div></div>
    
    <div id="privacy-popup">
        <p>By using Font Flow, you agree to our <a href="/privacy">Privacy Policy</a>. We use cookies to ensure you get the best experience on our website.</p>
        <button onclick="acceptPrivacy()">OK, GOT IT!</button>
    </div>

    <div class="container">
        <h1>FONT FLOW</h1>
        <div class="description">Elevate your style for social media and games</div>
        
        <textarea id="input" placeholder="Type your text here..."></textarea>
        
        <div class="ad-box">
            <ins class="adsbygoogle"
                 style="display:block"
                 data-ad-client="ca-pub-2712778222245542"
                 data-ad-slot="auto"
                 data-ad-format="auto"
                 data-full-width-responsive="true"></ins>
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
        // ЛОГИКА ОКНА (ПОКАЗЫВАЕМ ТОЛЬКО ПЕРВЫЙ РАЗ)
        if (!localStorage.getItem('privacyAccepted')) {
            document.getElementById('privacy-popup').style.display = 'block';
        }
        function acceptPrivacy() {
            localStorage.setItem('privacyAccepted', 'true');
            document.getElementById('privacy-popup').style.display = 'none';
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
            const CSS_FONTS = { "Strike": "strikethrough", "Underline": "underline" };
            for (const key in CSS_FONTS) {
                oldContent += `<div class='card ${CSS_FONTS[key]}' onclick="copyDynamic(this, '${val}')"><span>${val}</span><div class='copy-btn'>COPY</div></div>`;
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
        h1 { color: #00ff88; font-family: sans-serif; }
        h2 { color: #fff; margin-top: 30px; border-left: 4px solid #bd00ff; padding-left: 15px; }
        p { margin-bottom: 20px; color: #aaa; }
        ul { color: #aaa; margin-bottom: 20px; }
        li { margin-bottom: 10px; }
        .back-link { 
            display: inline-block; margin-top: 40px; color: #00ff88; text-decoration: none; 
            font-weight: bold; transition: all 0.3s ease; padding: 10px 20px; border: 1px solid #00ff88; border-radius: 8px;
        }
        .back-link:hover { background: #00ff88; color: #000; transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,255,136,0.3); }
    </style>
</head>
<body>
    <h1>Privacy Policy for Font Flow</h1>
    <p>Last updated: March 21, 2026</p>
    
    <p>Your privacy is critically important to us. This Privacy Policy document outlines the types of personal information that is received and collected by Font Flow and how it is used.</p>

    <h2>1. General Information</h2>
    <p>Font Flow is a free online tool for generating stylish text. We do not require registration, accounts, or any personal details (such as names, emails, or phone numbers) to use our service.</p>

    <h2>2. Log Files</h2>
    <p>Like many other websites, Font Flow makes use of log files. The information inside the log files includes internet protocol (IP) addresses, type of browser, Internet Service Provider (ISP), date/time stamp, referring/exit pages, and number of clicks. This information is used to analyze trends, administer the site, and track user’s movement around the site. IP addresses and other such information are not linked to any information that is personally identifiable.</p>

    <h2>3. Cookies and Web Beacons</h2>
    <p>Font Flow uses cookies to store information about visitors' preferences, to record user-specific information on which pages the site visitor accesses or visits, and to personalize or customize our web page content based upon visitors' browser type or other information that the visitor sends via their browser.</p>

    <h2>4. Advertising Partners (Google AdSense)</h2>
    <p>Google, as a third-party vendor, uses cookies to serve ads on Font Flow. Google's use of the DART cookie enables it to serve ads to our users based on their visit to our site and other sites on the Internet. Users may opt out of the use of the DART cookie by visiting the Google ad and content network privacy policy.</p>

    <h2>5. Google Analytics</h2>
    <p>We use Google Analytics to understand how the site is used and to improve user experience. All data is aggregated and completely anonymous.</p>

    <h2>6. Children's Privacy Protection (COPPA Compliance)</h2>
    <p>Protecting the privacy of the very young is especially important. For that reason, Font Flow never collects or maintains information at our website from those we actually know are under 13, and no part of our website is structured to attract anyone under 13.</p>
    <ul>
        <li><strong>No Personal Data Collection:</strong> We do not ask for, collect, or store any personal identification from any user, including children.</li>
        <li><strong>No Account Creation:</strong> There are no profiles or accounts, which prevents children from sharing personal details.</li>
        <li><strong>Parental Control:</strong> If a parent or guardian believes that Font Flow has in its database the personal information of a child under the age of 13, please contact us immediately, and we will use our best efforts to promptly remove such information from our records.</li>
    </ul>

    <h2>7. Policy Updates</h2>
    <p>We reserve the right to update this policy at any time. We encourage visitors to frequently check this page for any changes.</p>

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
    content = "google.com, pub-2712778222245542, DIRECT, f08c47fec0942fa0"
    return content, 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
