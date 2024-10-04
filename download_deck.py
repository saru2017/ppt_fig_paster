import argparse
import sys
import requests
import re
import os
from bs4 import BeautifulSoup


parser = argparse.ArgumentParser(description="excel hoge hoge")
parser.add_argument("code", help="filename hog hoge")

args = parser.parse_args()
code = args.code

# URLを指定
url_base = "https://www.pokemon-card.com/deck/result.html/deckID/"


url = url_base + code + "/"

# ページの内容を取得
response = requests.get(url)
html_content = response.content

# BeautifulSoupでHTMLを解析
soup = BeautifulSoup(html_content, 'html.parser')

# formタグのid="inputArea"を持つ部分を探し、form全体を取得
form_content = soup.find('form', {'id': 'inputArea'})


card_num_array = {}

# value属性を持つ全ての要素を探して、値をリストに格納
if form_content:
    values = [element.get('value') for element in form_content.find_all() if element.get('value') is not None]
    # 値を列挙
    
    for value in values:
        cards = value.split("-")
#        print(cards)
        for card in cards:
            items = card.split("_")
            if len(items) != 3:
                continue
            print(items)
            card_num_array[items[0]] = int(items[1])
            
        
#        print(value)
else:
    print("指定されたformが見つかりませんでした。")

print(card_num_array)

pattern = r"PCGDECK\.searchItemCardPict\[\d+\]='[^']+';"
#pattern = r"<script>(PCGDECK.*?);PCGDECK.viewItemMode=2;</script>"
#matches = re.search(pattern, html_content, re.DOTALL)
print(html_content)
matches = re.findall(pattern, html_content.decode('utf-8'))

card_url_array = {}

for match in matches:
    print(match)
    pattern = r"PCGDECK\.searchItemCardPict\[(\d+)\]='([^']+)';"
    item = re.search(pattern, match)
    key = item.group(1)
    value = item.group(2)
    card_url_array[key] = value

print(card_url_array)

url_base = "https://www.pokemon-card.com"

#print(card_url_array["41737"])
#exit(1)

for key, value in card_url_array.items():
    num_files = card_num_array[key]
    url = url_base + value
    print(url, num_files)

    original_filename = os.path.basename(url)
    name, ext = os.path.splitext(original_filename)  # 拡張子を分けて抽出

    # 画像をダウンロード
    response = requests.get(url)

    # 画像を保存するファイル名を生成して保存
    if response.status_code == 200:  # リクエストが成功した場合
        for i in range(num_files):
            new_filename = f"data/{name}_{i}{ext}"
            with open(new_filename, 'wb') as f:
                f.write(response.content)
        print(f"{num_files}枚の画像が正常に保存されました。")
    else:
        print("画像のダウンロードに失敗しました。")
    

exit(1)
    
# 結果を表示
if form_content:
    print(form_content.prettify())
else:
    print("指定されたformが見つかりませんでした。")
