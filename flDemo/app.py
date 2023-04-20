from flask import Flask, render_template, request
import requests
import hashlib
import random
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['value']

        return render_template('index.html', data=translate(username))
    else:
        return render_template('cidian.html')

# @app.route('/index')
# def fanhui():
#     return render_template('cidian.html')

def translate(word):
    app_key = '填写你的有道开发者应用ID'  # 填写你的有道开发者应用ID
    secret_key = '填写你的有道开发者应用密钥'  # 填写你的有道开发者应用密钥
    api_url = 'http://openapi.youdao.com/api'

    salt = str(random.randint(1, 65536))
    sign_str = app_key + word + salt + secret_key
    sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()

    payload = {
        'q': word,
        'from': 'auto',
        'to': 'zh-CHS',
        'appKey': app_key,
        'salt': salt,
        'sign': sign
    }

    response = requests.get(api_url, params=payload)
    result = json.loads(response.text)
    if result['errorCode'] == '0':
        translation = result['translation'][0]
        return f'{word}的翻译结果为：{translation}'
    else:
        return '翻译失败！'



if __name__ == '__main__':
    app.run()
