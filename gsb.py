import os
import random
from pathlib import Path

# 配置
RANDOM_SEED = 42  # ✅ 固定随机种子
NUM_SAMPLES = 50
PROMPT_FILE = "/root/paddlejob/workspace/env_run/gxl/paddle_speed/ppdiffusers/examples/taylorseer_flux/prompts/prompt.txt"
PROMPT_ZH_FILE = "/root/paddlejob/workspace/env_run/gxl/paddle_speed/ppdiffusers/examples/taylorseer_flux/prompts/prompt_zh.txt"
MODEL_DIRS = ["firstblock_taylorseer0.14_300", "origin_300", "firstblock_taylorseer0.09_300_28"]
OUTPUT_HTML = "study_0.html"
MODEL_NAMES = ["modelA", "modelB"]  # 用于结果记录
# 加载 prompts
with open(PROMPT_FILE, "r", encoding="utf-8") as f:
    prompts = [line.strip() for line in f if line.strip()]
# 加载 prompts
with open(PROMPT_ZH_FILE, "r", encoding="utf-8") as f:
    prompts_zh = [line.strip() for line in f if line.strip()]

# ==== 固定随机种子并抽样 index ====
random.seed(RANDOM_SEED)
max_index = min(len(prompts), len(os.listdir(MODEL_DIRS[0])))
selected_indices = sorted(random.sample(range(max_index), NUM_SAMPLES))

# ==== HTML HEADER ====
html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Human Study</title>
    <style>
        table { border-collapse: collapse; width: 100%; table-layout: fixed; }
        td, th { border: 1px solid #ccc; padding: 10px; text-align: center; word-wrap: break-word; }
        img { max-width: 256px; max-height: 256px; display: block; margin: auto; }
        .score-btns button { margin: 4px; padding: 4px 8px;font-size: 20px; }
        button {
        font-size: 20px;
        padding: 10px 20px;
        margin: 5px;
        cursor: pointer;
    }
        th.prompt-col, td.prompt-col { width: 300px; }
        th.prompt-zh-col, td.prompt-zh-col { width: 300px; }
        th.index-col, td.index-col { width: 40px; }
        .selected { background-color: #007bff; color: white; }
    </style>
</head>
<body>
<h1>Human Study</h1>
<p>请比较者两个模型生成图片的质量 good(g): 代表第一个模型要比第二个模型好,so-so(s): 代表两个模型的效果相似, bad(b): 代表第一个模型要比第二个模型差 。</p>
<p>Click a score (g,s,b) for two images. After completing, you can export results.</p>
<p><strong>评分指南：</strong> g = good,s = so-so,b = bad</p>

<table>


<tr>
    <th class="index-col">#</th>
    <th class="prompt-col">Prompt</th>
    <th class="prompt-zh-col">中文Prompt</th>
    <th>Model A</th>
    <th>Model B</th>
    <th>Score</th>
</tr>
"""

# ==== HTML BODY ====
for idx, i in enumerate(selected_indices):
    en_prompt = prompts[i]
    zh_prompt = prompts_zh[i]
    html += f"<tr><td>{idx+1}</td><td>{en_prompt}</td><td>{zh_prompt}</td>"

    # 两张图
    imgA = f"{MODEL_DIRS[0]}/{i}.png"
    imgB = f"{MODEL_DIRS[1]}/{i}.png"
    score_id = f"r{idx}"

    html += f"""
        <td><img src="{imgA}" width="1024"></td>
        <td><img src="{imgB}" width="1024"></td>
        <td>
            <div id="{score_id}">
                <button onclick="setScore('{score_id}', 'g')">g</button>
                <button onclick="setScore('{score_id}', 's')">s</button>
                <button onclick="setScore('{score_id}', 'b')">b</button>
            </div>
        </td>
    </tr>
    """

html += "</table>"



# 按钮 + JS
html += """
<div style="text-align: center; margin-top: 30px;">
  <button onclick="handleSubmit()">✅ Submit</button>
</div>

<script>
const TOTAL_SAMPLES = """ + str(NUM_SAMPLES) + """;
const scores = {};

function setScore(id, value) {
    scores[id] = value;
    const btns = document.getElementById(id).getElementsByTagName('button');
    for (let btn of btns) {
        btn.classList.remove('selected');
        if (btn.textContent === value) {
            btn.classList.add('selected');
        }
    }
}

function handleSubmit() {
    for (let i = 0; i < TOTAL_SAMPLES; i++) {
        const key = `r${i}`;
        if (!(key in scores)) {
            alert("Please score all rows before submitting. Missing score: Row " + (i + 1));
            return;
        }
    }
    downloadResults();
}

function downloadResults() {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(scores, null, 2));
    const dlAnchor = document.createElement('a');
    dlAnchor.setAttribute("href", dataStr);
    dlAnchor.setAttribute("download", "comparison_results_0.json");
    document.body.appendChild(dlAnchor);
    dlAnchor.click();
    dlAnchor.remove();
}
</script>
</body>
</html>
"""

# ==== 写入文件 ====
with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ Interactive study HTML saved to {OUTPUT_HTML}")
