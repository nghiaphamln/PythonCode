import requests
from bs4 import BeautifulSoup
import json


with open("comments.txt", "w") as write_file:
    count = 0

    with open("urls.txt", "r") as file:
        url = file.readline()  # lấy từng url trong urls.txt để lấy đánh giá

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
                    write_file.write(i['Comment'].replace('. \n', '. ').replace('.\n', '.').replace('\n', '. ') + "\n")
                    write_file.write(f"{i['AvgRating']}\n\n")

            url = file.readline()

print(f"Đã lấy được {count} bình luận!")
write_file.close()
