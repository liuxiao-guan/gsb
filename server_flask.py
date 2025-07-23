# save as: server.py
from flask import Flask, request, jsonify
import os
import datetime
import json
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "/root/paddlejob/workspace/env_run/gxl/output/PaddleMIX/inf_speed_bf16/gsb_results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_json():
    
    data = request.get_json()
    if not data:
        return jsonify({"status": "fail", "msg": "No JSON received"}), 400

    # 提取字段
    scores = data.get("scores")
    user = data.get("user", "anonymous").strip()
    index = str(data.get("index", "unknown"))
    print(f"✅ 收到{user}_{index}上传请求")

    # 清洗用户名，防止路径注入
    safe_user = "".join(c for c in user if c.isalnum() or c in ['_', '-'])[:40]
    if not safe_user:
        return jsonify({"status": "fail", "msg": "Invalid username"}), 400

    # 构建保存路径
    folder = os.path.join(UPLOAD_FOLDER, index)
    os.makedirs(folder, exist_ok=True)

    filename = f"{safe_user}_comparison_results_{index}.json"
    filepath = os.path.join(folder, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2, ensure_ascii=False)

    return jsonify({"status": "success", "filename": filename}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081,debug=True)
