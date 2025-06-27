import os
import json
from collections import Counter
import matplotlib.pyplot as plt

# 修改为你自己的根目录路径
root_dir = "/root/paddlejob/workspace/env_run/output/gxl/comparion_json"

# 图像保存目录
output_dir = os.path.join(root_dir, "bar_charts")
os.makedirs(output_dir, exist_ok=True)

# 存储每个子文件夹的统计结果
folder_stats = {}

# 遍历子文件夹
for subfolder in sorted(os.listdir(root_dir)):
    subfolder_path = os.path.join(root_dir, subfolder)
    if not os.path.isdir(subfolder_path) or subfolder == "bar_charts":
        continue

    total_counter = Counter()

    # 遍历每个子文件夹中的 JSON 文件
    for file_name in os.listdir(subfolder_path):
        if file_name.endswith(".json"):
            file_path = os.path.join(subfolder_path, file_name)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    total_counter.update(data.values())
            except Exception as e:
                print(f"❌ Error reading {file_path}: {e}")

    # 计算百分比
    total = sum(total_counter.values())
    percent = {k: round(total_counter.get(k, 0) / total * 100, 2) if total > 0 else 0.0 for k in ['g', 's', 'b']}

    
    # 保存统计信息
    folder_stats[subfolder] = {'count': total_counter, 'percent': percent}

    # 绘制条形图
    labels = ['g', 's', 'b']
    values = [total_counter.get(l, 0) for l in labels]
    percentages = [percent.get(l, 0.0) for l in labels]

    fig, ax = plt.subplots()
    bars = ax.bar(labels, values, color=['green', 'orange', 'red'])
    ax.set_title(f"{subfolder} - g/s/b Count")
    ax.set_ylabel("Count")

    # 添加百分比标注
    # for bar, p in zip(bars, percentages):
    #     height = bar.get_height()
    #     ax.text(bar.get_x() + bar.get_width()/2, height + 0.5, f"{p}%", ha='center', va='bottom', fontsize=10)
    # 添加数值标准
    for bar, p in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 0.5, f"{p}", ha='center', va='bottom', fontsize=10)

    # 保存图表
    plt.tight_layout()
    fig_path = os.path.join(output_dir, f"{subfolder}_bar_chart.png")
    plt.savefig(fig_path)
    plt.close()
    print(f"📁 Folder {subfolder}: g={total_counter['g']}, s={total_counter['s']}, b={total_counter['b']}")
    print(f"📁 Folder {subfolder}: g={percent['g']}, s={percent['s']}, b={percent['b']}")


print("✅ 所有子文件夹处理完成，图表已保存至：", output_dir)
