# %%
import face_recognition
import pickle
from tqdm import tqdm
import glob
import os.path

# %% convert all known encondings to feature vectors
input_path = 'known_faces'
output_path = 'known_faces.pkl'
face_dict = dict()
print('convert all known encondings to feature vectors')
for filepath in tqdm(list(glob.glob(os.path.join(input_path, '*.png')))):
    name = os.path.basename(os.path.splitext(filepath)[0])
    face_dict[name] = face_recognition.face_encodings(face_recognition.load_image_file(filepath))[0]

with open(output_path, 'wb') as f:
    pickle.dump(face_dict, f)

# %% example
known_image = face_recognition.load_image_file("faces/Omer.png")
unknown_image = face_recognition.load_image_file("faces/2022-09-23T10_43_04_593758.png")

known_encoding = face_recognition.face_encodings(known_image)[0]
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

results = face_recognition.compare_faces([known_encoding], unknown_encoding)

results
# %%
