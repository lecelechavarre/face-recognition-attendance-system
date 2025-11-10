import cv2
import os
import numpy as np
from tensorflow.keras.models import load_model
import pickle

class LoginEmbeddingExtractor:
    def __init__(self, model_path):
        self.model_path = model_path
        self.dataset_dir = os.path.join(os.getcwd(), 'dataset_login')
        self.embedding_model = self.load_model()

    def load_model(self):
        model = load_model(self.model_path)
        return model

    def get_login_details(self):
        login_details = [name for name in os.listdir(self.dataset_dir) if os.path.isdir(os.path.join(self.dataset_dir, name))]
        return login_details

    def are_there_new_accounts(self, embeddings_model_file):
        if os.path.exists(embeddings_model_file):
            with open(embeddings_model_file, "rb") as f:
                saved_data = pickle.load(f)
            saved_usernames = saved_data["usernames"]

            current_usernames = self.get_login_details()
            new_usernames = [username for username in current_usernames if username not in saved_usernames]

            return bool(new_usernames)
        else:
            return True  # Treat as new accounts if embeddings file doesn't exist

    def get_login_images(self, login_details):
        login_images = {"usernames": [], "image_paths": []}
        for username in login_details:
            image_dir = os.path.join(self.dataset_dir, username)
            if os.path.exists(image_dir):
                images = os.listdir(image_dir)
                for image in images:
                    image_path = os.path.join(image_dir, image)
                    login_images["usernames"].append(username)
                    login_images["image_paths"].append(image_path)
        return login_images

    def normalize_pixels(self, image_paths):
        face_pixels_list = []
        for image_path in image_paths:
            image = cv2.imread(image_path)
            if image is not None:
                image = cv2.resize(image, (160, 160))
                face_pixels = image.astype('float32')
                mean, std = face_pixels.mean(), face_pixels.std()
                face_pixels = (face_pixels - mean) / std
                face_pixels_list.append(face_pixels)
            else:
                print(f"Warning: Could not read image {image_path}")
        return np.array(face_pixels_list)

    def extract_embeddings(self, face_pixels_list):
        embeddings = []
        for face_pixels in face_pixels_list:
            sample = np.expand_dims(face_pixels, axis=0)
            embedding = self.embedding_model.predict(sample)
            new_embedding = embedding.reshape(-1)
            embeddings.append(new_embedding)
        return embeddings

    def face_embedding_for_login(self):
        embeddings_model_file = os.path.join(os.getcwd(), "models/login_embeddings.pickle")

        if os.path.exists(embeddings_model_file):
            with open(embeddings_model_file, "rb") as f:
                saved_data = pickle.load(f)
            saved_usernames = saved_data["usernames"]

            current_usernames = self.get_login_details()
            new_usernames = [username for username in current_usernames if username not in saved_usernames]

            if new_usernames:
                new_login_images = self.get_login_images(new_usernames)
                new_face_pixels = self.normalize_pixels(new_login_images["image_paths"])
                new_embeddings = self.extract_embeddings(new_face_pixels)

                saved_data["usernames"].extend(new_login_images["usernames"])
                saved_data["embeddings"].extend(new_embeddings)

                with open(embeddings_model_file, "wb") as f:
                    pickle.dump(saved_data, f)

                print("New embeddings extracted and saved successfully.")
            else:
                print("No new accounts found.")
        else:
            print("Embeddings file not found.")
