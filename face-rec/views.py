import os
import cv2
from app import app, db
from models import Face, User
from flask import session, redirect, url_for, render_template, abort, request, flash, Response
from face_recognition import face_encodings
from werkzeug.utils import secure_filename
from face_dec import get_face
from face_match import give_match
import pickle
from io import BytesIO



ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'mp4']
video = cv2.VideoCapture(0)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_frames(user_id):
    """Video streaming generator function."""
    while True:
        rval, frame = video.read()
        if not rval:
            db.session.commit()
            break
        else:
            new_frame = frame[:, :, ::-1]
            face_encodings = get_face(new_frame)
            f = BytesIO()
            pickle.dump(face_encodings, f)
            if face_encodings is not None:
                face = Face(user_id, f.getbuffer())
                db.session.add(face)
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

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/camera')
def camera():
    return render_template('camera.html')


def detect_person():
    while True:
        rval, frame = video.read()
        if not rval:
            break
        else:
            new_frame = frame[:, :, ::-1]
            people = give_match(new_frame)
            print(people)
            # f = BytesIO()
            # pickle.dump(face_encodings, f)
            # if face_encodings is not None:
            #     face = Face(user_id, f.getbuffer())
            #     db.session.add(face)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +  cv2.imencode('.jpg', frame)[1].tostring() + b'\r\n')


@app.route('/detect')
def detect_face():
    return Response(detect_person(), mimetype='multipart/x-mixed-replace; boundary=frame')
