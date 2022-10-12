import pandas as pd
import os
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, Response, session, flash
from flask_mongoengine import MongoEngine, Document
from flask_wtf import FlaskForm
from PIL import Image, ImageDraw, ImageFont
from wtforms import StringField, PasswordField
from wtforms import form
# from wtforms.fields import DateField
#from wtforms.fields.core import RadioField
import cv2
import json
from tkinter import *
import requests
import pymongo
from wtforms.form import Form
from wtforms.validators import Email, Length, InputRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message

import random

app = Flask(__name__, template_folder='.')
mail = Mail(app)

app.config['MONGODB_SETTINGS'] = {
    'db': 'project',
    'host': 'mongodb+srv://user:hello123@project.kswnu.mongodb.net/project?retryWrites=true&w=majority',
    'port': 27017
}
# mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'agganoor@gmail.com'
app.config['MAIL_PASSWORD'] = '896209Sa!'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.config['SECRET_KEY'] = "HELLO_WORLD"
db = MongoEngine(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Document):
    meta = {'collection': 'student'}
    email = db.StringField()
    password = db.StringField()
    name = db.StringField()
    rollno = db.StringField()

class adminn(UserMixin, db.Document):
    meta = {'collection': 'admin'}
    aemail = db.StringField()
    apassword = db.StringField()
    aname = db.StringField()
    anum = db.StringField()

class teach(UserMixin, db.Document):
    meta = {'collection': 'teacher'}
    temail = db.StringField()
    tpassword = db.StringField()
    tname = db.StringField()
    rollno = db.StringField()


class facial(UserMixin, db.Document):
    meta = {'collection': 'rec1'}
    rollno = db.StringField()
    face_pixels = db.ListField()


@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()


class cwise(FlaskForm):
    cname = StringField('cname',  validators=None)

# class dwise(FlaskForm):
#     dinp = DateField(id='datepick',format='%m-%d-%y')


class RegForm(FlaskForm):
    email = StringField('email',  validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=30)])
    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=20)])
    name = StringField('name', validators=[
        InputRequired(), Length(min=4, max=20)])
    rollno = StringField('name', validators=[
        InputRequired(), Length(min=8, max=20)])

class tform(FlaskForm):
    temail = StringField('email',  validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=30)])
    tpassword = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=20)])
    tname = StringField('name', validators=[
        InputRequired(), Length(min=4, max=20)])
    rollno = StringField('name', validators=[
        InputRequired(), Length(min=8, max=20)])



class UpdateForm(FlaskForm):
    email = StringField('email',  validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=30)])
    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=20)])
    name = StringField('name', validators=[
        InputRequired(), Length(min=4, max=20)])
    rollno = StringField('name', validators=[
        InputRequired(), Length(min=8, max=20)])

class adminform(FlaskForm):
    aemail = StringField('aemail',  validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=30)])
    apassword = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=20)])
    aname = StringField('name', validators=[
        InputRequired(), Length(min=4, max=20)])
    anum = StringField('name', validators=[
        InputRequired(), Length(min=8, max=20)])
    


class resetpasswordForm(FlaskForm):
    email = StringField('email',  validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=30)])

#####################################################

@app.route('/tregister', methods=['GET', 'POST'])
def treg():
    #form = tform()

    if request.method == 'POST':
        print('=============',request.form.get('name'))
        
        existing_user = teach.objects(
            temail=request.form.get("temail")).first()
        if existing_user is None:
            hashpass = generate_password_hash(
                request.form.get("tpassword"), method='sha256')
            hey = teach(tname=request.form.get("tname"),rollno=request.form.get("rollno"),temail=request.form.get("temail"),
                        tpassword=hashpass
                        ).save()
            if (hey != "null"):
                print("delete")
            login_user(hey)
            return (pop2())
        else:
            print(1)
        
    return render_template('teacherreg.html', form=form)

#####################################################

