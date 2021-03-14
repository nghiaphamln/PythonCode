import joblib
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


string = input("Nhập bình luận: ")

model_score = joblib.load("model.pkl", mmap_mode="r")
count_vect = CountVectorizer()
tfidf_tranformer = TfidfTransformer()
count_vect.fit_transform([string])
result = model_score.predict([string])
result_list = ["Tiêu cực", "Trung lập", "Tích cực"]

print(result_list[result[0] + 1])
