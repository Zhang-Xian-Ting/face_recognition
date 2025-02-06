from flask import Flask, request, jsonify
from pprint import pprint
from deepface import DeepFace
from gevent import pywsgi
import os
from werkzeug.utils import secure_filename

# 配置文件
app = Flask(__name__)

# 定义图片上传的路径
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# 创建目录如果不存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 配置上传文件夹
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 判断文件类型是否合法
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/verify_faces', methods=['POST'])
def verify_faces():
    # 确保请求是一个包含两张图片的 POST 请求
    if 'img1' not in request.files or 'img2' not in request.files:
        return jsonify({"error": "No file part"}), 400

    img1 = request.files['img1']
    img2 = request.files['img2']

    # 检查文件名是否合法
    if img1.filename == '' or img2.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # 如果文件合法，保存文件
    if img1 and allowed_file(img1.filename) and img2 and allowed_file(img2.filename):
        img1_filename = secure_filename(img1.filename)
        img2_filename = secure_filename(img2.filename)

        # 保存图片
        img1_path = os.path.join(app.config['UPLOAD_FOLDER'], img1_filename)
        img2_path = os.path.join(app.config['UPLOAD_FOLDER'], img2_filename)
        
        img1.save(img1_path)
        img2.save(img2_path)

        # 使用 DeepFace 进行比对
        try:
            result = DeepFace.verify(img1_path, img2_path)
            # 返回结果
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid file format"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001)
