from flask import Flask, render_template_string
import os

app = Flask(__name__)

INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FONT FLOW | Ultimate Style</title>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2712778222245542" crossorigin="anonymous"></script>
    <link href="https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Inter:wght@400;600;900&display=swap" rel="stylesheet">
    <style>
        :root { 
            --p: #00ff88; 
            --s: #bd00ff; 
            --bg: #080808;
        }

        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }

        body {
            background: var(--bg); color: #fff; font-family: 'Inter', sans-serif;
            margin: 0; min-height: 100vh; display: flex; flex-direction: column; align-items: center;
            padding: 40px 20px; overflow-x: hidden;
        }

        /* Анимированный фон с кругами */
        .bg-blobs {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            z-index: -1; overflow: hidden; filter: blur(80px); opacity: 0.4;
        }
        .blob {
            position: absolute; width: 300px; height: 300px; border-radius: 50%;
            animation: move 20s infinite alternate;
        }
        .blob1 { background: var(--p); top: -10%; left: -10%; }
        .blob2 { background: var(--s); bottom: -10%; right: -10%; animation-delay: -5s; }
        @keyframes move { from { transform: translate(0,0); } to { transform: translate(100px, 100px); } }

        .container { width: 100%; max-width: 550px; text-align: center; z-index: 1; }

        h1 {
            font-family: 'Syncopate', sans-serif; font-size: clamp(2rem, 8vw, 2.8rem);
            background: linear-gradient(90deg, var(--p), var(--s));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin-bottom: 8px; filter: drop-shadow(0 0 15px rgba(0,255,136,0.4));
            letter-spacing: -2px;
        }

        .description { 
            color: #aaa; font-weight: 400; font-size: 0.95rem; margin-bottom: 35px;
            opacity: 0.8; letter-spacing: 0.5px;
        }

        textarea {
            width: 100%; padding: 22px; border-radius: 18px; 
            background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1);
            color: #fff; font-size: 1.2rem; outline: none; transition: 0.4s;
            backdrop-filter: blur(10px); box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        textarea:focus { border-color: var(--p); background: rgba(255,255,255,0.06); }

        .results { margin-top: 30px; display: grid; gap: 15px; width: 100%; }

        /* Дизайн карточки */
        .card {
            background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05);
            padding: 18px 22px; border-radius: 16px; display: flex; justify-content: space-between;
            align-items: center; cursor: pointer; transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(5px); position: relative; overflow: hidden;
        }
        .card:hover { 
            transform: scale(1.02); border-color: rgba(0,255,136,0.3);
            background: rgba(255,255,255,0.05);
        }

        .card span { 
            font-size: 1.25rem; text-align: left; flex: 1; 
            padding-right: 15px; color: #fff; overflow-wrap: anywhere; 
        }

        /* Кнопка с анимацией */
        .copy-btn { 
            background: rgba(255,255,255,0.1); color: #fff; padding: 10px 18px; 
            border-radius: 12px; font-weight: 700; font-size: 0.75rem; 
            text-transform: uppercase; transition: 0.3s; border: 1px solid rgba(255,255,255,0.1);
            min-width: 90px; text-align: center;
        }

        .card:hover .copy-btn { background: var(--p); color: #000; border-color: var(--p); }

        .copied .copy-btn { 
            background: var(--s) !important; color: #fff !important; 
            border-color: var(--s) !important; transform: scale(1.1);
            box-shadow: 0 0 20px var(--s);
        }

        .ad-placeholder { width: 100%; height: 60px; border: 1px solid rgba(255,255,255,0.05); margin: 20px 0; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #222; font-size: 10px; }
    </style>
</head>
<body>
    <div class="bg-blobs">
        <div class="blob blob1"></div>
        <div class="blob blob2"></div>
    </div>

    <div class="container">
        <h1>FONT FLOW</h1>
        <div class="description">Твой уникальный стиль для соцсетей и игр</div>
        
        <textarea id="input" placeholder="Введи свой текст здесь..."></textarea>

        <div id="output" class="results"></div>
    </div>

    <script>
        const FONTS = {
            "Italic": "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻",
            "Underline": "A̲B̲C̲D̲E̲F̲G̲H̲I̲J̲K̲L̲M̲N̲O̲P̲Q̲R̲S̲T̲U̲V̲W̲X̲Y̲Z̲a̲b̲c̲d̲e̲f̲g̲h̲i̲j̲k̲l̲m̲n̲o̲p̲q̲r̲s̲t̲u̲v̲w̲x̲y̲z̲",
            "Strike": "A̶B̶C̶D̶E̶F̶G̶H̶I̶J̶K̶L̶M̶N̶O̶P̶Q̶R̶S̶T̶U̶V̶W̶X̶Y̶Z̶a̶b̶c̶d̶e̶f̶g̶h̶i̶j̶k_l̶m̶n̶o̶p̶q̶r̶s̶t̶u̶v̶w̶x̶y̶z̶",
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
                div.innerHTML = `<span>${res}</span><div class="copy-btn">COPY</div>`;
                
                div.onclick = () => {
                    navigator.clipboard.writeText(res);
                    div.classList.add('copied');
                    const btn = div.querySelector('.copy-btn');
                    btn.innerText = "COPIED!";
                    setTimeout(() => {
                        div.classList.remove('copied');
                        btn.innerText = "COPY";
                    }, 1200);
                };
                output.appendChild(div);
            });
        };
    </script>
</body>
</html>
