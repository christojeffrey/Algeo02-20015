from flask import Flask,render_template,request,flash,redirect,url_for
import os
from werkzeug.utils import secure_filename
import compressAlgo

app = Flask(__name__)

app.secret_key = "himitsu desu"
app.config["Image_upload"] = os.getcwd() + "\\static\\img\\base\\"
app.config["Image_compressed"] = os.getcwd() + "\\static\\img\\compressed\\"
app.config["ALLOWED_EXTENSIONS"] = ['png', 'jpg', 'jpeg', 'gif']

filename = ""
def isallowed(filename):
    if not "." in filename:
        return False    
    ext = filename.rsplit('.',1)[1] 

    if ext.lower() in app.config["ALLOWED_EXTENSIONS"]:
        return True
    else:
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_image():
    global filename
    if 'Compress' in request.form:
        percentage = request.form.get("compressPercentage") # percentage as string
        percentage = int(percentage)
        print(filename)
        print(percentage)

        compressAlgo.algoKompresi(filename,percentage)
        compressLog = """
        testing </br>
        mutli </br>
        line
        """
        return render_template('index.html', filename = filename ,compress = True, compressLog = compressLog, code=301)
    else:
        if 'image' in request.files:
            image = request.files["image"]
            if image.filename == "":
                return redirect(request.url)
            if not isallowed(image.filename):
                return redirect(request.url)
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["Image_upload"],filename))

            return render_template('index.html', filename = filename)
    return render_template(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/img/base/' + filename), code=301)

@app.route('/compress/<filename>')
def compress_image(filename):
    return redirect(url_for('static', filename='uploads/img/compressed/' + filename),compress = True, compressLog = compressLog, code=301)

if __name__ == "__main__":
    app.run(debug=True)
