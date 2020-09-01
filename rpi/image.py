# Ensure pip virtual environment is installed by running: pip install pipenv
# Activate virtual environemnt by running: pipenv shell
# Install face recognition library by running:      

import face_recognition

image = face_recognition.load_image_file('./rpi/unknown/download.jpg')
face_location = face_recognition.face_locations(image)

print(face_location)