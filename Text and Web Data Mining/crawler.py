import requests
from bs4 import BeautifulSoup


# url = "https://www.foody.vn/thuong-hieu/lotteria-ga-ran-sai-gon?c=ho-chi-minh"
def convert_rating(number):
    if number <= 4:
        return -1
    elif number >= 7:
        return 1
    else:
        return 0


count = 0
with open("comments.txt", "w") as write_file:

    with open("urls.txt", "r") as file:
        url = file.readline()

        while url:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html5lib")

            for x in soup.find_all("h2")[:-1]:
                response = requests.get(f"https://www.foody.vn{x.a['href']}/binh-luan")
                soup = BeautifulSoup(response.content, "html5lib")

                # for comment in soup.find_all("div", class_="rd-des toggle-height"):
                #     print(comment.span.text)

                for y in soup.find_all("div", class_="review-des fd-clearbox")[:-3]:
                    count += 1
                    comment = y.find_all("div")[1].span.text.replace('. \n', '. ').replace('.\n', '.').replace('\n', '. ')
                    rating = y.find_all("div")[0].span.text
                    print(f"train_{count}")
                    print(comment)
                    print(rating)
                    print()

                    write_file.write(f"train_{count}\n")
                    write_file.write(f'"{comment}"\n')
                    write_file.write(str(convert_rating(float(rating))) + "\n\n")

print(f"Đã lấy được {count} đánh giá!")
write_file.close()
