import cv2
import os

name = input("Enter student name: ")
path = f"dataset/{name}"

if not os.path.exists(path):
    os.makedirs(path)

cap = cv2.VideoCapture(0)

count = 0

print("⏳ Starting camera...")
print("👉 Press 's' to capture image")
print("👉 Press 'q' to quit")

while True:

    ret, frame = cap.read()

    if not ret:
        continue

    cv2.imshow("Capture Dataset", frame)

    key = cv2.waitKey(1)

    if key == ord('s'):

        img_path = f"{path}/img{count}.jpg"

        cv2.imwrite(img_path, frame)

        print(f"✅ Saved: {img_path}")

        count += 1

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()