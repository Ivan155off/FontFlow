from flask import Flask, render_template_string, request
import os
import json

app = Flask(__name__)

# --- ПОЛНАЯ ЛОГИКА (БЕЗ ВЫРЕЗАНИЙ) ---
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

# ТВОЙ ОРИГИНАЛЬНЫЙ INDEX С ПОЛНЫМ НАБОРОМ ШРИФТОВ И АНИМАЦИЙ
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Font Flow — Stylish Text Generator & Aesthetic Fonts</title>
    
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
        .card:active { transform: scale(0.98); }
        
        .copy-btn { 
            background: rgba(255,255,255,0.08); color: #fff; padding: 8px 16px; 
            border-radius: 10px; font-weight: 700; font-size: 0.7rem; 
            text-transform: uppercase; transition: 0.3s; min-width: 85px; text-align: center;
        }
        .card:hover .copy-btn { background: var(--p); color: #000; }
        .copied .copy-btn { background: var(--s) !important; color: #fff !important; }

        /* ВЕРНУЛ ЭФФЕКТЫ */
        .strike span { text-decoration: line-through; }
        .underline span { text-decoration: underline; }

        .seo-content { margin-top: 40px; text-align: left; padding: 20px; background: rgba(255,255,255,0.02); border-radius: 15px; border: 1px solid rgba(255,255,255,0.05); }
        .seo-content h2 { color: var(--p); font-size: 1.1rem; margin-top: 15px; }
        .seo-content p { color: #888; font-size: 0.85rem; line-height: 1.5; }

        footer { margin-top: 40px; padding-bottom: 20px; font-size: 0.8rem; opacity: 0.6; }
        footer a { color: #aaa; text-decoration: none; margin: 0 10px; transition: 0.3s; }
        footer a:hover { color: var(--p); }
        
        /* КНОПКА НАЗАД ДЛЯ НОВЫХ СТРАНИЦ */
        .back-link { display: inline-block; margin-top: 30px; padding: 10px 20px; border: 1px solid var(--p); color: var(--p); text-decoration: none; border-radius: 10px; transition: 0.3s; }
        .back-link:hover { background: var(--p); color: #000; }
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
            <h2>Frequently Asked Questions</h2>
            <p><strong>How to use?</strong> Just type your text and click copy. Our generator uses Unicode characters to ensure compatibility with Discord, Instagram, and TikTok.</p>
        </div>

        <footer>
            © 2026 Font Flow | <a href="/about">About</a> | <a href="/contact">Contact</a> | <a href="/privacy">Privacy</a>
        </footer>
    </div>

    <script>
        // ВЕРНУЛ ВСЕ 8+ ШРИФТОВ
        const FONTS = {
            "Italic": "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻",
            "Bold": "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳",
            "Monospace": "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄傳ＷＸＹ𝚉𝚊𝚋𝚌𝚍ｅ𝚏𝚐ｈ𝚒𝚓𝚔𝚕𝕞𝚗𝚘𝚙𝚚𝚛𝘴𝚝𝚞𝚠𝚡𝚢𝚣",
            "Bubbles": "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ",
            "Small Caps": "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ",
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
            // CSS СТИЛИ
            oldContent += `<div class='card strike' onclick="copyDynamic(this, '${val}')"><span>${val}</span><div class='copy-btn'>COPY</div></div>`;
            oldContent += `<div class='card underline' onclick="copyDynamic(this, '${val}')"><span>${val}</span><div class='copy-btn'>COPY</div></div>`;
            output.innerHTML = oldContent;
        };
    </script>
</body>
</html>
"""

# ВЕРНУЛ PRIVACY_HTML И ДОБАВИЛ НОВЫЕ СТРАНИЦЫ
ABOUT_HTML = """
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>About - Font Flow</title>""" + FAVICON + """
<style>body{background:#080808;color:#ccc;font-family:sans-serif;padding:40px;text-align:center;} .box{max-width:600px;margin:0 auto;background:rgba(255,255,255,0.02);padding:30px;border-radius:20px;border:1px solid rgba(255,255,255,0.05); text-align:left;} h1{color:#00ff88;} .back{display:inline-block;margin-top:20px;color:#00ff88;text-decoration:none;border:1px solid #00ff88;padding:10px 20px;border-radius:10px;}</style></head>
<body>
    <div class="box">
        <h1>About Project</h1>
        <p>I am a student from Ukraine, learning web development. Font Flow is my personal experiment with Python and Flask. I created it to help people make their social media profiles more unique.</p>
        <p>Everything you see here is processed in your browser. No data is stored, and no tracking is done beyond basic analytics to improve the tool.</p>
    </div>
    <a href="/" class="back">← Back</a>
</body>
</html>
"""

CONTACT_HTML = """
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Contact - Font Flow</title>""" + FAVICON + """
<style>body{background:#080808;color:#ccc;font-family:sans-serif;padding:40px;text-align:center;} .box{max-width:600px;margin:0 auto;background:rgba(255,255,255,0.02);padding:30px;border-radius:20px;border:1px solid rgba(255,255,255,0.05);} h1{color:#00ff88;} .back{display:inline-block;margin-top:20px;color:#00ff88;text-decoration:none;border:1px solid #00ff88;padding:10px 20px;border-radius:10px;}</style></head>
<body>
    <div class="box">
        <h1>Contact</h1>
        <p>Suggestions? Bug reports? Email me at:</p>
        <p style="color:#bd00ff; font-weight:bold;">support@fontflow.onrender.com</p>
    </div>
    <a href="/" class="back">← Back</a>
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
def privacy(): return render_template_string(PRIVACY_HTML) # (Тут твоя переменная PRIVACY_HTML)

@app.route('/ads.txt')
def ads_txt():
    return "google.com, pub-2712778222245542, DIRECT, f08c47fec0942fa0", 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
