from flask import Flask, render_template_string
import os

app = Flask(__name__)

INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FONT FLOW | Ultimate</title>
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
            margin-bottom: 5px; filter: drop-shadow(0 0 10px rgba(0,255,136,0.3));
        }
        .tagline { color: #444; letter-spacing: 2px; font-weight: 900; font-size: 0.6rem; margin-bottom: 20px; text-transform: uppercase; }
        textarea {
            width: 100%; padding: 15px; border-radius: 12px; background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1); color: #fff; font-size: 1.1rem;
            outline: none; box-sizing: border-box; transition: 0.3s;
        }
        .results { margin-top: 20px; display: grid; gap: 12px; width: 100%; }
        
        .card {
            background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05);
            padding: 15px; border-radius: 10px; display: flex; justify-content: space-between;
            align-items: center; cursor: pointer; transition: 0.3s;
            /* ФИКС БАГА С ДЛИННЫМ ТЕКСТОМ */
            overflow: hidden; 
        }
        .card:hover { border-color: var(--p); background: rgba(255,255,255,0.07); }
        
        .card span { 
            font-size: 1.1rem; text-align: left; 
            flex: 1; padding-right: 10px; color: #eee;
            /* ФИКС ПЕРЕНОСА СТРОК */
            overflow-wrap: anywhere; 
            white-space: pre-wrap;
        }
        
        .copy-btn { 
            background: var(--p); color: #000; padding: 7px 14px; border-radius: 8px; 
            font-weight: 900; font-size: 0.6rem; text-transform: uppercase;
            flex-shrink: 0; /* Чтобы кнопка не сжималась */
        }
        .copied-state { background: var(--s) !important; color: #fff !important; }
    </style>
</head>
<body>
    <div class="container">
        <h1>FONT FLOW</h1>
        <div class="tagline">Fixed & Styled</div>
        <textarea id="input" placeholder="Введите текст..."></textarea>
        <div id="output" class="results"></div>
    </div>
    <script>
        const FONTS = {
            "Italic": "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻",
            "Underline": "A̲B̲C̲D̲E̲F̲G̲H̲I̲J̲K̲L̲M̲N̲O̲P̲Q̲R̲S̲T̲U̲V̲W̲X̲Y̲Z̲a̲b̲c̲d̲e̲f̲g̲h̲i̲j̲k̲l̲m̲n̲o̲p̲q̲r̲s̲t̲u̲v̲w̲x̲y̲z̲",
            "Strike": "A̶B̶C̶D̶E̶F̶G̶H̶I̶J̶K̶L̶M̶N̶O̶P̶Q̶R̶S̶T̶U̶V̶W̶X̶Y̶Z̶a̶b̶c̶d̶e̶f̶g̶h̶i̶j̶k̶l̶m̶n̶o̶p̶q̶r̶s̶t̶u̶v̶w̶x̶y̶z̶",
            "Bubbles": "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ",
            "Wide": "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ",
            "Small Caps": "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ",
            "Upside": "ɐqɔpǝɟƃɥᴉɾʞꞁɯuodbɹsʇnʌʍxʎzⱯᗷᑐᗡEᖵᘐHIᘀKꞀWNOᗡᑐᖴS⊥∩ΛM᙭⅄Z"
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
                let textToProcess = (key === "Upside") ? val.split("").reverse().join("") : val;
                
                for(let c of textToProcess) {
                    let i = alpha.indexOf(c);
                    res += (i !== -1) ? FONTS[key][i] : c;
                }

                const div = document.createElement('div');
                div.className = 'card';
                div.onclick = () => {
                    navigator.clipboard.writeText(res);
                    const btn = div.querySelector('.copy-btn');
                    btn.innerText = "DONE!";
                    btn.classList.add('copied-state');
                    setTimeout(() => {
                        btn.innerText = "COPY";
                        btn.classList.remove('copied-state');
                    }, 1000);
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
