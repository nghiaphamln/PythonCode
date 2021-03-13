from pyvi import ViTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

data = []

with open("comments.txt", "r", encoding="utf-8") as file:
    line = file.readline()
    i = -2
    k = 0
    while line:
        k += 1
        if k == i + 4:
            i += 4
            data.append(line)
        line = file.readline()

comment = []

for x in data:
    comment.append(ViTokenizer.tokenize(x))

tfIdfVectorizer = TfidfVectorizer()
tfIdf = tfIdfVectorizer.fit_transform(comment)

df = pd.DataFrame(tfIdf.toarray(), columns=tfIdfVectorizer.get_feature_names())
print(df)
