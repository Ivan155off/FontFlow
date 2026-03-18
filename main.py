from flask import Flask, render_template_string
import os

app = Flask(__name__)

# Весь сайт в одной переменной - это исключает ошибки 500
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FONT FLOW | Style Generator</title>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2712778222245542" crossorigin="anonymous"></script>
    <link href="https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Inter:wght@400;700;900&family=Noto+Sans+Symbol&display=swap" rel="stylesheet">
    <style>
        :root { --p: #00ff88; --s: #bd00ff; }
        body {
            background: #000; color: #fff; font-family: 'Inter', 'Noto Sans Symbol', sans-serif;
            margin: 0; min-height: 100vh; display: flex; flex-direction: column; align-items: center;
            padding: 40px 20px;
        }
        .container { width: 100%; max-width: 600px; text-align: center; }
        h1 {
            font-family: 'Syncopate', sans-serif; font-size: 2.5rem;
            background: linear-gradient(90deg, var(--p), var(--s));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin-bottom: 10px; filter: drop-shadow(0 0 10px rgba(0,255,136,0.3));
        }
        .tagline { color: #444; letter-spacing: 3px; font-weight: 900; font-size: 0.7rem; margin-bottom: 30px; }
        textarea {
            width: 100%; padding: 20px; border-radius: 15px; background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1); color: #fff; font-size: 1.2rem;
            outline: none; transition: 0.3s; box-sizing: border-box;
        }
        textarea:focus { border-color: var(--p); box-shadow: 0 0 20px rgba(0,255,136,0.2); }
        .results { margin-top: 30px; display: grid; gap: 12px; width: 100%; }
        .card {
            background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05);
            padding: 20px; border-radius: 12px; display: flex; justify-content: space-between;
            align-items: center; transition: 0.2s; cursor: pointer;
        }
        .card:hover { border-color: var(--s); transform: scale(1.02); background: rgba(255,255,255,0.07); }
        .card span { font-size: 1.4rem; text-align: left; word-break: break-all; flex: 1; padding-right: 10px; }
        .copy-btn { background: var(--p); color: #000; padding: 6px 12px; border-radius: 8px; font-weight: 900; font-size: 0.65rem; text-transform: uppercase; }
        .ad-unit { width: 100%; height: 90px; border: 1px dashed #222; margin: 20px 0; display: flex; align-items: center; justify-content: center; color: #222; font-size: 9px; }
    </style>
</head>
<body>
    <div class="ad-unit">ADSENSE TOP</div>
    <div class="container">
        <h1>FONT FLOW</h1>
        <div class="tagline">EXCLUSIVE STYLE FOR YOU</div>
        <textarea id="input" placeholder="Type here..."></textarea>
        <div class="results" id="output"></div>
    </div>
    <script>
        const FONTS = {
            "Vibe": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
            "Bubbles": "Ⓐ⒒ⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ",
            "Bold": "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳",
            "Italic": "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥ⓔ𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻",
            "Gothic": "𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔚𝔛𝔜ℨ𝔞𝔟𝔠𝔡𝔢𝔣𝔫𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷",
            "Square": "🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅶🅇🅈🅉🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅶🅇🅈🅉"
        };
        const alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
        const input = document.getElementById('input');
        const output = document.getElementById('output');

        input.oninput = () => {
            const val = input.value;
            output.innerHTML = "";
            if(!val) return;
            Object.keys(FONTS).forEach(key => {
                let res = "";
                for(let c of val) {
                    let i = alpha.indexOf(c);
                    res += i !== -1 ? FONTS[key][i] : c;
                }
                const div = document.createElement('div');
                div.className = 'card';
                div.onclick = () => {
                    navigator.clipboard.writeText(res);
                    div.querySelector('.copy-btn').innerText = "DONE";
                    setTimeout(() => div.querySelector('.copy-btn').innerText = "COPY", 800);
                };
                div.innerHTML = `<span>${res}</span><div class="copy-btn">COPY</div>`;
                output.appendChild(div);
            });
        };
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
