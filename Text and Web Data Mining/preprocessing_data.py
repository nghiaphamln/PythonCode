from __future__ import print_function

import re
import pandas as pd
from underthesea import word_tokenize
import joblib
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.base import TransformerMixin

# từ điển tích cực, tiêu cực, phủ định
path_nag = "sentiment_dicts/nag.txt"
path_pos = "sentiment_dicts/pos.txt"
path_not = "sentiment_dicts/not.txt"
path_neu = "sentiment_dicts/neu.txt"

with open(path_nag, "r", encoding="utf-8") as file:
    nag_list = [n.replace("\n", "") for n in file.readlines()]

with open(path_pos, "r", encoding="utf-8") as file:
    pos_list = [n.replace("\n", "") for n in file.readlines()]

with open(path_not, "r", encoding="utf-8") as file:
    not_list = [n.replace("\n", "") for n in file.readlines()]

with open(path_neu, "r", encoding="utf-8") as file:
    neu_list = [n.replace("\n", "") for n in file.readlines()]


def check_string(text):
    for x in text.split():
        if len(x) >= 8:
            return False
    return True


def check_number(text):
    try:
        int(text)
        return True
    finally:
        return False


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
        if word not in stop_word and not check_number(word):
            new_word = ""
            for char in word:
                if char not in punctuations:
                    new_word += char
            result += new_word + " "

    return result


