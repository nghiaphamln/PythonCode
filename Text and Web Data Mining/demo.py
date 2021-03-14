import joblib
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from underthesea import word_tokenize


def get_stopword():
    stop_word = []
    # lấy tất cả stop word trong file
    with open("stopword.txt", encoding="utf-8") as file:
        text = file.read()

        for word in text.split():
            stop_word.append(word)

        file.close()

    # trả về stop word lấy từ file và những kí tự đặc biệt từ string.punctuation
    return stop_word


def remove_stopword(text, stop_word):
    text = word_tokenize(text)  # ghép những từ có nghĩa lại với nhau
    result = ""
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

    for word in text:
        if word not in stop_word:
            new_word = ""
            for char in word:
                if char not in punctuations:
                    new_word += char
            result += new_word + " "

    return result


string = input("Nhập bình luận: ")

# string = remove_stopword(string, get_stopword())

model_score = joblib.load("model.pkl", mmap_mode="r")
count_vect = CountVectorizer()
tfidf_tranformer = TfidfTransformer()
count_vect.fit_transform([string])
result = model_score.predict([string])
result_list = ["Tiêu cực", "Trung lập", "Tích cực"]

print(result_list[result[0] + 1])
