from fileinput import filename
import flask 
from flask import Flask,render_template,request,send_from_directory,session
from werkzeug.utils import secure_filename
import os 
import imageio
import json
from PyPDF2 import PdfReader

app = Flask(__name__,template_folder='templates')
UPLOAD_FOLDER="C:\\Test\\flaskfileupload\\upload"
print("folder path"+"\r"+UPLOAD_FOLDER)


app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH']=1024*1024*1024
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

@app.route('/',methods = ['GET', 'POST'])
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html',files=files)


@app.route('/uploader', methods = ['GET', 'POST'])
def uploader_file():
   if request.method == 'POST':
      f = request.files['file']
      filenames=[]
      filename = secure_filename(f.filename)
      f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
      filenames.append(filename)
      return 'file uploaded successfully'+str(request.files['file'])

         

@app.route('/uploaded')
def uploaded():
    return render_template('foo.html', content=os.listdir(app.config['UPLOAD_FOLDER']))

@app.errorhandler(413)
def too_large(e):
  return "File is too large",413

@app.route('/uploads/<filename>')
def view(filename):   
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/read/<page>')
def read(page):
   content=os.listdir(app.config['UPLOAD_FOLDER'])
   for i in content:
        f=PdfReader(app.config['UPLOAD_FOLDER']+'\\'+i,'rb')
        print(f.numPages)
        k=f.numPages
        pages=[]
        for i in range(k):
         pages.append(f.getPage(i).extractText())
        return str(pages[int(page)])



if __name__ == '__main__':
   app.run(debug = True)