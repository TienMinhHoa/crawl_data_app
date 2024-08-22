import pandas as pd
from sklearn.model_selection import train_test_split
import re
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from sklearn.naive_bayes import MultinomialNB   
import os
hot_words = ["tuyển dụng","công chức"]
def emphasize_hot_words(text):
    for word in hot_words:
        text = text.replace(word, word + " " + word)  # Nhân đôi từ hot
    return text
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\d', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    # stop_words = set(stopwords.words('english'))
    text = ' '.join(word for word in text.split())
    return text
def train(save = False,name_model = None,name_vectorize = None):
    data = []
    for path in os.listdir("data_ai_content/pos"):
        with open(f"data_ai_content/pos/{path}","r",encoding='utf8') as file:
            pos_sample = file.read() 
            data.append([pos_sample,1])
    for path in os.listdir("data_ai_content/neg"):
        with open(f"data_ai_content/neg/{path}","r",encoding='utf8') as file:
            neg_sample = file.read() 
            data.append([neg_sample,0])
    content = [preprocess_text(tmp[0]) for tmp in data]
    content = [emphasize_hot_words(tmp) for tmp in content]
    labels = [int(tmp[1]) for tmp in data]
    print(labels)

    X_train, X_test, y_train, y_test = train_test_split(content, labels, test_size=0.3, random_state=42)


    stop_words_vietnamese = [
        'và', 'là', 'của', 'trong', 'với', 'một', 'những', 'đã', 'được', 'có', 'cho', 'về', 
        'này', 'như', 'khi', 'từ', 'để', 'thì', 'bị', 'bởi', 'các', 'tại', 'theo', 'vào', 
        'ra', 'lại', 'nên', 'mà', 'sau', 'trước', 'hơn', 'nữa', 'cùng', 'cũng', 'đến', 'đi'
    ]

    vectorizer = TfidfVectorizer(stop_words=stop_words_vietnamese)
    X_train_counts = vectorizer.fit_transform(X_train)
    X_test_counts = vectorizer.transform(X_test)



    clf = MultinomialNB(class_prior=[0.7, 0.3])
    clf.fit(X_train_counts, y_train)

    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

    y_pred = clf.predict(X_test_counts)
    print(y_pred)
    print(y_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")
    if save:
        save_model(clf,vectorizer,name_model=name_model,name_vectorize=name_vectorize)
    return clf,vectorizer
import joblib
def save_model(model,vectorizer,name_model = "Bayse.pkl",name_vectorize = "vetorize.pkl"):
    joblib.dump(model, name_model)
    joblib.dump(vectorizer, name_vectorize)
    
    
# train(save = True,name_model = "model_AI/filter_content/Bayes.pkl",name_vectorize = "model_AI/filter_content/vectorize.pkl")