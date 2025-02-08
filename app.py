from flask import Flask, request, jsonify
import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from insightface.model_zoo import get_model

app = Flask(__name__)

# 加载 ArcFace 预训练模型
model_path = "/home/zhangting/.insightface/models/buffalo_l/w600k_r50.onnx"  # 确保路径正确
recognizer = get_model(model_path)
recognizer.prepare(ctx_id=0)  # 使用 GPU（ctx_id=-1 代表 CPU）

# 加载人脸检测 & 对齐模型
face_app = FaceAnalysis(name="buffalo_l")
face_app.prepare(ctx_id=0)

@app.route('/verify_faces', methods=['POST'])
def verify_faces():
    # 读取上传的图片
    img1_file = request.files.get('img1')
    img2_file = request.files.get('img2')

    if img1_file is None or img2_file is None:
        return jsonify({"error": "请上传两张图片!"}), 400

    # 将图片读取为 OpenCV 格式
    img1 = cv2.imdecode(np.frombuffer(img1_file.read(), np.uint8), cv2.IMREAD_COLOR)
    img2 = cv2.imdecode(np.frombuffer(img2_file.read(), np.uint8), cv2.IMREAD_COLOR)

    if img1 is None or img2 is None:
        return jsonify({"error": "图片读取失败！"}), 400

    # 人脸检测
    faces1 = face_app.get(img1)
    faces2 = face_app.get(img2)

    # 确保检测到人脸
    if len(faces1) == 0 or len(faces2) == 0:
        return jsonify({"error": "未检测到人脸，请使用清晰的人脸图片！"}), 400

    # 获取人脸特征向量
    emb1 = recognizer.get(img1, faces1[0])  # 提取 face1 特征
    emb2 = recognizer.get(img2, faces2[0])  # 提取 face2 特征

    if emb1 is None or emb2 is None:
        return jsonify({"error": "特征提取失败，请检查图片质量或尝试其他图片！"}), 400

    emb1 = emb1.flatten()
    emb2 = emb2.flatten()

    # 计算余弦相似度
    emb1 = emb1 / np.linalg.norm(emb1)  # 归一化
    emb2 = emb2 / np.linalg.norm(emb2)  # 归一化
    similarity = np.dot(emb1, emb2)  # 计算余弦相似度

    # 阈值设置为0.6
    verified = "true" if similarity > 0.6 else "false"  # 返回字符串 "true" 或 "false"

    result = {
        "similarity": f"{similarity:.3f}",
        "verified": verified  # 返回 "true" 或 "false" 字符串
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=6001)
