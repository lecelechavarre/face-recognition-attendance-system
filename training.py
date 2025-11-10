from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC
import pickle
import numpy as np
from sklearn.calibration import CalibratedClassifierCV
from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import messagebox

class Training:
    def __init__(self, embedding_path):
        self.embedding_path = embedding_path

    def load_embeddings_and_labels(self):
        with open(self.embedding_path, "rb") as f:
            data = pickle.load(f)
        label = LabelEncoder()
        ids = np.array(data["face_ids"])
        labels = label.fit_transform(ids)
        embeddings = np.array(data["embeddings"])
        return [label, labels, embeddings, ids]

    def create_svm_model(self, labels, embeddings):
        model_svc = LinearSVC()
        recognizer = CalibratedClassifierCV(model_svc)
        recognizer.fit(embeddings, labels)
        return recognizer