@app.route('/repassword', methods=['GET', 'POST'])
def repassword():
    form = resetpasswordForm()
    if request.method == 'POST':
        if form.validate():
            check_user = User.objects(email=form.email.data).first()
            if check_user:
                msg = Message(
                    'RESET PASSWORD', sender='dragonsairam.sai@gmail.com', recipients=[form.email.data])
                print(form.email.data)
                number = random.randint(1111, 9999)
                msg.body = str(number)
                mail.send(msg)

                return "Sent"
            else:
                print("invalid user")
    return render_template('passwordreset.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    # form = RegForm()
    if request.method == 'POST':
        print('=============',request.form.get('name'))
        existing_user = User.objects(
            email=request.form.get("email")).first()
        if existing_user is None:
            hashpass = generate_password_hash(
                request.form.get("password"), method='sha256')
            hey = User(name=request.form.get("name"),rollno=request.form.get("rollno"),email=request.form.get("email"),
                        password=hashpass
                        ).save()
            if (hey != "null"):
                print("delete")
            login_user(hey)
            return(pop())
        else:
            print(1)
        
    return render_template('adminindex.html', form=form)


@app.route('/update', methods=['GET', 'POST'])
def update():
    form = UpdateForm()
    if request.method == 'POST':
        if form.validate():
            existing_user = User.objects(email=form.email.data).first()
            if existing_user is not None:
                hashpass = generate_password_hash(
                    form.password.data, method='sha256')
                existing_user.update(name=form.name.data, password=hashpass,rollno=form.rollno.data)
                login_user(existing_user)
                return redirect(url_for('dashboard'))
            else:
                print(1)
        else:
            print(2)
    return render_template('updaten.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated == True:
        return redirect(url_for('dashboard'))
    form = RegForm()
    if request.method == 'POST':
        check_user = User.objects(rollno=form.rollno.data).first()
        if check_user:
            if check_password_hash(check_user['password'], form.password.data):
                login_user(check_user)
                return redirect(url_for('dashboard'))

            else:
                return render_template('index.html', form=form,  password=True)
        else:
            return render_template('index.html', form=form, user=True)
    return render_template('index.html', form=form)
def recognize_attendence(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()  
        #recognizer.read("TrainingImageLabel"+os.sep+"Trainner.yml")
        recognizer.read('./classifier.xml')
        harcascadePath = "./Cascades/haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath)
        font = cv2.FONT_HERSHEY_SIMPLEX
        

        # start realtime video capture
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cam.set(3, 640) 
        cam.set(4, 480) 
        minW = 0.1 * cam.get(3)
        minH = 0.1 * cam.get(4)

        while True:
            ret, im = cam.read()
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2, 5,
            minSize = (int(minW), int(minH)),flags = cv2.CASCADE_SCALE_IMAGE)
            for(x, y, w, h) in faces:
                cv2.rectangle(im, (x, y), (x+w, y+h), (10, 159, 255), 2)
                id,predict=recognizer.predict(gray[y:y+h,x:x+w])
                confidence=int((100*(1-predict/300)))

                conn=mysql.connector.connect(host='localhost',username='root',password='abhi2021',database='face_recognition')
                my_cursor=conn.cursor()

                my_cursor.execute("select name from student_detail where student_id="+str(id))
                n=my_cursor.fetchone()
                n="+".join(n)

                # my_cursor.execute("select s from student where Student_id="+str(id))
                # r=my_cursor.fetchone()
                # r="+".join(r)

                my_cursor.execute("select dep from student_detail where student_id="+str(id))
                d=my_cursor.fetchone()
                d="+".join(d)


                my_cursor.execute("select eno from student_detail where student_id="+str(id))
                i=my_cursor.fetchone()
                i="+".join(i)
                        
                if confidence>77:
                    cv2.putText(im,f"ID:{i}",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(im,f"Name:{n}",(x,y-30),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(im,f"Dep:{d}",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    self.mark_attendance(i,n,d)                
                else:
                    cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),3)
                    cv2.putText(im,"Unknown Face",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)


            cv2.imshow("Welcome to Face Recognition",im)
    
            if (cv2.waitKey(1) == ord('q')):
                break
        
        cam.release()
        cv2.destroyAllWindows()


@app.route('/tlogin', methods=['GET', 'POST'])
def tlogi():
    # if current_user.is_authenticated == True:
    #     return redirect(url_for('/logout'))
    form = tform()
    if request.method == 'POST':
        check_user = teach.objects(rollno=form.rollno.data).first()
        if check_user:
            if check_password_hash(check_user['tpassword'], form.tpassword.data):
                login_user(check_user)
                return("Logged in!")
                #return redirect(url_for('dashboard'))

            else:
                return render_template('index.html', form=form,  password=True)
        else:
            return render_template('index.html', form=form, user=True)
    return render_template('index.html', form=form)


def pop():
    import win32api
    win32api.MessageBox(0, 'Lets register your face', 'NOTICE')
    return render_template('frame_register.html')

def pop2():
    import win32api
    win32api.MessageBox(0, 'Lets register your face', 'NOTICE')
    return render_template('tframe.html')

@app.route('/webcam')
@login_required
def webcam():
    return render_template('webindex.html')


@app.route('/receiveframe', methods=['GET', 'POST'])
def receive():
    print("hello")
    if request.method == "GET":
        return "no picture"
    elif request.method == "POST":
        image_data = request.form.get("content").spilt(",")[1]
        print(image_data)
        with open("clientimage.png", "wb") as f:
            print(f.write(base64.b64decode(image_data)))
            f.write(base64.b64decode(image_data))
        print("PICTURE", image_data)
        return "got picture"


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.name)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    print('====================',logout)
    return redirect(url_for('login'))


global camera
camera = cv2.VideoCapture(0)  # use 0 for web camera

# face_cascade = cv2.CascadeClassifier('./FaceDetect.xml')
'''
with open("face_encoding.txt", "rb") as fp:
    # Unpickling
    face_encoding = pickle.load(fp)
'''

global frame, frame1
def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
       
        success, frame = camera.read()  # read the camera frame
        # temp = User.rollno
        # cv2.imwrite('C:\Users\banav\OneDrive\Desktop\SOFTWARE PROJECT\login\local\"%s.csv" % temp' ,frame)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame1 = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame1 + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/cpt', methods=['GET', 'POST'])
def index():
    
    """Video streaming home page."""
    if request.method == 'POST' and 'capture' in request.form:
        frame2 = str(frame)
        print(frame)
        facial1 = facial(rollno=current_user.rollno,
                         face_pixels=frame.tolist()).save()
        # facial1.to_json()
    return render_template('frame_register.html')

@app.route('/cpt1', methods=['GET', 'POST'])
def index1():
    
    """Video streaming home page."""
    if request.method == 'POST' and 'capture' in request.form:
        frame2 = str(frame)
        print(frame)
        facial1 = facial(rollno=request.form.get("rollno"),
                         face_pixels=frame.tolist()).save()
        # facial1.to_json()
    return render_template('frame_register.html')

@app.route('/cpt2', methods=['GET', 'POST'])
def index2(): 
    """Video streaming home page."""
    if request.method == 'POST' and 'capture' in request.form:
        frame2 = str(frame)
        print(frame)
        facial1 = facial(rollno ,
                         face_pixels=frame.tolist()).save()
        # facial1.to_json()
    return render_template('tframe.html')



@app.route('/train', methods=['GET', 'POST'])
@login_required
def send():
    client = pymongo.MongoClient(
        "mongodb+srv://user:hello123@project.kswnu.mongodb.net/project?retryWrites=true&w=majority:27017/")

    # Database Name
    db = client["project"]

    # Collection Name
    col = db["rec1"]

    x = col.find({})
    allface_arr = []
    rollnum_arr = []
    for i in x:
        allface_arr.append(i['face_pixels'])
        rollnum_arr.append(i['rollno'])
    allface_arr

    url = '/uploader'
    myobj = {'allface_arr': allface_arr, "Roll_No": rollnum_arr}
    x = requests.post(url, json=myobj)
    # print(x.text)
    # print the response text (the content of the requested file):

   # print(x.text)

    print(allface_arr)

    #return render_template('adminindex.html', str(x))

    return str(x)


# @app.route("/cwis", methods=['GET', 'POST'])
# def coursewise():
#     form = cwise()
#     cname = request.form.get("cname")
#     client = pymongo.MongoClient(
#         "mongodb+srv://user:hello123@project.kswnu.mongodb.net/project?retryWrites=true&w=majority:27017/")
#     db = client["project"]
#     col = db["time"]
#     x = col.find({})
#     resdict = {}
#     coursename = cname  # take from post
#     for i in x:
#         print(i['course'], coursename)
#         if str(i['course']) == str(coursename):
#             resdict[i['time'].split(', ')[0]] = 'Present'
#             print(3)

#     print(json.dumps(resdict))

#     # return (render_template('tables.html',form=form,resdict=json.dumps(resdict)))
#     return(render_template('tables.html', form=form, resdict=json.dumps(resdict)))
@app.route("/dwise", methods=['GET', 'POST'])
def datewise():
    client = pymongo.MongoClient(
            "mongodb+srv://user:hello123@project.kswnu.mongodb.net/project?retryWrites=true&w=majority:27017/")
    db = client["project"]
    col = db["users"]
    x = col.find({})
    rlist=[]
    for doc in x:
        rlist.append(doc.get('rollno'))
    #print(rlist)

    if request.method == "POST":
        date = request.form.get("date")
        client = pymongo.MongoClient(
            "mongodb+srv://user:hello123@project.kswnu.mongodb.net/project?retryWrites=true&w=majority:27017/")
        db = client["project"]
        col = db["time"]
        x = col.find({})
        for doc in x:
            for i in rlist:
                # print(type(key))
                # print(type(str(doc.get('rollno'))))
                if(str(i)==str(doc.get('rollno'))):
                    value=str(doc.get('time'))
                    temp = value.split(",")
                    if(temp[0]==date):
                        print('roll number: '+str(doc.get('rollno')) +' '+'course: '+str(doc.get('course')) +' '+'Attendance: 1')
                # else:
                #     print('roll number: '+ str(i) +' '+'course: '+str(doc.get('course')) +' '+'Attendance: 0')
            #print(doc)

        return "The date is "+str(date)
    return render_template('datewise.html')

@app.route("/cwise", methods=['GET', 'POST'])
def coursewise():
    if request.method == "POST":
        course = request.form.get("course")
        client = pymongo.MongoClient(
            "mongodb+srv://user:hello123@project.kswnu.mongodb.net/project?retryWrites=true&w=majority:27017/")
        db = client["project"]
        col = db["time"]
        x = col.find({})
        for doc in x:
            for key, value in doc.items():
                if(key =='course'):
                    temp = str(doc.get('time')).split(",")
                    if(str(value) == course):
                        print('roll number: '+str(doc.get('rollno')) +' '+'date: '+str(temp[0]) +' '+'Attendance: 1')
                    # else:
                    #     print('roll number: '+str(doc.get('rollno')) +' '+'date: '+str(temp[0]) +' '+'Attendance: 0')
            #print(doc)


        return('roll number: '+str(doc.get('rollno')) +' '+'date: '+str(temp[0]) +' '+'Attendance: 1')
        #return "The course is "+str(course)
    return render_template('coursewise.html')

@app.route("/rwise", methods=['GET', 'POST'])
def rollwise():
    if request.method == "POST":
        rollno = request.form.get("rollno")
        client = pymongo.MongoClient(
            "mongodb+srv://user:hello123@project.kswnu.mongodb.net/project?retryWrites=true&w=majority:27017/")
        db = client["project"]
        col = db["time"]
        x = col.find({})
        for doc in x:
            temp = str(doc.get('time')).split(",")
            if(str(doc.get('rollno')) == str(rollno)):
                print('course: '+str(doc.get('course')) +' '+'date: '+str(temp[0]) +' '+'Attendance: 1')
            # else:
            #     print('course: '+str(doc.get('course')) +' '+'date: '+str(temp[0]) +' '+'Attendance: 0')
        #print(doc)

        return "The course is "+str(rollno)
    return render_template('rollwise.html')


# @app.route('/dwise', methods=['GET','POST'])
# def datewise():
#     form=dwise()
#     if form.validate_on_submit():
#         return form.dt.data.strftime('%m-%d-%y')

# code for date to be implemented
# <form action="#" method="post">
#     {{ form.dt(class='datepicker') }}
#     {{ form.hidden_tag() }}
#     <input type="submit"/>
# </form>
############ image upload code ##############

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/upload", methods=["POST"])
def upload():
    folder_name = request.form['images']
    '''
    # this is to verify that folder to upload to exists.
    if os.path.isdir(os.path.join(APP_ROOT, 'files/{}'.format(folder_name))):
        print("folder exist")
    '''
    target = os.path.join(APP_ROOT, 'files/{}'.format(folder_name))
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        if (ext == ".jpg") or (ext == ".png"):
            print("File supported moving on...")
        else:
            render_template("Error.html", message="Files uploaded are not supported...")
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)

    # return send_from_directory("images", filename, as_attachment=True)
    return render_template("complete.html", image_name=filename)


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)


