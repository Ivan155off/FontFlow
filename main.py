from flask import Flask, render_template_string
import os
import json

app = Flask(__name__)

# База данных шрифтов (строго задана)
FONTS_DATA = {
    "Vibe": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
    "Bubbles": "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ",
    "Bold": "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳",
    "Italic": "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷w𝘹𝘺𝘻",
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
    <title>FontFlow | Fancy Text Generator</title>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2712778222245542" crossorigin="anonymous"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Noto+Sans+Symbol&display=swap" rel="stylesheet">
    <style>
        :root { --bg: #030303; --primary: #00ff88; --secondary: #bd00ff; --card-bg: rgba(20, 20, 20, 0.6); --border: rgba(255, 255, 255, 0.08); --text: #ffffff; }
        @keyframes bgMove { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
        @keyframes glow { from { text-shadow: 0 0 10px var(--primary); } to { text-shadow: 0 0 25px var(--primary); } }
        body { 
            background: linear-gradient(-45deg, #050505, #121212, #050505, #000);
            background-size: 400% 400%; animation: bgMove 15s ease infinite; 
            color: var(--text); font-family: 'Inter', 'Noto Sans Symbol', sans-serif; 
            margin: 0; display: flex; flex-direction: column; align-items: center; min-height: 100vh;
            padding: 40px 20px; box-sizing: border-box;
        }
        .container { max-width: 700px; width: 100%; text-align: center; z-index: 5; }
        h1 { color: var(--primary); font-size: 3.5rem; font-weight: 900; margin: 0; animation: glow 2s infinite alternate; }
        .tagline { color: #888; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 30px; font-size: 0.9rem; }
        textarea { 
            width: 100%; padding: 20px; border-radius: 15px; background: var(--card-bg); 
            border: 1px solid var(--border); color: white; font-size: 1.2rem; outline: none; transition: 0.3s;
        }
        textarea:focus { border-color: var(--primary); box-shadow: 0 0 20px rgba(0,255,136,0.2); }
        .results { margin-top: 30px; display: grid; gap: 15px; }
        .card { 
            background: var(--card-bg); padding: 20px; border-radius: 12px; border: 1px solid var(--border);
            display: flex; justify-content: space-between; align-items: center; cursor: pointer; transition: 0.2s;
        }
        .card:hover { border-color: var(--secondary); background: rgba(30, 30, 30, 0.8); transform: scale(1.02); }
        .card span { font-size: 1.4rem; word-break: break-all; text-align: left; flex: 1; padding-right: 10px; }
        .copy-btn { color: var(--primary); font-weight: bold; font-size: 0.8rem; text-transform: uppercase; background: rgba(0,255,136,0.1); padding: 5px 10px; border-radius: 5px; }
        .ad-box { width: 100%; background: rgba(255,255,255,0.02); border: 1px dashed #333; margin: 20px 0; min-height: 90px; display: flex; align-items: center; justify-content: center; color: #444; font-size: 10px; }
    </style>
</head>
<body>
    <div class="ad-box">TOP AD SPACE</div>
    <div class="container">
        <h1>FONT FLOW</h1>
        <div class="tagline">Upgrade Your Social Media Text</div>
        <textarea id="input" placeholder="Type something cool..." oninput="update()"></textarea>
        <div class="results" id="output"></div>
        <div class="ad-box" style="min-height: 250px;">BOTTOM AD SPACE</div>
    </div>
    <script>
        const fontMaps = %s;
        const normalChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
        function update() {
            const val = document.getElementById('input').value;
            const output = document.getElementById('output');
            output.innerHTML = "";
            if(!val) return;
            Object.keys(fontMaps).forEach(f => {
                let res = "";
                for(let c of val) {
                    let i = normalChars.indexOf(c);
                    res += i !== -1 ? fontMaps[f][i] : c;
                }
                const div = document.createElement('div');
                div.className = 'card';
                div.onclick = () => {
                    navigator.clipboard.writeText(res);
                    div.querySelector('.copy-btn').innerText = "COPIED!";
                    setTimeout(() => div.querySelector('.copy-btn').innerText = "COPY", 1000);
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
    return render_template_string(HTML_TEMPLATE % json.dumps(FONTS_DATA))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
