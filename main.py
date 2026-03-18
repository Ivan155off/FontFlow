from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Твой уникальный ID AdSense
ADSENSE_CLIENT = "ca-pub-2712778222245542"

# База данных шрифтов
FONTS_DATA = {
    "Vibe": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
    "Bubbles": "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ",
    "Bold": "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳",
    "Italic": "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘈𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻",
    "Gothic": "𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔚𝔛𝔜ℨ𝔞𝔟𝔠𝔡𝔢𝔣𝔫𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷",
    "Square": "🄰🄱🄲🄳🄴🄵🄿🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅶🅇🅈🅉🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅶🅇🅈🅉",
    "Wide": "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ"
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FontFlow | Ultra Fancy Text Generator</title>
    
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2712778222245542" crossorigin="anonymous"></script>
    
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Noto+Sans+Symbol&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --bg: #030303;
            --primary: #00ff88;
            --secondary: #bd00ff;
            --card-bg: rgba(20, 20, 20, 0.6);
            --border: rgba(255, 255, 255, 0.08);
            --text: #ffffff;
            --text-dim: #888888;
        }

        @keyframes bgMove { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
        @keyframes glow { from { text-shadow: 0 0 10px var(--primary); } to { text-shadow: 0 0 25px var(--primary); } }
        @keyframes slideIn { from { opacity: 0; transform: translateX(-20px); } to { opacity: 1; transform: translateX(0); } }

        body { 
            background: linear-gradient(-45deg, #050505, #121212, #050505, #000);
            background-size: 400% 400%; animation: bgMove 15s ease infinite; 
            color: var(--text); font-family: 'Inter', 'Noto Sans Symbol', sans-serif; 
            margin: 0; display: flex; flex-direction: column; align-items: center; min-height: 100vh;
            padding: 80px 20px; box-sizing: border-box; overflow-x: hidden;
        }

        .ad-banner { width: 100%; max-width: 970px; min-height: 90px; background: rgba(255,255,255,0.01); border: 1px dashed rgba(255,255,255,0.05); margin-bottom: 30px; display: flex; align-items: center; justify-content: center; color: #333; font-size: 10px; text-transform: uppercase; letter-spacing: 2px; }
        .ad-side { position: fixed; top: 50%; transform: translateY(-50%); width: 160px; height: 600px; background: rgba(255,255,255,0.01); border: 1px dashed rgba(255,255,255,0.05); display: flex; align-items: center; justify-content: center; color: #333; font-size: 10px; z-index: 10; text-transform: uppercase; letter-spacing: 2px; }
        .ad-left { left: 20px; }
        .ad-right { right: 20px; }
        .ad-bottom { width: 100%; max-width: 970px; min-height: 250px; margin-top: 50px; background: rgba(255,255,255,0.01); border: 1px dashed rgba(255,255,255,0.05); display: flex; align-items: center; justify-content: center; color: #333; font-size: 10px; text-transform: uppercase; letter-spacing: 2px; }

        @media (max-width: 1400px) { .ad-side { display: none; } }

        .container { max-width: 700px; width: 100%; text-align: center; position: relative; z-index: 5; }
        
        h1 { 
            color: var(--primary); font-size: clamp(2.5rem, 8vw, 4.5rem); font-weight: 900; 
            letter-spacing: -3px; margin: 0 0 10px 0; animation: glow 2s infinite alternate; 
            background: linear-gradient(90deg, var(--primary), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .tagline { color: var(--text-dim); font-size: 1rem; margin-bottom: 50px; text-transform: uppercase; letter-spacing: 3px; font-weight: 700; }
        
        textarea { 
            width: 100%; padding: 25px; border-radius: 20px; background: var(--card-bg); 
            backdrop-filter: blur(15px); border: 1px solid var(--border); color: var(--text); 
            font-size: 1.4rem; resize: none; outline: none; transition: 0.4s; box-sizing: border-box;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5); font-family: 'Inter', sans-serif;
        }
        textarea:focus { border-color: var(--primary); box-shadow: 0 0 30px rgba(0,255,136,0.3); background: rgba(25, 25, 25, 0.8); }

        .results { margin-top: 40px; display: grid; gap: 18px; }
        
        .card { 
            background: var(--card-bg); backdrop-filter: blur(10px); padding: 25px; border-radius: 18px; 
            border: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; 
            transition: 0.3s cubic-bezier(0.2, 0.8, 0.2, 1); cursor: pointer; animation: slideIn 0.5s ease both;
        }
        .card:hover { border-color: var(--secondary); background: rgba(30, 0, 40, 0.7); transform: translateY(-5px) scale(1.01); box-shadow: 0 15px 40px rgba(189,0,255,0.15); }
        
        .card span { font-size: 1.6rem; color: var(--text); font-weight: 500; word-break: break-all; text-align: left; padding-right: 15px; flex: 1; }
        .copy-btn { 
            color: var(--primary); font-size: 0.75rem; text-transform: uppercase; font-weight: 900; 
            letter-spacing: 1px; transition: 0.2s; background: rgba(0,255,136,0.1); padding: 8px 15px; border-radius: 8px;
            white-space: nowrap;
        }
        .card:hover .copy-btn { color: #fff; background: var(--secondary); transform: scale(1.05); }
        
    </style>
</head>
<body>
    <div class="ad-banner">Top Ad Space</div>
    <div class="ad-side ad-left">Side Ad Left</div>
    <div class="ad-side ad-right">Side Ad Right</div>

    <div class="container">
        <h1>FONT FLOW</h1>
        <div class="tagline">Elevate Your Social Text</div>
        
        <textarea id="input" placeholder="Type or paste your text here..." oninput="update()"></textarea>
        
        <div class="results" id="output"></div>
        
        <div class="ad-bottom">Bottom Ad Space</div>
    </div>

    <script>
        const fontMaps = %s;
        const fontKeys = Object.keys(fontMaps);
        const normalChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";

        function update() {
            const val = document.getElementById('input').value;
            const output = document.getElementById('output');
            output.innerHTML = "";

            if(!val) return;

            fontKeys.forEach((f, index) => {
                let transformed = "";
                for(let char of val) {
                    let idx = normalChars.indexOf(char);
                    transformed += idx !== -1 ? fontMaps[f][idx] : char;
                }
                
                const card = document.createElement('div');
                card.className = 'card';
                card.style.animationDelay = (index * 0.05) + "s";
                
                card.onclick = () => copyText(transformed, card);
                card.innerHTML = `<span>${transformed}</span><div class="copy-btn">Copy</div>`;
                output.appendChild(card);
            });
        }

        function copyText(text, card) {
            navigator.clipboard.writeText(text);
            const btn = card.querySelector('.copy-btn');
            btn.innerText = "COPIED!";
            btn.style.color = "#fff";
            btn.style.background = "#00ff88";
            setTimeout(() => { 
                btn.innerText = "Copy"; 
                btn.style.color = "var(--primary)"; 
                btn.style.background = "rgba(0,255,136,0.1)"; 
            }, 1500);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    import json
    return render_template_string(HTML_TEMPLATE % json.dumps(FONTS_DATA))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
