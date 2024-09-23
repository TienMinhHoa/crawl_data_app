import re
import joblib
import nltk
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, precision_score, \
    recall_score, f1_score

# nltk.download('stopwords')


def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\d', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    # stop_words = set(stopwords.words('english'))
    text = ' '.join(word for word in text.split())
    return text


def train(save=False):
    with open("content.txt", "r", encoding='utf8') as file:
        data = file.read().strip().split("\n")
    data = data[1:]
    emails = [preprocess_text(tmp.split(",")[0]) for tmp in data]
    labels = [int(tmp.split(",")[1]) for tmp in data]
    print(labels)

    X_train, X_test, y_train, y_test = train_test_split(
        emails, labels, test_size=0.3, random_state=42)

    stop_words_vietnamese = [
        'và', 'là', 'của', 'trong', 'với', 'một', 'những',
        'đã', 'được', 'có', 'cho', 'về', 'này', 'như', 'khi',
        'từ', 'để', 'thì', 'bị', 'bởi', 'các', 'tại', 'theo',
        'vào', 'ra', 'lại', 'nên', 'mà', 'sau', 'trước', 'hơn',
        'nữa', 'cùng', 'cũng', 'đến', 'đi'
    ]

    vectorizer = CountVectorizer(stop_words=stop_words_vietnamese)
    X_train_counts = vectorizer.fit_transform(X_train)
    X_test_counts = vectorizer.transform(X_test)

    clf = MultinomialNB()
    clf.fit(X_train_counts, y_train)

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
        save_model(clf, vectorizer)
    return clf, vectorizer


def save_model(model, vectorizer,
               name_model="Bayse.pkl",
               name_vectorize="vetorize.pkl"):
    joblib.dump(model, name_model)
    joblib.dump(vectorizer, name_vectorize)
