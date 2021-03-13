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
    with pen("stopword.txt", encoding="utf-8") as file:
        text = file.read()

        for word in text.split():
            stop_word.append(word)

        file.close()

    # trả về stop word lấy từ file và những kí tự đặc biệt từ string.punctuation
    return stop_word + list(string.punctuation)


def remove_stopword(text, stop_word):
    text = word_tokenize(text)  # ghép những từ có nghĩa lại với nhau
    result = ""

    for word in text:
        if word not in stop_word and not check_number(word):
            result += word + " "

    return result
