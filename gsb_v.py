import os
import random
from pathlib import Path

# 配置
RANDOM_SEED = 42  # ✅ 固定随机种子
NUM_SAMPLES = 50
PROMPT_FILE = "/root/paddlejob/workspace/env_run/test_data/prompt.txt"
PROMPT_ZH_FILE = "/root/paddlejob/workspace/env_run/test_data/prompt_zh.txt"
MODEL_DIRS = ["teacache_300", "origin_300_28", "firstblock_taylorseer0.09_300_28"]
OUTPUT_HTML = "study.html"
MODEL_NAMES = ["modelA", "modelB", "modelC"]  # 用于结果记录
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
        .score-btns button { margin: 2px; padding: 4px 8px; }
        th.prompt-col, td.prompt-col { width: 300px; }
        th.prompt-zh-col, td.prompt-zh-col { width: 300px; }
        th.index-col, td.index-col { width: 40px; }
        .selected { background-color: #007bff; color: white; }
    </style>
</head>
<body>
<h1>Human Study</h1>
<p>Click a score (g,s,b) for each image. After completing, you can export results.</p>
<p><strong>评分指南：</strong> g = good,s = so-so,b = bad,一行中的三组图片可以是同一个值</p>

<table>

<tr>
    <th class="index-col">#</th>
    <th class="prompt-col">Prompt</th>
    <th class="prompt-zh-col">中文Prompt</th>
    <th>Model A</th>
    <th>Model B</th>
    <th>Model C</th>
</tr>
"""

# ==== HTML BODY ====
for display_idx, real_idx in enumerate(selected_indices, start=1):
    prompt = prompts[real_idx]
    prompt_zh = prompts_zh[real_idx]
    html += f"<tr>\n  <td class='index-col'>{display_idx}</td>\n"
    html += f"  <td class='prompt-col'>{prompt}</td>\n"
    html += f"  <td class='prompt-zh-col'>{prompt_zh}</td>\n"


    for model_idx, model_dir in enumerate(MODEL_DIRS):
        model_name = MODEL_NAMES[model_idx]
        img_path = os.path.join(model_dir, f"{real_idx}.png")
        rel_path = os.path.relpath(img_path, os.path.dirname(OUTPUT_HTML))
        unique_id = f"r{display_idx}_m{model_name}"
        html += f"""<td>
            <img src="{rel_path}" alt="{unique_id}">
            <div class="score-btns" id="{unique_id}">
                <button onclick="setScore('{unique_id}', 'g')">g</button>
                <button onclick="setScore('{unique_id}', 's')">s</button>
                <button onclick="setScore('{unique_id}', 'b')">b</button>
            </div>
        </td>\n"""
    html += "</tr>\n"

html += "</table>\n"



# ==== JAVASCRIPT LOGIC ====
html += """
<script>
const scores = {};  // { "r1_mmodelA": 1, ... }
const TOTAL_SAMPLES = 5;
const MODELS = ["modelA", "modelB", "modelC"];

function setScore(id, value) {
    scores[id] = value;
    const btns = document.getElementById(id).getElementsByTagName('button');
    for (let btn of btns) {
        btn.classList.remove('selected');
        if (btn.textContent == value) {
            btn.classList.add('selected');
        }
    }
}

function checkAllScored() {
    for (let i = 1; i <= TOTAL_SAMPLES; i++) {
        for (let model of MODELS) {
            const key = `r${i}_m${model}`;
            if (!(key in scores)) {
                alert(`❌ Missing score: Row ${i}, Model ${model}`);
                return false;
            }
        }
    }
    return true;
}

function downloadResults() {
    const blob = new Blob([JSON.stringify(scores, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'human_study_scores.json';
    link.click();
    URL.revokeObjectURL(url);
}

function handleSubmit() {
    if (!checkAllScored()) {
        return;
    }
    alert("✅ All images scored. Submitting...");
    downloadResults();
}
</script>

<div style="text-align: center; margin-top: 30px;">
  <button onclick="handleSubmit()">✅ Submit</button>
</div>
</body>
</html>
"""

# ==== 写入文件 ====
with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ Interactive study HTML saved to {OUTPUT_HTML}")