replace_list = {
    'òa': 'oà', 'óa': 'oá', 'ỏa': 'oả', 'õa': 'oã', 'ọa': 'oạ', 'òe': 'oè', 'óe': 'oé', 'ỏe': 'oẻ',
    'õe': 'oẽ', 'ọe': 'oẹ', 'ùy': 'uỳ', 'úy': 'uý', 'ủy': 'uỷ', 'ũy': 'uỹ', 'ụy': 'uỵ', 'uả': 'ủa',
    'ả': 'ả', 'ố': 'ố', 'u´': 'ố', 'ỗ': 'ỗ', 'ồ': 'ồ', 'ổ': 'ổ', 'ấ': 'ấ', 'ẫ': 'ẫ', 'ẩ': 'ẩ',
    'ầ': 'ầ', 'ỏ': 'ỏ', 'ề': 'ề', 'ễ': 'ễ', 'ắ': 'ắ', 'ủ': 'ủ', 'ế': 'ế', 'ở': 'ở', 'ỉ': 'ỉ',
    'ẻ': 'ẻ', 'àk': u' à ', 'aˋ': 'à', 'iˋ': 'ì', 'ă´': 'ắ', 'ử': 'ử', 'e˜': 'ẽ', 'y˜': 'ỹ', 'a´': 'á',
    # Quy các icon về 2 loại emoj: Tích cực hoặc tiêu cực
    "👹": "negative", "👻": "positive", "💃": "positive", '🤙': ' positive ', '👍': ' positive ',
    "💄": "positive", "💎": "positive", "💩": "positive", "😕": "negative", "😱": "negative", "😸": "positive",
    "😾": "negative", "🚫": "negative", "🤬": "negative", "🧚": "positive", "🧡": "positive", '🐶': ' positive ',
    '👎': ' negative ', '😣': ' negative ', '✨': ' positive ', '❣': ' positive ', '☀': ' positive ',
    '♥': ' positive ', '🤩': ' positive ', 'like': ' positive ', '💌': ' positive ',
    '🤣': ' positive ', '🖤': ' positive ', '🤤': ' positive ', ':(': ' negative ', '😢': ' negative ',
    '❤': ' positive ', '😍': ' positive ', '😘': ' positive ', '😪': ' negative ', '😊': ' positive ',
    '?': ' ? ', '😁': ' positive ', '💖': ' positive ', '😟': ' negative ', '😭': ' negative ',
    '💯': ' positive ', '💗': ' positive ', '♡': ' positive ', '💜': ' positive ', '🤗': ' positive ',
    '^^': ' positive ', '😨': ' negative ', '☺': ' positive ', '💋': ' positive ', '👌': ' neutral ',
    '😖': ' negative ', '😀': ' positive ', ':((': ' negative ', '😡': ' negative ', '😠': ' negative ',
    '😒': ' negative ', '🙂': ' neutral ', '😏': ' negative ', '😝': ' positive ', '😄': ' positive ',
    '😙': ' positive ', '😤': ' negative ', '😎': ' positive ', '😆': ' positive ', '💚': ' positive ',
    '✌': ' positive ', '💕': ' positive ', '😞': ' negative ', '😓': ' negative ', '️🆗️': ' positive ',
    '😉': ' positive ', '😂': ' positive ', ':v': '  positive ', '=))': '  positive ', '😋': ' positive ',
    '💓': ' positive ', '😐': ' neutral ', ':3': ' positive ', '😫': ' negative ', '😥': ' negative ',
    '😃': ' positive ', '😬': ' 😬 ', '😌': ' 😌 ', '💛': ' positive ', '🤝': ' positive ', '🎈': ' positive ',
    '😗': ' neutral ', '🤔': ' neutral ', '😑': ' negative ', '🔥': ' negative ', '🙏': ' negative ',
    '🆗': ' positive ', '😻': ' positive ', '💙': ' positive ', '💟': ' positive ',
    '😚': ' positive ', '❌': ' negative ', '👏': ' positive ', ';)': ' positive ', '<3': ' positive ',
    '🌝': ' positive ', '🌷': ' positive ', '🌸': ' positive ', '🌺': ' positive ',
    '🌼': ' positive ', '🍓': ' positive ', '🐅': ' positive ', '🐾': ' positive ', '👉': ' positive ',
    '💐': ' positive ', '💞': ' positive ', '💥': ' positive ', '💪': ' positive ',
    '💰': ' positive ', '😇': ' positive ', '😛': ' positive ', '😜': ' positive ',
    '🙃': ' positive ', '🤑': ' positive ', '🤪': ' positive ', '☹': ' negative ', '💀': ' negative ',
    '😔': ' negative ', '😧': ' negative ', '😩': ' negative ', '😰': ' negative ', '😳': ' negative ',
    '😵': ' negative ', '😶': ' negative ', '🙁': ' negative ',
    # Chuẩn hóa 1 số sentiment words/English words
    ':))': '  positive ', ':)': ' positive ', 'ô kêi': ' ok ', 'okie': ' ok ', ' o kê ': ' ok ',
    'okey': ' ok ', 'ôkê': ' ok ', 'oki': ' ok ', ' oke ': ' ok ', ' okay': ' ok ', 'okê': ' ok ',
    ' tks ': u' cám ơn ', 'thks': u' cám ơn ', 'thanks': u' cám ơn ', 'ths': u' cám ơn ', 'thank': u' cám ơn ',
    '⭐': 'star ', '*': 'star ', '🌟': 'star ', '🎉': u' positive ',
    'kg ': u' không ', 'not': u' không ', u' kg ': u' không ', '"k ': u' không ', ' kh ': u' không ', 'kô': u' không ',
    'hok': u' không ', ' kp ': u' không phải ', u' kô ': u' không ', '"ko ': u' không ', u' ko ': u' không ',
    u' k ': u' không ', 'khong': u' không ', u' hok ': u' không ',
    'he he': ' positive ', 'hehe': ' positive ', 'hihi': ' positive ', 'haha': ' positive ', 'hjhj': ' positive ',
    ' lol ': ' negative ', ' cc ': ' negative ', 'cute': u' dễ thương ', 'huhu': ' negative ', ' vs ': u' với ',
    'wa': ' quá ', 'wá': u' quá', 'j': u' gì ', '“': ' ',
    ' sz ': u' cỡ ', 'size': u' cỡ ', u' đx ': u' được ', 'dk': u' được ', 'dc': u' được ', 'đk': u' được ',
    'đc': u' được ', 'authentic': u' chuẩn chính hãng ', u' aut ': u' chuẩn chính hãng ',
    u' auth ': u' chuẩn chính hãng ', 'thick': u' positive ', 'store': u' cửa hàng ',
    'shop': u' cửa hàng ', 'sp': u' sản phẩm ', 'gud': u' tốt ', 'god': u' tốt ', 'wel done': ' tốt ', 'good': u' tốt ',
    'gút': u' tốt ',
    'sấu': u' xấu ', 'gut': u' tốt ', u' tot ': u' tốt ', u' nice ': u' tốt ', 'perfect': 'rất tốt',
    'bt': u' bình thường ',
    'time': u' thời gian ', 'qá': u' quá ', u' ship ': u' giao hàng ', u' m ': u' mình ', u' mik ': u' mình ',
    'ể': 'ể', 'product': 'sản phẩm', 'quality': 'chất lượng', 'chat': ' chất ', 'excelent': 'hoàn hảo', 'bad': 'tệ',
    'fresh': ' tươi ', 'sad': ' tệ ',
    'date': u' hạn sử dụng ', 'hsd': u' hạn sử dụng ', 'quickly': u' nhanh ', 'quick': u' nhanh ', 'fast': u' nhanh ',
    'delivery': u' giao hàng ', u' síp ': u' giao hàng ',
    'beautiful': u' đẹp tuyệt vời ', u' r ': u' rồi ', u' shopE ': u' cửa hàng ',
    u' order ': u' đặt hàng ',
    'chất lg': u' chất lượng ', u' sd ': u' sử dụng ', u' dt ': u' điện thoại ', u' nt ': u' nhắn tin ',
    u' tl ': u' trả lời ', u' sài ': u' xài ', u'bjo': u' bao giờ ',
    'thik': u' thích ', u' sop ': u' cửa hàng ', ' fb ': ' facebook ', ' face ': ' facebook ', ' very ': u' rất ',
    u'quả ng ': u' quảng  ',
    'dep': u' đẹp ', u' xau ': u' xấu ', 'delicious': u' ngon ', u'hàg': u' hàng ', u'qủa': u' quả ',
    'iu': u' yêu ', 'fake': u' giả mạo ', 'trl': 'trả lời', '><': u' positive ',
    ' por ': u' tệ ', ' poor ': u' tệ ', 'ib': u' nhắn tin ', 'rep': u' trả lời ', u'fback': ' feedback ',
    'fedback': ' feedback '
}


