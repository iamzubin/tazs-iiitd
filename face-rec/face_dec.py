from PIL import Image
import face_recognition

# Load the jpg file into a numpy array
def get_face(image):
	image = face_recognition.load_image_file(image)
	face_locations = face_recognition.face_locations(image)
	if face_locations:
		top, right, bottom, left = face_locations[0]
		print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
		face_image = image[top:bottom, left:right]
		print(face_image)
		return face_image
	else:
		return None