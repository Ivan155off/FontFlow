from flask import Flask, render_template_string, request
import os
import json

app = Flask(__name__)

# --- ЛОГИКА ШРИФТОВ (ПОЛНАЯ) ---
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

# --- ГЛОБАЛЬНЫЕ СТИЛИ И АНИМАЦИИ ---
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
    
    .container { width: 100%; max-width: 650px; text-align: center; z-index: 1; }
    
    .fade-in { animation: fadeIn 0.8s cubic-bezier(0.4, 0, 0.2, 1) forwards; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }

    h1 {
        font-family: 'Syncopate', sans-serif; font-size: clamp(2rem, 10vw, 2.8rem);
        background: linear-gradient(90deg, var(--p), var(--s));
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 10px; filter: drop-shadow(0 0 15px rgba(0,255,136,0.4));
    }

    .content-box { 
        background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); 
        padding: 30px; border-radius: 24px; text-align: left; margin-top: 25px;
        backdrop-filter: blur(12px); transition: all 0.4s ease;
    }
    .content-box:hover { border-color: var(--p); transform: scale(1.01); background: rgba(255,255,255,0.04); }

    .back-btn {
        display: inline-block; margin-top: 35px; padding: 14px 28px; border: 1px solid var(--p);
        color: var(--p); text-decoration: none; border-radius: 14px; font-weight: 900;
        text-transform: uppercase; letter-spacing: 1px; font-size: 0.8rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .back-btn:hover { background: var(--p); color: #000; transform: translateY(-4px) scale(1.05); box-shadow: 0 8px 25px rgba(0,255,136,0.4); }
    .back-btn:active { transform: scale(0.95); }

    footer { margin-top: 60px; padding: 30px 0; width: 100%; border-top: 1px solid rgba(255,255,255,0.05); text-align: center; }
    footer a { 
        color: #777; text-decoration: none; margin: 0 15px; font-size: 0.9rem; 
        transition: all 0.3s ease; display: inline-block; font-weight: 500;
    }
    footer a:hover { color: var(--p); transform: translateY(-3px); }
</style>
"""

INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Font Flow — Aesthetic Text Generator</title>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2712778222245542" crossorigin="anonymous"></script>
    <link href="https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Inter:wght@400;600;900&display=swap" rel="stylesheet">
    """ + FAVICON + COMMON_STYLE + """
    <style>
        textarea {
            width: 100%; padding: 22px; border-radius: 18px; background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.1); color: #fff; font-size: 1.15rem; outline: none; transition: 0.4s;
            backdrop-filter: blur(10px); box-shadow: inset 0 2px 10px rgba(0,0,0,0.5);
        }
        textarea:focus { border-color: var(--p); background: rgba(255,255,255,0.07); box-shadow: 0 0 30px rgba(0,255,136,0.15); }

        .results { margin-top: 30px; display: grid; gap: 14px; width: 100%; }
        .card {
            background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05);
            padding: 18px 24px; border-radius: 16px; display: flex; justify-content: space-between;
            align-items: center; cursor: pointer; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .card:hover { transform: scale(1.03) translateX(10px); border-color: var(--p); background: rgba(255,255,255,0.06); }
        .card:active { transform: scale(0.97); }
        
        .copy-btn { 
            background: rgba(255,255,255,0.1); color: #fff; padding: 10px 18px; 
            border-radius: 12px; font-weight: 800; font-size: 0.75rem; transition: 0.3s;
        }
        .card:hover .copy-btn { background: var(--p); color: #000; box-shadow: 0 0 15px rgba(0,255,136,0.5); }
        .copied .copy-btn { background: var(--s) !important; color: #fff !important; }

        .strike span { text-decoration: line-through; }
        .underline span { text-decoration: underline; }
    </style>
</head>
<body class="fade-in">
    <div class="bg-blobs"><div class="blob blob1"></div><div class="blob blob2"></div></div>
    <div class="container">
        <h1>FONT FLOW</h1>
        <p style="color:#888; margin-bottom:30px; font-weight:500;">Transform your text into aesthetic art</p>
        
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

        <div class="content-box">
            <h2 style="color:var(--p); font-size:1.2rem; margin-top:0;">Why Use Font Flow?</h2>
            <p style="color:#aaa; line-height:1.7; font-size:0.9rem;">Our tool generates unique combinations that work perfectly for <b>Discord</b>, <b>Roblox</b>, or <b>Social Media</b>. No installation required — just copy and paste!</p>
        </div>

        <footer>
            <a href="/about">About</a>
            <a href="/contact">Contact</a>
            <a href="/privacy">Privacy</a>
            <p style="opacity: 0.2; margin-top: 20px; font-size: 0.75rem;">© 2026 Font Flow. All Rights Reserved.</p>
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
            el.querySelector('.copy-btn').innerText = "COPIED!";
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
    <title>About Us - Font Flow</title>
    """ + FAVICON + COMMON_STYLE + """
</head>
<body class="fade-in">
    <div class="container">
        <h1>ABOUT US</h1>
        <div class="content-box">
            <p>Welcome to <strong>Font Flow</strong>. I am a student from <strong>Ukraine</strong> who is passionate about coding and creating aesthetic web tools.</p>
            <p>I started this project to learn modern web technologies like <strong>Python and JavaScript</strong>. My goal was to create a clean, fast, and free font generator for gamers and social media creators.</p>
            <p>I believe in a web where tools are simple, useful, and respect user privacy. Font Flow is a part of my journey to becoming a developer.</p>
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
            <p>Feedback or suggestions?</p>
            <p>Email me at:</p>
            <p style="color: var(--p); font-weight: 900; font-size: 1.2rem; margin: 25px 0;">support@fontflow.onrender.com</p>
            <p style="font-size: 0.85rem; color: #777;">I usually respond within 48 hours.</p>
        </div>
        <a href="/" class="back-btn">← Back to Generator</a>
    </div>
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
    """ + FAVICON + COMMON_STYLE + """
    <style>
        h2 { color: var(--p); font-size: 1.3rem; margin-top: 30px; border-bottom: 1px solid rgba(0,255,136,0.1); padding-bottom: 10px; }
        p, li { color: #aaa; font-size: 0.95rem; line-height: 1.8; margin-bottom: 15px; }
        strong { color: #fff; }
        ul { padding-left: 20px; text-align: left; }
    </style>
</head>
<body class="fade-in">
    <div class="container" style="max-width: 800px; text-align: left;">
        <h1 style="text-align: center;">PRIVACY POLICY</h1>
        <div class="content-box">
            <p><i>Last Updated: March 24, 2026</i></p>
            <p>At <strong>Font Flow</strong>, we are committed to protecting the privacy and safety of our users. This detailed policy explains how we handle data and our dedication to internet safety.</p>

            <h2>1. Our Privacy Mission: Zero-Data Collection</h2>
            <p>We operate on a "Privacy-First" principle. Font Flow is a client-side tool, meaning all font transformations happen <strong>locally on your computer or phone</strong>. The text you input is never uploaded, stored, or processed on our servers. We believe your creative text is your business, not ours.</p>

            <h2>2. Children's Online Privacy Protection (COPPA)</h2>
            <p>Protecting children online is our absolute priority. Font Flow is designed to be a safe, clean environment for users of all ages, including children under 13.</p>
            <ul>
                <li><strong>No Registration Required:</strong> We never ask for names, emails, ages, or any personal identification.</li>
                <li><strong>No Profile Building:</strong> We do not track individual behavior or create "user profiles" of any kind.</li>
                <li><strong>Strict Ad Filtering:</strong> We strive to ensure that any advertisements shown are family-friendly and comply with COPPA regulations regarding tracking.</li>
            </ul>
            <p>If you are a parent and believe your child has accidentally provided personal information, please contact us immediately for its removal.</p>

            <h2>3. Transparency on Log Files</h2>
            <p>Like almost every website, our hosting provider (Render) automatically collects standard log files. This information includes IP addresses, browser types, Internet Service Providers (ISP), and date/time stamps. This data is strictly used for technical maintenance, preventing bot attacks, and ensuring the website stays online. This information is <strong>not</strong> linked to your personal identity.</p>

            <h2>4. Third-Party Services (Google AdSense/Analytics)</h2>
            <p>To keep this tool free, we use Google AdSense to show advertisements and Google Analytics to understand site traffic. These partners may use cookies or web beacons to serve ads based on your visit to this and other sites. You can choose to disable cookies in your browser settings or visit the Google Ad Settings page to manage your preferences.</p>

            <h2>5. Data Security</h2>
            <p>Even though we do not collect personal text, we secure our website using SSL (HTTPS) encryption to ensure that your connection to our generator is safe and cannot be intercepted by third parties.</p>

            <h2>6. User Rights & GDPR</h2>
            <p>If you are a resident of the European Economic Area (EEA), you have rights regarding your data. Since we do not collect personal data (like names or emails), we have no data to "delete" or "transfer." However, you have the right to browse anonymously and manage your cookie settings at any time.</p>

            <h2>7. External Links</h2>
            <p>Our website may contain links to other sites. We are not responsible for the content or privacy practices of those external websites. We encourage you to read their policies before providing any information.</p>

            <h2>8. Contacting Us</h2>
            <p>If you have any questions about this massive policy or how we protect your privacy, feel free to reach out to us at <strong>support@fontflow.onrender.com</strong>. We are always happy to clarify our practices.</p>
        </div>
        <div style="text-align: center;">
            <a href="/" class="back-btn">← Back to Generator</a>
        </div>
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
