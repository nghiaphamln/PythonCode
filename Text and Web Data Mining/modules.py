from underthesea import word_tokenize
import string


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
    return stop_word + list(string.punctuation)


def remove_stopword(text, stop_word):
    text = word_tokenize(text)  # ghép những từ có nghĩa lại với nhau
    result = ""

    for word in text:
        if word not in stop_word and not check_number(word):
            result += word + " "

    return result


replace_list = {
    "👹": "negative", "👻": "positive", "💃": "positive", '🤙': ' positive ', '👍': ' positive ',
    "💄": "positive", "💎": "positive", "💩": "positive", "😕": "negative", "😱": "negative", "😸": "positive",
    "😾": "negative", "🚫": "negative", "🤬": "negative", "🧚": "positive", "🧡": "positive", '🐶': ' positive ',
    '👎': ' negative ', '😣': ' negative ', '✨': ' positive ', '❣': ' positive ', '☀': ' positive ',
    '♥': ' positive ', '🤩': ' positive ', 'like': ' positive ', '💌': ' positive ',
    '🤣': ' positive ', '🖤': ' positive ', '🤤': ' positive ', ':(': ' negative ', '😢': ' negative ',
    '❤': ' positive ', '😍': ' positive ', '😘': ' positive ', '😪': ' negative ', '😊': ' positive ',
    '?': ' ? ', '😁': ' positive ', '💖': ' positive ', '😟': ' negative ', '😭': ' negative ',
    '💯': ' positive ', '💗': ' positive ', '♡': ' positive ', '💜': ' positive ', '🤗': ' positive ',
    '^^': ' positive ', '😨': ' negative ', '☺': ' positive ', '💋': ' positive ', '👌': ' positive ',
    '😖': ' negative ', '😀': ' positive ', ':((': ' negative ', '😡': ' negative ', '😠': ' negative ',
    '😒': ' negative ', '🙂': ' positive ', '😏': ' negative ', '😝': ' positive ', '😄': ' positive ',
    '😙': ' positive ', '😤': ' negative ', '😎': ' positive ', '😆': ' positive ', '💚': ' positive ',
    '✌': ' positive ', '💕': ' positive ', '😞': ' negative ', '😓': ' negative ', '️🆗️': ' positive ',
    '😉': ' positive ', '😂': ' positive ', ':v': '  positive ', '=))': '  positive ', '😋': ' positive ',
    '💓': ' positive ', '😐': ' negative ', ':3': ' positive ', '😫': ' negative ', '😥': ' negative ',
    '😃': ' positive ', '😬': ' 😬 ', '😌': ' 😌 ', '💛': ' positive ', '🤝': ' positive ', '🎈': ' positive ',
    '😗': ' positive ', '🤔': ' negative ', '😑': ' negative ', '🔥': ' negative ', '🙏': ' negative ',
    '🆗': ' positive ', '😻': ' positive ', '💙': ' positive ', '💟': ' positive ',
    '😚': ' positive ', '❌': ' negative ', '👏': ' positive ', ';)': ' positive ', '<3': ' positive ',
    '🌝': ' positive ', '🌷': ' positive ', '🌸': ' positive ', '🌺': ' positive ',
    '🌼': ' positive ', '🍓': ' positive ', '🐅': ' positive ', '🐾': ' positive ', '👉': ' positive ',
    '💐': ' positive ', '💞': ' positive ', '💥': ' positive ', '💪': ' positive ',
    '💰': ' positive ', '😇': ' positive ', '😛': ' positive ', '😜': ' positive ',
    '🙃': ' positive ', '🤑': ' positive ', '🤪': ' positive ', '☹': ' negative ', '💀': ' negative ',
    '😔': ' negative ', '😧': ' negative ', '😩': ' negative ', '😰': ' negative ', '😳': ' negative ',
    '😵': ' negative ', '😶': ' negative ', '🙁': ' negative '
}


def replace_icons(text):
    for x, y in replace_list.items():
        text = text.replace(x, y)

    return text


def convert_rating(rating):
    if rating <= 4:
        return -1
    elif rating >= 7:
        return 1
    else:
        return 0
