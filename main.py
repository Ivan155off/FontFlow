from flask import Flask, render_template_string
import os
import json

app = Flask(__name__)

# Твои шрифты
FONTS_DATA = {
    "Cyber": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
    "Bubbles": "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ",
    "Magic": "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳",
    "Ghost": "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷w𝘹𝘺𝘻",
    "Knight": "𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔚𝔛𝔜ℨ𝔞𝔟𝔠𝔡𝔢𝔣𝔫𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷",
    "Retro": "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ"
}

# Мы используем замену строк вручную, чтобы Python не ругался на скобки и проценты
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FONT FLOW | Ultimate Style</title>
    
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2712778222245542" crossorigin="anonymous"></script>
    
    <link href="https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Inter:wght@400;600;900&family=Noto+Sans+Symbol&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --p: #00ff88; --s: #bd00ff; --bg: #050505;
        }

        body {
            background: #000; color: #fff; font-family: 'Inter', 'Noto Sans Symbol', sans-serif;
            margin: 0; min-height: 100vh; display: flex; flex-direction: column; align-items: center;
            overflow-x: hidden; padding-bottom: 100px;
        }

        /* Анимированный фон */
        .bg-glow {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: radial-gradient(circle at 50% 50%, #1a1a1a 0%, #000 100%);
            z-index: -1;
        }
        
        .blob {
            position: absolute; width: 500px; height: 500px; background: var(--p);
            filter: blur(150px); opacity: 0.1; border-radius: 50%;
            animation: move 20s infinite alternate; z-index: -1;
        }

        @keyframes move { from { transform: translate(-30%, -30%); } to { transform: translate(30%, 30%); } }

        .container { width: 90%; max-width: 800px; text-align: center; margin-top: 80px; }

        h1 {
            font-family: 'Syncopate', sans-serif; font-size: 4rem; margin: 0;
            background: linear-gradient(to right, var(--p), var(--s));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 0 20px rgba(0,255,136,0.3));
        }

        .tagline { letter-spacing: 5px; color: #555; font-weight: 900; margin-bottom: 50px; font-size: 0.8rem; }

        textarea {
            width: 100%; padding: 30px; border-radius: 25px; background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.1); color: #fff; font-size: 1.5rem;
            outline: none; transition: 0.5s; backdrop-filter: blur(10px);
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        }

        textarea:focus { border-color: var(--p); box-shadow: 0 0 40px rgba(0,255,136,0.2); background: rgba(255,255,255,0.05); }

        .results { margin-top: 50px; display: grid; gap: 20px; width: 100%; }

        .card {
            background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05);
            padding: 30px; border-radius: 20px; display: flex; justify-content: space-between;
            align-items: center; transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            animation: reveal 0.6s ease forwards; opacity: 0;
        }

        @keyframes reveal { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }

        .card:hover {
            background: rgba(255,255,255,0.05); border-color: var(--s);
            transform: scale(1.03) translateY(-5px); box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        }

        .card span { font-size: 1.8rem; font-weight: 600; color: #eee; word-break: break-all; text-align: left; flex: 1; }

        .copy-btn {
            background: var(--p); color: #000; padding: 10px 20px; border-radius: 12px;
            font-weight: 900; font-size: 0.7rem; text-transform: uppercase;
            cursor: pointer; transition: 0.3s; margin-left: 20px;
        }

        .card:hover .copy-btn { transform: rotate(-3deg); box-shadow: 0 0 20px var(--p); }

        .ad-slot { width: 100%; background: rgba(255,255,255,0.01); border: 1px dashed #222; margin: 40px 0; min-height: 100px; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #333; }
    </style>
</head>
<body>
    <div class="bg-glow"></div>
    <div class="blob"></div>

    <div class="ad-slot">TOP AD ADVERTISING</div>

    <div class="container">
        <h1>FONT FLOW</h1>
        <div class="tagline">STYLE YOUR DIGITAL SOUL</div>
        
        <textarea id="input" placeholder="Enter text to stylize..." oninput="update()"></textarea>

        <div class="results" id="output"></div>

        <div class="ad-slot" style="min-height: 250px;">BOTTOM AD ADVERTISING</div>
    </div>

    <script>
        const maps = JSON_DATA_HERE;
        const normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";

        function update() {
            const val = document.getElementById('input').value;
            const output = document.getElementById('output');
            output.innerHTML = "";
            if(!val) return;

            Object.keys(maps).forEach((key, i) => {
                let res = "";
                for(let c of val) {
                    let idx = normal.indexOf(c);
                    res += idx !== -1 ? maps[key][idx] : c;
                }
                
                const div = document.createElement('div');
                div.className = 'card';
                div.style.animationDelay = (i * 0.1) + 's';
                div.onclick = () => {
                    navigator.clipboard.writeText(res);
                    const btn = div.querySelector('.copy-btn');
                    btn.innerText = "COPIED!";
                    btn.style.background = "#fff";
                    setTimeout(() => { btn.innerText = "COPY"; btn.style.background = "#00ff88"; }, 1000);
                };
                div.innerHTML = `<span>${res}</span><div class="copy-btn">COPY</div>`;
                output.appendChild(div);
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    # Безопасно вставляем данные без использования % или f-строк
    return HTML_CONTENT.replace("JSON_DATA_HERE", json.dumps(FONTS_DATA))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
