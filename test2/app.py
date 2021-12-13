from flask import Flask, url_for, request, redirect, session, send_from_directory, flash, render_template
from markupsafe import escape
import os
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
from datetime import datetime, timedelta
from pypinyin import lazy_pinyin
import json

# 文件目录
UPLOAD_FOLDER = os.path.join('.', 'file_path', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
# 允许上传的文件类型
ALLOWED_EXT = (
    '.txt', '.doc', '.docx', '.pdf', '.md',
    '.jpg', '.png', '.jpeg', '.gif', 
    )

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# 设置session保存时长
app.permanent_session_lifetime = timedelta(days=30)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# 设置文件大小限制（当前64M）
app.config['MAX_CONTENT_LENGTH'] = 64 * 1000 * 1000
# app.add_url_rule(
#     "/downloads/<name>", endpoint="download_file", build_only=True
# )
# 添加CSRF保护
CSRFProtect(app)

user = {
    "username": "root",
    "password": "root"
}
# 读取用户名密码，读不到则默认为root:root
if os.path.exists("user.json"):
    with open("user.json") as f:
        user = json.load(f)

def allowed_file(filename):
    '''
    检查后缀名（基于白名单）
    '''
    return os.path.splitext(filename)[-1].lower() in ALLOWED_EXT and filename.count(".") == 1



@app.before_request
def before_request():
    '''
    请求钩子函数，用于认证
    '''
    if not session.get('auth'):
        # 如果没有认证
        if not request.full_path.split("?")[0] == url_for("auth"):
            # 当前页面不是登录页，则条状到登录页
            flash("请登录")
            return redirect(url_for("auth"))
        
@app.route('/auth', methods=['GET', 'POST'])
def auth():
    '''
    认证
    '''
    if request.method == 'POST':
        if request.form['username'] == user['username'] and request.form['password'] == user['password']:
            session['auth'] = True
            flash("登录成功")
            return redirect(url_for("choice"))
        else:
            flash("登录失败")
            return redirect(request.url)
    elif session.get('auth'):
        return redirect(url_for("choice"))
    return render_template("index.html")

@app.route('/choice')
def choice():
    '''
    功能选择
    '''
    return render_template("choice.html")



@app.route("/uploads", methods=["GET", "POST"])
def uploads():
    '''
    文件上传
    '''
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('文件不存在')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('请选择文件')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(''.join(lazy_pinyin(file.filename))) # 文件重命名
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("上传成功")
            return redirect(request.url)
        else:
            flash("文件上传失败，原因可能是文件后缀名不被允许")
            return redirect(request.url)
    return render_template("uploads.html")


@app.route("/downloads")
def downloads():
    '''
    文件下载列表
    '''
    files = [(file, datetime.fromtimestamp(os.path.getctime(os.path.join(app.config['UPLOAD_FOLDER'], file)))) for file in os.listdir(app.config['UPLOAD_FOLDER'])]
    files.sort(key=lambda x: x[1], reverse=True)
    return render_template("downloads.html", files=files)


@app.route('/downloads/<name>')
def download_file(name):
    '''
    返回目标文件
    '''
    return send_from_directory(app.config["UPLOAD_FOLDER"], escape(name))

    

if __name__ == '__main__':
    app.run(host='10.0.16.6',port=5770)







