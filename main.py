from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

# Словари для шрифтов (просто замена символов)
FONTS = {
    "Bubbles": "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ",
    "Bold": "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳",
    "Italic": "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻",
    "Gothic": "𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔚𝔛𝔜ℨ𝔞𝔟𝔠𝔡𝔢𝔣𝔫𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷",
    "Square": "🄰🄱🄲🄳🄴🄵🄿🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅶🅇🅈🅉🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅶🅇🅈🅉",
    "Wide": "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ"
}
NORMAL_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def transform_text(text, font_key):
    if font_key not in FONTS: return text
    res = ""
    for char in text:
        if char in NORMAL_CHARS:
            res += FONTS[font_key][NORMAL_CHARS.index(char)]
        else:
            res += char
    return res

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TEXT VIBE | Fancy Font Generator</title>
    <style>
        body { 
            background: #0a0a0a; color: white; font-family: 'Inter', sans-serif; 
            display: flex; flex-direction: column; align-items: center; padding: 50px 20px;
        }
        .container { max-width: 600px; width: 100%; text-align: center; }
        h1 { color: #00ff88; letter-spacing: 5px; font-size: 3rem; margin-bottom: 10px; }
        p { color: #666; margin-bottom: 40px; }
        
        textarea { 
            width: 100%; padding: 20px; border-radius: 15px; background: #151515; 
            border: 2px solid #333; color: white; font-size: 1.2rem; resize: none; outline: none;
            transition: 0.3s; box-sizing: border-box;
        }
        textarea:focus { border-color: #00ff88; box-shadow: 0 0 20px rgba(0,255,136,0.2); }

        .results { margin-top: 30px; display: grid; gap: 15px; }
        .card { 
            background: #151515; padding: 20px; border-radius: 12px; border: 1px solid #222;
            display: flex; justify-content: space-between; align-items: center; transition: 0.2s;
            cursor: pointer;
        }
        .card:hover { border-color: #00ff88; background: #1a1a1a; transform: scale(1.02); }
        .card span { font-size: 1.3rem; }
        .copy-btn { color: #00ff88; font-size: 0.8rem; text-transform: uppercase; font-weight: bold; }
        
        /* Стили для AdSense */
        .ad-banner { width: 100%; height: 90px; background: #111; margin: 20px 0; border: 1px dashed #333; display: flex; align-items: center; justify-content: center; color: #444; }
    </style>
</head>
<body>
    <div class="container">
        <h1>TEXT VIBE</h1>
        <p>Преврати обычный текст в уникальный для соцсетей</p>
        
        <div class="ad-banner">AD BLOCK (PLACEHOLDER)</div>
        
        <textarea id="input" placeholder="Введи свой ник или текст..." oninput="update()"></textarea>
        
        <div class="results" id="output">
            </div>
    </div>

    <script>
        const fonts = """ + str(list(FONTS.keys())) + """;
        const normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
        const fontMaps = """ + str(FONTS) + """;

        function update() {
            const val = document.getElementById('input').value;
            const output = document.getElementById('output');
            output.innerHTML = "";

            if(!val) return;

            fonts.forEach(f => {
                let transformed = "";
                for(let char of val) {
                    let idx = normal.indexOf(char);
                    transformed += idx !== -1 ? fontMaps[f][idx] : char;
                }
                
                const card = document.createElement('div');
                card.className = 'card';
                card.onclick = () => copyText(transformed, card);
                card.innerHTML = `<span>${transformed}</span><div class="copy-btn">Копировать</div>`;
                output.appendChild(card);
            });
        }

        function copyText(text, card) {
            navigator.clipboard.writeText(text);
            const btn = card.querySelector('.copy-btn');
            btn.innerText = "Скопировано!";
            btn.style.color = "#fff";
            setTimeout(() => { btn.innerText = "Копировать"; btn.style.color = "#00ff88"; }, 1500);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