def replace_icons(text):
    for x, y in replace_list.items():
        text = text.replace(x, y)

    return text


def process(text):
    text = text.lower()
    text = remove_stopword(text, get_stopword())

    word_list = text.split()
    len_text_list = len(word_list)

    for i in range(len_text_list):
        if word_list[i] in not_list:  # xử lí vấn đề phủ địnnh (vd: áo này chẳng đẹp => áo này notpos)
            numb_word = 2 if len_text_list - i - 1 >= 4 else len_text_list - i - 1

            for j in range(numb_word):
                if word_list[i + j + 1] in pos_list:
                    word_list[i] = "notpos"
                    word_list[i + j + 1] = ""

                if word_list[i + j + 1] in nag_list:
                    word_list[i] = "notnag"
                    word_list[i + j + 1] = ""

        else:  # Thêm feature cho những sentiment words (áo này đẹp--> áo này đẹp positive)
            if word_list[i] in pos_list:
                word_list.append('positive')
            elif word_list[i] in nag_list:
                word_list.append('negative')
            elif word_list[i] in neu_list:
                word_list.append('neutral')

    # chuyển word list thành text string
    text = " ".join(word_list)

    # remove nốt những ký tự thừa thãi
    text = text.replace(u'"', u' ')
    text = text.replace(u'️', u'')
    text = text.replace('🏻', '')

    return text


# string = "Đồ uống được ship đến nhà trong một cái cốc xấu xí èo uột, nắp lỏng lẻo đến độ vừa mới nghiêng cốc 1 chút thì nắp bung ra đổ lênh láng ra bàn. Gọi matcha machiato ít ngọt nhưng pha cực ngọt, không thể uống nổi, machiato quánh lại thành cục ( nhìn ảnh thì thấy ngay), ngoáy mạnh vẫn không tan được, ăn ..."
# print(process(string))

VN_CHARS_LOWER = u'ạảãàáâậầấẩẫăắằặẳẵóòọõỏôộổỗồốơờớợởỡéèẻẹẽêếềệểễúùụủũưựữửừứíìịỉĩýỳỷỵỹđð'
VN_CHARS_UPPER = u'ẠẢÃÀÁÂẬẦẤẨẪĂẮẰẶẲẴÓÒỌÕỎÔỘỔỖỒỐƠỜỚỢỞỠÉÈẺẸẼÊẾỀỆỂỄÚÙỤỦŨƯỰỮỬỪỨÍÌỊỈĨÝỲỶỴỸÐĐ'
VN_CHARS = VN_CHARS_LOWER + VN_CHARS_UPPER


def no_marks(s):
    __INTAB = [ch for ch in VN_CHARS]
    __OUTTAB = "a" * 17 + "o" * 17 + "e" * 11 + "u" * 11 + "i" * 5 + "y" * 5 + "d" * 2
    __OUTTAB += "A" * 17 + "O" * 17 + "E" * 11 + "U" * 11 + "I" * 5 + "Y" * 5 + "D" * 2
    __r = re.compile("|".join(__INTAB))
    __replaces_dict = dict(zip(__INTAB, __OUTTAB))
    result = __r.sub(lambda m: __replaces_dict[m.group(0)], s)
    return result


