import os
from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import messagebox
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
import numpy as np

class LoginTraining:
    def __init__(self, embedding_path, recognizer_type):
        self.embedding_path = embedding_path
        self.recognizer_type = recognizer_type

    def load_embeddings_and_labels(self):
        with open(self.embedding_path, "rb") as f:
            data = pickle.load(f)
        label = LabelEncoder()
        usernames = np.array(data["usernames"])
        labels = label.fit_transform(usernames)
        embeddings = np.array(data["embeddings"])
        return [label, labels, embeddings, usernames]

    def create_svm_model(self, labels, embeddings):
        model_svc = LinearSVC()
        recognizer = CalibratedClassifierCV(model_svc)
        recognizer.fit(embeddings, labels)
        return recognizer

    def save_recognizer(self, recognizer):
        filename = f'models/login_{self.recognizer_type}_recognizer.pickle'
        with open(filename, "wb") as f:
            pickle.dump(recognizer, f)