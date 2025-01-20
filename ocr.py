from flask import Flask, request, jsonify
from cnocr import CnOcr
import io
from PIL import Image

# 初始化 Flask 应用
app = Flask(__name__)
ocr = CnOcr(rec_model_name='doc-densenet_lite_136-gru')
@app.route('/api/ocr', methods=['POST'])
def ocr_service():
    try:
        # 检查请求中是否有文件
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        # 获取上传的文件
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400

        # 读取文件内容并执行 OCR
        image_bytes = file.read()
        result = perform_ocr(image_bytes)
        return result, 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def perform_ocr(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
      # 所有参数都使用默认值 \n
    out = ocr.ocr(image)
    result = ''
    for i in out:
        if 'text' in i:
            result = result + i['text'] + '\n'
    if not result:
        result = result[:-2]
    print(result)
    return result

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    # 启动 Flask 应用，默认运行在 http://127.0.0.1:5000
    app.run(host='0.0.0.0', port=5000)
# # 如果 pytesseract 没有在环境变量中，可以手动设置路径
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
# # S1 : 读取图片
# image_path = r'D:\img\test.png'
# if not os.path.isfile(image_path):
#     print("错误：图像文件未找到！")
#     exit()
#
# # S2 : 识别图片
# image = cv2.imread(image_path)
# # 灰度化图片
# gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# # 应用二值化处理
# _,binary_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY)
# # 使用 pytesseract 识别处理后的图像
# text_processed = pytesseract.image_to_string(image, lang='chi_sim')
# print('处理后的识别文本：', text_processed)


