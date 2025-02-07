# face_recognition
使用deepface框架进行1:1人脸比对
运行以下命令启动服务接口
```
python app.py
```
接口返回结果格式如下所示
```
{
    "detector_backend": "opencv",
    "distance": 0.2750691403511798,
    "facial_areas": {
        "img1": {
            "h": 183,
            "left_eye": [
                262,
                159
            ],
            "right_eye": [
                200,
                146
            ],
            "w": 183,
            "x": 142,
            "y": 78
        },
        "img2": {
            "h": 136,
            "left_eye": [
                241,
                110
            ],
            "right_eye": [
                197,
                117
            ],
            "w": 136,
            "x": 169,
            "y": 59
        }
    },
    "model": "VGG-Face",
    "similarity_metric": "cosine",
    "threshold": 0.68,
    "time": 6.72,
    "verified": true
}
```
其中`(x,y)`表示检测得到检测框左上角的坐标，`h`,`w`为检测框的高和宽，`verified`为比对结果，`true`表示比对成功

现已打包为docker镜像face-recognition-app
```
docker run -p 6001:6001 face-recognition-app
```

