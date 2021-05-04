import requests
import json
import csv
import time
import numpy as npy
from PIL import Image
from datetime import datetime
from bs4 import BeautifulSoup

import jieba
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


USER_ID = "1062839290"
CONTAINER_ID = "1076031062839290"
COOKIE = "_T_WM=10171743382; WEIBOCN_FROM=1110006030; XSRF-TOKEN=159e76; loginScene=102003; SCF=AoeA2cziCpTgDc-nSGcLM-nbehDfn8dp3Ui9TSCUworY03mWbk6YPKdmacF5hHQvcpTLV5YGY-mruARWc6LPYoo.; SUB=_2A25NlV5LDeRhGeFI61YW-CjLzzyIHXVvdmIDrDV6PUJbktANLVH3kW1NfXpJtn8MsuDiheD5pxQYBSLKHpKPbgK0; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5XIxEq1c8Z8NnqyFuQdih05JpX5KzhUgL.FoMcehBN1hqNSh52dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNSo5XS0ncS0B7; SSOLoginState=1620127259; ALF=1622719259; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4631726607308751%26luicode%3D20000061%26lfid%3D4631726607308751%26uicode%3D20000061%26fid%3D4631726607308751"


def get_user_info(user_id: str):
    url = "https://m.weibo.cn/api/container/getIndex?is_hot[]=1&is_hot[]=1&jumpfrom=weibocom&type=uid&value=" + user_id
    data = requests.get(url).text
    try:
        content = json.loads(data)
        userinfo = content["data"]["userInfo"]
        name = userinfo['screen_name']
        desc = userinfo['description']
        gender = "female" if userinfo['gender'] == 'f' else "male"
        followers = userinfo['followers_count']
        follow = userinfo['follow_count']
        with open("result/userinfo.txt", "w") as f:
            f.write("username: {}\ndescription: {}\ngender: {}\nfollowers_count: {}\nfollow_count: {}".format(name, desc, gender, followers, follow))
    except Exception as e:
        print("[ERROR][get_user_info] ", end='')
        print(e)


def get_content_last10(user_id: str, cont_id: str):
    url = "https://m.weibo.cn/api/container/getIndex?type=uid&value={}&containerid={}".format(user_id, cont_id)
    data = requests.get(url).text
    try:
        content = json.loads(data)
        for i in range(len(content['data']['cards'])):
            try:
                mblog = content['data']['cards'][i]['mblog']
                source = mblog['source']
                created_at = mblog['created_at']
                cont = mblog['text']
                attitudes_count = mblog["attitudes_count"]
                comments_count = mblog["comments_count"]
                reposts_count = mblog["reposts_count"]
                with open("result/usercontent_last10.txt", "a+") as f:
                    f.writelines("date: {}\nclient: {}\ncontent: {}\nattitudes_count: {}\ncomments_count: {}\nreposts_count: {}\n\n"\
                                 .format(created_at, source, cont, attitudes_count, comments_count, reposts_count))
            except Exception as e:
                print("[ERROR][get_content_list10][loop][{}] ".format(i), end='')
                print(e)
                continue
    except Exception as e:
        print("[ERROR][get_content_list10] ", end='')
        print(e)


def get_containerid(url):
    data = requests.get(url).text
    content = json.loads(data).get('data')
    for cont in content.get('tabsInfo').get('tabs'):
        if cont.get('tab_type') == 'weibo':
            containerid = cont["containerid"]
    return containerid


def get_full_content(contori: str) -> str:
    sp = BeautifulSoup(contori, "html.parser")
    url = ""
    cont = ""
    for s in sp.find_all("a"):
        s = s["href"]
        #print("[DEBUG][get_full_content][a tag] " + s)
        if "/status/" in s:
            url = "https://m.weibo.cn/statuses/extend?id=" + s[8:]
            #print("[DEBUG][get_full_content][URL] " + url)
            try:
                headers = {
                    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
                    'Cookie': COOKIE
                }
                data = requests.get(url=url, headers=headers).text
                cont = json.loads(data).get("data").get("longTextContent")
                return BeautifulSoup(cont, "html.parser").get_text()
            except Exception as e:
                print("[ERROR][get_full_content] ", end='')
                print(e)
                break
    return "ERR"