@app.route('/gallery')
def get_gallery():
    image_names = os.listdir('./images')
    print(image_names)
    return render_template("gallery.html", image_names=image_names)

############# - ADMIN CODE - ###################
@app.route('/alogout', methods=['GET'])
#@login_required
def alogout():
    logout_user()
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    return render_template('adminlogin.html',form=form)

@app.route('/adminlogin', methods=['GET', 'POST'])
def adlogin():
    if current_user.is_authenticated == True:
        return("hello")
        # return redirect(url_for('dashboard'))
    form = adminform()
    if request.method == 'POST':
        check_user = adminn.objects(aemail=form.aemail.data).first()
        if check_user:
            if check_password_hash(check_user['apassword'], form.apassword.data):
                login_user(check_user)
                return render_template('adminindex.html', aname=current_user.aname)
                # return redirect(url_for('dashboard'))

            else:
                return render_template('adminlogin.html', form=form,  password=True)
        else:
            return render_template('adminlogin.html', form=form, user=True)
    return render_template('adminlogin.html', form=form)


@app.route('/adminregister', methods=['GET', 'POST'])
def aregister():
    form = adminform()
    if request.method == 'POST':
        existing_user = adminn.objects(aemail=form.aemail.data).first()
        if existing_user is None:
            hashpass = generate_password_hash(
                form.apassword.data, method='sha256')
            hey = adminn(aname=form.aname.data, anum=form.anum.data, aemail=form.aemail.data,
                       apassword=hashpass).save()
            login_user(hey)
            return ("registered")
            # return redirect(url_for('dashboard'))
        else:
            print(1)
    return render_template('adminreg.html', form=form)


