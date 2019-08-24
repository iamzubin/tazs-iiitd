import os
import cv2
from app import app, db
from models import Face, User
from forms import LoginForm
from flask import session, redirect, url_for, render_template, abort, request, flash, Response, send_from_directory
from face_recognition import face_encodings
from werkzeug.utils import secure_filename
from face_dec import get_face
from face_match import give_match
import pickle

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'mp4']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_frames(user_id):
    """Video streaming generator function."""
    video = cv2.VideoCapture(0)
    while True:
        rval, frame = video.read()
        if not rval:
            break
        else:
            new_frame = frame[:, :, ::-1]
            face_encodings = get_face(new_frame)
            f = pickle.dumps(face_encodings)
            if face_encodings is not None:
                face = Face(user_id, f)
                db.session.add(face)
                db.session.commit()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +  cv2.imencode('.jpg', frame)[1].tostring() + b'\r\n')

@app.route('/')
def index():
    user = User('nigga', 'Test Nigga')
    db.session.add(user)
    db.session.commit()
    return 'okay'


@app.route('/record-face/<user_id>')
def add_face(user_id):
    return Response(get_frames(user_id), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/camera')
def camera():
    return render_template('camera.html')


def detect_person():
    video = cv2.VideoCapture(0)
    while True:
        rval, frame = video.read()
        if not rval:
            break
        else:
            new_frame = frame[:, :, ::-1]
            face_locations, people = give_match(new_frame)
            if people:
                person = User.get_by_id(people[0])
                top, right, bottom, left = face_locations[0]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, 'Hi!' + person.username, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +  cv2.imencode('.jpg', frame)[1].tostring() + b'\r\n')


@app.route('/detect')
def detect_face():
    return Response(detect_person(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = LoginForm()
    if form.validate_on_submit():
        username, password = form.username.data, form.password.data
        print(username, password)
        user = User.get_by_username(username)
        if user and user.password == password:
            return redirect(url_for('dashboard'))
        else:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            return render_template('signup.html', user_id=new_user.id)
    return render_template('login.html', form=form)


@app.route('/dashboard')
def dashboard():
    return render_template("admin.html")


@app.route('/assets/<path:path>')
def send_file(path):
    return send_from_directory('assets', path)