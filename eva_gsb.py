import os
import json
import re
from collections import defaultdict, Counter
import matplotlib.pyplot as plt

# 收集所有符合命名规则的 JSON 文件
files = [f for f in os.listdir('.') if f.startswith("comparison_results_") and f.endswith(".json")]

# 按 group_id 分组统计
grouped_counts = defaultdict(Counter)

for file in files:
    match = re.search(r"comparison_results_(\d+)_.*\.json", file)
    if not match:
        continue
    group_id = int(match.group(1))
    with open(file, 'r') as f:
        data = json.load(f)
        for v in data.values():
            if v in ['g', 's', 'b']:
                grouped_counts[group_id][v] += 1

# 排序分组编号
group_ids = sorted(grouped_counts.keys())

# 设置柱状图参数
labels = ['g', 's', 'b']
width = 0.25
x = range(len(group_ids))

# 获取每组的统计数据
g_counts = [grouped_counts[i]['g'] for i in group_ids]
s_counts = [grouped_counts[i]['s'] for i in group_ids]
b_counts = [grouped_counts[i]['b'] for i in group_ids]

# 画图
fig, ax = plt.subplots(figsize=(10, 6))

bars_g = ax.bar([i - width for i in x], g_counts, width=width, label='g', color='green')
bars_s = ax.bar(x, s_counts, width=width, label='s', color='blue')
bars_b = ax.bar([i + width for i in x], b_counts, width=width, label='b', color='orange')

# 给每个柱子添加数值标签
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.5,
            str(height),
            ha='center',
            va='bottom',
            fontsize=10
        )

add_labels(bars_g)
add_labels(bars_s)
add_labels(bars_b)

# 设置图例和坐标
ax.set_xticks(x)
#ax.set_xticklabels([f'Group {i}' for i in group_ids])
ax.set_xticklabels(['firstblock0.14 4s','firstblock0.07 6s', 'teacache 7s'])
ax.set_ylabel("Count")
ax.set_title("Counts of 'g', 's', 'b' per Group")
ax.legend()
plt.tight_layout()
plt.show()
plt.savefig('counts_per_group.png')