def get_content_all(user_id: str):
    pageCounter = 1
    while True:
        url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + user_id
        contentURL = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + user_id + '&containerid=' + get_containerid(url) + '&page=' + str(pageCounter)
        try:
            time.sleep(1)
            data = requests.get(contentURL).text
            cards = json.loads(data).get("data").get("cards")
            if len(cards) > 0:
                for i in range(len(cards)):
                    print("[SYS] Progress: page {}, weibo {}".format(pageCounter, i))
                    if cards[i].get("card_type") == 9:
                        # print("[DEBUG][get_content_all][data] " + data)
                        mblog = cards[i].get('mblog')
                        attitudes_count = mblog.get('attitudes_count')
                        comments_count = mblog.get('comments_count')
                        created_at = mblog.get('created_at')
                        reposts_count = mblog.get('reposts_count')
                        scheme = cards[i].get('scheme')
                        cont = mblog.get('text')
                        if ">全文</a>" in cont:
                            cont = get_full_content(cont)
                        cont = BeautifulSoup(cont, "html.parser").get_text()
                        with open("result/usercontent.txt", 'a+', encoding='utf-8') as f:
                            f.write("\npage {}, weibo {}\n".format(pageCounter, i))
                            f.write("scheme: " + str(scheme) + "\n" + "created_at: " + str(created_at) + "\n"
                                    + "content: " + cont + "\n" + "attitudes_count: " + str(attitudes_count)
                                    + "\n" + "comments_count: " + str(comments_count) + "\n" + "reposts_count: "
                                    + str(reposts_count) + "\n")
                        with open("result/result.csv", 'a+', newline='', encoding='utf-8') as f:
                            f_csv = csv.writer(f)
                            f_csv.writerow([created_at, cont.encode('utf-8').decode('utf-8'), attitudes_count, comments_count, reposts_count, scheme])
                pageCounter += 1
            else:
                break
        except Exception as e:
            print("[ERROR][get_content_all][pageloop][{}] ".format(pageCounter), end='')
            print(e)
            break


def date_cleanup(start: datetime, end: datetime):
    if start > end:
        temp = start
        start = end
        end = temp
    with open("result/result.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            Time = row[0].replace('+0800 ', '')
            Time = datetime.strptime(Time, "%a %b %d %H:%M:%S %Y")
            if start <= Time <= end:
                with open("result/cleanup/result_cleanup.csv", 'a+', newline='', encoding='utf-8') as o:
                    f_csv = csv.writer(o)
                    f_csv.writerow(row)
                with open("result/cleanup/usercontent_cleanup.txt", 'a+', encoding='utf-8') as o:
                    o.write("created_at: " + row[0] + "\ncontent: " + row[1].encode('utf-8').decode('utf-8')
                            + "\nattitudes_count: " + row[2] + "\ncomments_count: " + row[3] + "\nreposts_count: "
                            + row[4] + "\nscheme: " + row[5] + "\n\n")
                with open("result/cleanup/word.txt", "a+", newline='', encoding='utf-8') as o:
                    o.write(row[1].encode('utf-8').decode('utf-8'))


def generate_wordcloud():
    file = open("result/cleanup/word.txt", "r", encoding='utf-8').read()
    file = file.replace("微博", "")
    file = file.replace("视频", "")
    file = file.replace("的", "")
    stopwords = set(STOPWORDS)
    mask = npy.array(Image.open("img/background/0_waifu2x_art_noise2_scale_tta_1.png"))
    word_cut = jieba.cut(file)
    content = " ".join(word_cut)
    wc = WordCloud(
        font_path="font/wqy zenhei.ttf",
        background_color="white",
        mask=mask,
        #stopwords=stopwords
    )
    wc.generate(content)
    wc.to_file("result/cleanup/wordcloud.jpg")
    image_colors = ImageColorGenerator(mask)
    wc = wc.recolor(color_func=image_colors)
    wc.to_file("result/cleanup/wordcloud_color.jpg")
    wc = WordCloud(
        font_path="font/wqy zenhei.ttf",
        background_color="white",
        # mask=mask,
        width=1920, height=1080,
        stopwords=stopwords
    )
    wc.generate(content)
    wc.to_file("result/cleanup/wordcloud.jpg")

if __name__ == '__main__':
    #get_user_info(USER_ID)
    #get_content_last10(USER_ID, CONTAINER_ID)
    #get_content_all(USER_ID)
    date_cleanup(datetime(2019, 8, 17), datetime(2020, 8, 17))
    generate_wordcloud()
    pass