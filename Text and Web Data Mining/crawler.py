import requests
from bs4 import BeautifulSoup
import json
import modules


stop_word = modules.get_stopword()

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

                    print(f"#{i['ReviewId']}\n")
                    write_file.write(f"#{i['ReviewId']}\n")

                    # replace icon with positive and negative
                    text = modules.replace_icons(i['Comment'].replace('. \n', '. ').replace('.\n', '.').replace('\n', '. ') + "\n")
                    # lower string and remove stopword
                    write_file.write(modules.remove_stopword(text.lower(), stop_word) + "\n")

                    # convert rating to 1, -1, 0
                    write_file.write(f"{modules.convert_rating(i['AvgRating'])}\n\n")

            url = file.readline()

print(f"Đã lấy được {count} bình luận!")
write_file.close()
