import re

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with open("crawled_websites.txt", "r", encoding="utf8") as file:
        text = file.read()
    text = text.split("-----")
    with open("crawled_data.txt", "w", encoding="utf8") as datafile:
        for chunk_of_text in text:
            if not re.search("https://www.comics.org/.*", chunk_of_text):
                continue
            url = re.search("https://www.comics.org/.*", chunk_of_text).group()

            datafile.write(url + "\n")
            print(url)
            if re.search("/details/.*", url):
                matches = re.findall('<th.*?>.*?</th>|<td.*?>.*?</td>', chunk_of_text)
                for match in matches:
                    if not match:
                        continue
                    match = re.sub('<.*?>|&nbsp;', "", match)
                    match = re.sub('^ ', "", match)
                    if not match or match == " ":
                        continue
                    datafile.write(match + "\n")
                    #print(match)
            elif re.search("/history/", url):
                continue
            elif re.search("/series/.*", url):
                match_dl = re.findall('<dl.*>((.|\n)*)</dl>', chunk_of_text)
                match_title = re.search('<title>.*', chunk_of_text).group()
                match_title = re.sub("<.*?>", "", match_title)
                match_title = match_title.replace("\n", " ")
                match_title = re.sub(' +', " ", match_title)
                #print(match_title[1:-1])
                datafile.write(match_title[1:-1] + "\n")
                for chunk in match_dl[0][0].split("<dt"):
                    chunk = re.sub("(class=\".*>)|(<dd id=\".*>)|(^>)", "", chunk)
                    chunk = chunk.replace("\n", " ")
                    chunk = re.sub(' +', " ", chunk)
                    #print(chunk[1:-1])
                    datafile.write(chunk[1:-1] + "\n")

            datafile.write("-----\n")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