class DataSource(object):
    def _load_raw_data(self, filename, is_train=True):

        a = []
        b = []

        regex = 'train_'
        if not is_train:
            regex = 'test_'

        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                if regex in line:
                    b.append(a)
                    a = [line]
                elif line != '\n':
                    a.append(line)
        b.append(a)

        return b[1:]

    def _create_row(self, sample, is_train=True):
        d = {}
        d['id'] = sample[0].replace('\n', '')
        review = ""

        if is_train:
            for clause in sample[1:-1]:
                review += clause.replace('\n', ' ')
                review = review.replace('.', ' ')

            d['label'] = int(sample[-1].replace('\n', ' '))
        else:
            for clause in sample[1:]:
                review += clause.replace('\n', ' ')
                review = review.replace('.', ' ')

        d['review'] = review

        return d

    def load_data(self, filename, is_train=True):
        raw_data = self._load_raw_data(filename, is_train)
        lst = []

        for row in raw_data:
            lst.append(self._create_row(row, is_train))

        return lst

    def transform_to_dataset(self, x_set, y_set):
        X, y = [], []
        for document, topic in zip(list(x_set), list(y_set)):
            document = process(document)
            X.append(document.strip())
            y.append(topic)
            # Augmentation bằng cách remove dấu tiếng Việt
            X.append(no_marks(document))
            y.append(topic)
        return X, y


ds = DataSource()
train_data = pd.DataFrame(ds.load_data('comments.txt'))
new_data = []

# Thêm mẫu bằng cách lấy trong từ điển Sentiment (nag/pos)
for index, row in enumerate(pos_list):
    new_data.append(['pos' + str(index), '1', row])
for index, row in enumerate(nag_list):
    new_data.append(['nag' + str(index), '-1', row])
for index, row in enumerate(neu_list):
    new_data.append(['neu' + str(index), '0', row])

new_data = pd.DataFrame(new_data, columns=list(['id', 'label', 'review']))
train_data.append(new_data)
# test_data = pd.DataFrame(ds.load_data('Data/test.txt', is_train=False))

# Try some models
classifiers = [
    # LinearSVC(fit_intercept = True,multi_class='crammer_singer', C=1),
    KNeighborsClassifier(),
    # GaussianNB(),
    # SVC(),
]

"con số thực tế là 42, 0, 21, ... Điều quan trọng là mỗi khi bạn sử dụng 42, bạn sẽ luôn nhận được cùng một đầu ra trong lần đầu tiên bạn thực hiện phân tách."
X_train, X_test, y_train, y_test = train_test_split(train_data.review, train_data.label, test_size=0.1, random_state=42)
X_train, y_train = ds.transform_to_dataset(X_train, y_train)


# X_test, y_test = ds.transform_to_dataset(X_test, y_test)
class DenseTransformer(TransformerMixin):
    def transform(self, X, y=None, **fit_params):
        return X.todense()

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        return self.transform(X)

    def fit(self, X, y=None, **fit_params):
        return self


# THÊM STOPWORD LÀ NHỮNG TỪ KÉM QUAN TRỌNG
model_name = ['KNeighborsClassifier', 'GaussianNB', 'SVC']
count = 0

print("X_test: \n", X_test.to_frame())
print(type(X_test))


def model(classifier, X_train, y_train):
    steps = []
    steps.append(('CountVectorizer', CountVectorizer(ngram_range=(1, 5))))
    steps.append(('tfidf', TfidfTransformer(use_idf=False, sublinear_tf=True, norm='l2', smooth_idf=True)))
    # steps.append(('to_dense', DenseTransformer()))
    steps.append(('classifier', classifier))
    clf = Pipeline(steps)
    clf.fit(X_train, y_train)
    joblib.dump(clf, 'model.pkl')
    y_pred = clf.predict(X_test)
    print("classification_report rate=9/1")
    print(classification_report(y_test, y_pred))
    print("accuracy_score")
    print(accuracy_score(y_test, y_pred))
    print("confusion matrix")
    print(confusion_matrix(y_test, y_pred))
    print("f1-score")
    print(f1_score(y_test, y_pred, average='micro'))
    print("--------------------------------------------------")
    cross_score = cross_val_score(clf, X_train, y_train, cv=5)
    print('DATASET LEN %d' % (len(X_train)))
    print("CROSSVALIDATION 5 FOLDS: %0.4f (+/- %0.4f)" % (cross_score.mean(), cross_score.std() * 2))
    return y_pred


for classifier in classifiers:
    print("_______" + str(model_name[count]) + "_______")
    model(classifier, X_train, y_train)
