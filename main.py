from flask import Flask, render_template_string
import os

app = Flask(__name__)

# Весь интерфейс и логика в одной переменной для стабильности
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FONT FLOW | Pro</title>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2712778222245542" crossorigin="anonymous"></script>
    <link href="https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root { --p: #00ff88; --s: #bd00ff; }
        body {
            background: #000; color: #fff; font-family: 'Inter', sans-serif;
            margin: 0; min-height: 100vh; display: flex; flex-direction: column; align-items: center;
            padding: 20px; box-sizing: border-box;
        }
        .container { width: 100%; max-width: 500px; text-align: center; }
        h1 {
            font-family: 'Syncopate', sans-serif; font-size: 1.8rem;
            background: linear-gradient(90deg, var(--p), var(--s));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin-bottom: 5px; filter: drop-shadow(0 0 10px rgba(0,255,136,0.2));
        }
        .tagline { color: #444; letter-spacing: 2px; font-weight: 900; font-size: 0.6rem; margin-bottom: 20px; text-transform: uppercase; }
        textarea {
            width: 100%; padding: 15px; border-radius: 12px; background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1); color: #fff; font-size: 1.1rem;
            outline: none; box-sizing: border-box; transition: 0.3s;
        }
        textarea:focus { border-color: var(--p); box-shadow: 0 0 15px rgba(0,255,136,0.1); }
        .results { margin-top: 20px; display: grid; gap: 10px; width: 100%; }
        .card {
            background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05);
            padding: 15px; border-radius: 10px; display: flex; justify-content: space-between;
            align-items: center; cursor: pointer; transition: 0.2s;
        }
        .card:hover { border-color: var(--s); background: rgba(255,255,255,0.06); }
        .card span { font-size: 1.1rem; text-align: left; word-break: break-all; flex: 1; padding-right: 10px; color: #eee; }
        .copy-btn { background: var(--p); color: #000; padding: 5px 10px; border-radius: 6px; font-weight: 900; font-size: 0.6rem; text-transform: uppercase; }
        .ad-unit { width: 100%; height: 60px; border: 1px dashed #222; margin: 15px 0; display: flex; align-items: center; justify-content: center; color: #222; font-size: 8px; }
    </style>
</head>
<body>
    <div class="ad-unit">ADSENSE TOP</div>
    <div class="container">
        <h1>FONT FLOW</h1>
        <div class="tagline">The Best Styles For You</div>
        <textarea id="input" placeholder="Type text here..."></textarea>
        <div id="output" class="results"></div>
    </div>
    <script>
        const FONTS = {
            "Bold": "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳",
            "Bubbles": "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ",
            "Wide": "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ",
            "Small Caps": "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ",
            "Upside Down": "ɐqɔpǝɟƃɥᴉɾʞꞁɯuodbɹsʇnʌʍxʎzⱯᗷᑐᗡEᖵᘐHIᘀKꞀWNOᗡᑐᖴS⊥∩ΛM᙭⅄Z"
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
                let textToProcess = (key === "Upside Down") ? val.split("").reverse().join("") : val;
                
                for(let c of textToProcess) {
                    let i = alpha.indexOf(c);
                    res += (i !== -1) ? FONTS[key][i] : c;
                }

                const div = document.createElement('div');
                div.className = 'card';
                div.onclick = () => {
                    navigator.clipboard.writeText(res);
                    const btn = div.querySelector('.copy-btn');
                    btn.innerText = "COPIED";
                    setTimeout(() => btn.innerText = "COPY", 800);
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
