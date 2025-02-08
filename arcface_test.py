import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from insightface.model_zoo import get_model

# 1️⃣ 加载 ArcFace 预训练模型
model_path = "/home/zhangting/.insightface/models/buffalo_l/w600k_r50.onnx"  # 确保路径正确
recognizer = get_model(model_path)
recognizer.prepare(ctx_id=0)  # 使用 GPU（ctx_id=-1 代表 CPU）

# 2️⃣ 加载人脸检测 & 对齐模型
face_app = FaceAnalysis(name="buffalo_l")
face_app.prepare(ctx_id=0)

# 3️⃣ 读取两张人脸图片
img1 = cv2.imread("/home/zhangting/face_recognition/static/uploads/1.jpg")
img2 = cv2.imread("/home/zhangting/face_recognition/static/uploads/4.jpg")

# 确保图片正确加载
if img1 is None or img2 is None:
    raise ValueError("图片读取失败！请检查路径是否正确。")

# 4️⃣ 人脸检测
faces1 = face_app.get(img1)
faces2 = face_app.get(img2)


# 确保检测到人脸
if len(faces1) == 0 or len(faces2) == 0:
    raise ValueError("未检测到人脸，请使用清晰的人脸图片！")

# 获取人脸框坐标
face1 = faces1[0].bbox.astype(int)
face2 = faces2[0].bbox.astype(int)
print(face1)
print(face2)

# 画出人脸框保存到新图片
cv2.rectangle(img1, (face1[0], face1[1]), (face1[2], face1[3]), (0, 255, 0), 2)
cv2.rectangle(img2, (face2[0], face2[1]), (face2[2], face2[3]), (0, 255, 0), 2)
cv2.imwrite("/home/zhangting/face_recognition/static/uploads/2.jpg", img1)
cv2.imwrite("/home/zhangting/face_recognition/static/uploads/3.jpg", img2)



# 5️⃣ 获取人脸特征向量
emb1 = recognizer.get(img1, faces1[0])  # 提取 face1 特征
emb2 = recognizer.get(img2, faces2[0])  # 提取 face2 特征

# 确保特征提取成功
if emb1 is None or emb2 is None:
    raise ValueError("特征提取失败，请检查图片质量或尝试其他图片。")

emb1 = emb1.flatten()
emb2 = emb2.flatten()

# 6️⃣ 计算余弦相似度
emb1 = emb1 / np.linalg.norm(emb1)  # 归一化
emb2 = emb2 / np.linalg.norm(emb2)  # 归一化
similarity = np.dot(emb1, emb2)  # 计算余弦相似度

# 7️⃣ 输出相似度
print(f"人脸相似度: {similarity:.3f}")

# 阈值设置为0.6
if similarity > 0.6:
    print("这两张图片是同一个人！")

