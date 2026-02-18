import cv2
import os
import numpy as np

# Path to dataset folder
dataset_path = "dataset"

# Create LBPH recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

faces = []
ids = []

print("Training started...")

for file_name in os.listdir(dataset_path):
    if file_name.endswith(".jpg"):
        path = os.path.join(dataset_path, file_name)

        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

        # Extract ID from file name
        # Format: user.<id>.<count>.jpg
        id = int(file_name.split(".")[1])

        faces.append(img)
        ids.append(id)

ids = np.array(ids)

recognizer.train(faces, ids)

# Save trained model
recognizer.save("trainer.yml")

print("Training completed successfully.")
print("Model saved as trainer.yml")
