import os
import cv2
from app import app, db
from flask import session, redirect, url_for, render_template, abort, request, flash, Response
from face_recognition import face_encodings
from werkzeug.utils import secure_filename
from face_dec import get_face
import pickle



ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'mp4']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_frames(user_id):
    video = cv2.VideoCapture(0)
    """Video streaming generator function."""
    while True:
        rval, frame = video.read()
        if not rval:
            break
        else:
            frame = frame[:, :, ::-1]
            face_encodings = get_face(frame)
            if face_encodings:
                face = Face(user_id, face_encodings)
                db.session.add(face)
                db.commit()


@app.route('/record-face/<user_id>')
def add_face(user_id):
    return Response(get_frames(user_id),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/signup')
def signup():
    return render_template('signup.html')