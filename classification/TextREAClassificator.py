import pickle

class Classifier:
    def __init__(self):
        with open('classification/text_classifier', 'rb') as training_model:
            self.trained_model = pickle.load(training_model)
        with open('classification/vectorizer', 'rb') as vct:
            self.vectorizer1 = pickle.load(vct)

    def text(self,X_test):
        y_pred = self.trained_model.predict(self.vectorizer1.transform([X_test]))
        return y_pred
