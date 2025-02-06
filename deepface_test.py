from pprint import pprint
# deep 库的所有功能都在 deep.DeepFace 子模块下面
from deepface import DeepFace

# 传入两张图片即可进行对比
result = DeepFace.verify("/home/zhangting/Script/data/face_recognition_1.png", "/home/zhangting/Script/data/face_recognition_2.png")
pprint(result)
