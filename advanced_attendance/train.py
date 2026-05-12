import face_recognition
import os
import pickle
import cv2
import numpy as np

known_encodings = []
known_names = []

DATASET_DIR = "dataset"

print("🔄 Training started...")

for person_name in os.listdir(DATASET_DIR):

    person_path = os.path.join(DATASET_DIR, person_name)

    if not os.path.isdir(person_path):
        continue

    for image_name in os.listdir(person_path):

        image_path = os.path.join(person_path, image_name)

        try:

            img = cv2.imread(image_path)

            if img is None:
                print("❌ Cannot read:", image_path)
                continue

            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            rgb = np.array(rgb, dtype=np.uint8)

            locations = face_recognition.face_locations(rgb)

            encodings = face_recognition.face_encodings(
                rgb,
                locations
            )

            if len(encodings) > 0:

                known_encodings.append(encodings[0])
                known_names.append(person_name)

                print("✅ Trained:", image_path)

            else:
                print("❌ No face:", image_path)

        except Exception as e:
            print("ERROR:", e)

with open("encodings.pkl", "wb") as f:

    pickle.dump({
        "encodings": known_encodings,
        "names": known_names
    }, f)

print("✅ Training complete!")