# @app.route('/admin', methods=['GET', 'POST'])
# def admin():
#     return render_template('adminindex.html', form=form)


@app.route('/adminform', methods=['GET', 'POST'])
def import_content():
    filepath = 'c:/student-gender-grade.csv'
    mng_client = pymongo.MongoClient('localhost', 27017)
    mng_db = mng_client['project']
    collection_name = 'trial7'
    db_cm = mng_db[collection_name]
    cdir = os.path.dirname(__file__)
    file_res = os.path.join(cdir, filepath)

    data = pd.read_csv(file_res)
    data_json = json.loads(data.to_json(orient='records'))
    db_cm.delete_many({})
    db_cm.insert_many(data_json)
    return ('Done')

@app.route('/aalloc', methods=['GET', 'POST'])
def alloc():
    client = pymongo.MongoClient(
            "mongodb+srv://user:hello123@project.kswnu.mongodb.net/project?retryWrites=true&w=majority:27017/")
    db = client["project"]
    col = db["users"]
    x = col.find({})
    rlist=[]
    for doc in x:
        rlist.append(doc.get('name'))
    
    return render_template('alloc.html',rlist=rlist)

@app.route('/cal', methods=['GET', 'POST'])
def calender():
    return render_template('json.html')
@app.route('/data')
def return_data():
    start_date = request.args.get('start', '')
    end_date = request.args.get('end', '')
    with open("events.json", "r") as input_data:
                return input_data.read()




################################################################






##########Trial Code#######################
@app.route("/allocation", methods=['GET', 'POST'])
def alc():
    client = pymongo.MongoClient(
            "mongodb+srv://user:hello123@project.kswnu.mongodb.net/project?retryWrites=true&w=majority:27017/")
    db = client["project"]
    col = db["users"]
    x = col.find({})
    rlist=[]
    for doc in x:
        rlist.append(doc.get('name'))
    print(rlist)

    # return (render_template('tables.html',form=form,resdict=json.dumps(resdict)))
    return(render_template('tables.html', form=form))

app.run(debug=True)


    