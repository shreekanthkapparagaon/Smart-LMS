import joblib
import os
current_file_path = os.path.dirname(os.path.abspath(__file__))



model = joblib.load(os.path.join(current_file_path,"subject_predictor_model.pkl"))
vectorizer = joblib.load(os.path.join(current_file_path,"tfidf_vectorizer.pkl"))
mlb = joblib.load(os.path.join(current_file_path,"subject_binarizer.pkl"))

def predict_subject(title, auther, department):
    text = f"{title} {auther} {department}"
    vec = vectorizer.transform([text])
    pred = model.predict(vec)
    return mlb.inverse_transform(pred)[0]

pre = predict_subject("A course in electrical circuits analysis","Soni, M L and Gupta J C","UG EEE")
print(pre)