# face_recognition
使用arcface框架进行1:1人脸比对
运行以下命令启动服务接口
```
python app.py
```
接口返回结果格式如下所示
```
{
    "similarity": "0.082",
    "verified": "false"
}
```
其中`similarity`表示人脸相似度，`verified`为比对结果，`true`表示比对成功

现已打包为docker镜像face-recognition-app
```
docker run -p 6001:6001 face-recognition-app
```

