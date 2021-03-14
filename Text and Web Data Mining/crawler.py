import requests
from bs4 import BeautifulSoup
import json


def convert_rating(rating):
    if rating <= 4:
        return -1
    elif rating >= 7:
        return 1
    else:
        return 0


with open("comments.txt", "w") as write_file:
    count = 0

    with open("urls.txt", "r") as file:
        url = file.readline()

        while url:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html5lib")

            script = soup.find_all("script")[12].text.split("\n")[3].rstrip().lstrip().replace("var initDataRes=", "")
            dictionary = json.loads(script[:-1])

            # print(json.dumps(dictionary, indent=4, ensure_ascii=False))

            for x in dictionary["Items"]:
                for i in x["LstReview"]:
                    count += 1

                    # replace icon with positive and negative
                    text = i['Comment'].replace('. \n', '. ').replace('.\n', '.').replace('\n', '. ')
                    # lower string and remove stopword
                    write_file.write(f"train_{count}\n")
                    write_file.write(f'"{text}"\n')
                    write_file.write(str(convert_rating(i["AvgRating"])) + "\n\n")

            url = file.readline()

print(f"Đã lấy được {count} bình luận!")
write_file.close()
