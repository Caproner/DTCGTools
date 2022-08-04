from bs4 import BeautifulSoup
from urllib import request
from tqdm import tqdm
import argparse
import time
import random
import os
import pickle

def get_effect(s):
    ret = ""
    ck = False
    for i in range(len(s)):
        c = s[i]
        if c == '<':
            ck = True
            if (i + 4 < len(s) and s[i:i+4] == '<br>') or (i + 5 < len(s) and s[i:i+5] == '<br/>'):
                ret += '\n'
            continue
        if c == '>':
            ck = False
            continue
        if ck:
            continue
        ret += c
    return ret

def get_single_card(pack, url):
    card_dict = dict()
    html = request.urlopen(url)
    soup = BeautifulSoup(html.read(), "lxml")
    card_html = soup.find_all('div', class_="card")[0]
    card_dict['img_url'] = card_html.contents[0].div.img['data-src']
    card_dict['name'] = card_html.contents[2].div.contents[0].contents[-1].get_text().strip()
    card_dict['name_jp'] = card_html.contents[2].div.contents[2].contents[-1].get_text().strip()
    card_dict['type'] = card_html.contents[2].div.contents[4].contents[-1].get_text().strip()
    if card_dict['type'] == '数码蛋卡':
        card_dict['color'] = card_html.contents[2].div.contents[8].contents[-1].get_text().strip()
        card_dict['id'] = card_html.contents[2].div.contents[10].contents[-1].get_text().strip()
        card_dict['rarity'] = card_html.contents[2].div.contents[12].contents[-1].get_text().strip()
        card_dict['feature_1'] = card_html.contents[2].div.contents[16].contents[-1].get_text().strip()
        card_dict['feature_2'] = card_html.contents[2].div.contents[18].contents[-1].get_text().strip()
        card_dict['feature_3'] = card_html.contents[2].div.contents[20].contents[-1].get_text().strip()
        card_dict['level'] = int(card_html.contents[2].div.contents[30].contents[-1].get_text().strip())
        card_dict['effect'] = ""
        for i in range(3, len(card_html)):
            if (len(card_html.contents[i].get_text().strip()) == 0):
                continue
            card_dict['effect'] += get_effect(str(card_html.contents[i]).strip())
            card_dict['effect'] += '\n'
    elif card_dict['type'] == '数码兽卡':
        card_dict['color'] = card_html.contents[2].div.contents[8].contents[-1].get_text().strip()
        card_dict['id'] = card_html.contents[2].div.contents[10].contents[-1].get_text().strip()
        card_dict['rarity'] = card_html.contents[2].div.contents[12].contents[-1].get_text().strip()
        card_dict['feature_1'] = card_html.contents[2].div.contents[16].contents[-1].get_text().strip()
        card_dict['feature_2'] = card_html.contents[2].div.contents[18].contents[-1].get_text().strip()
        card_dict['feature_3'] = card_html.contents[2].div.contents[20].contents[-1].get_text().strip()
        card_dict['level'] = int(card_html.contents[2].div.contents[30].contents[-1].get_text().strip())
        card_dict['cost'] = int(card_html.contents[2].div.contents[32].contents[-1].get_text().strip())
        card_dict['dp'] = int(card_html.contents[2].div.contents[34].contents[-1].get_text().strip())
        card_dict['evo_cost'] = list()
        for i in range(2, len(card_html.contents[2].div.contents[36])):
            card_dict['evo_cost'].append(card_html.contents[2].div.contents[36].contents[i].get_text().strip())
        card_dict['effect'] = ""
        for i in range(3, len(card_html)):
            if (len(card_html.contents[i].get_text().strip()) == 0):
                continue
            card_dict['effect'] += get_effect(str(card_html.contents[i]).strip())
            card_dict['effect'] += '\n'
    elif card_dict['type'] == '驯兽师卡' or card_dict['type'] == '选项卡':
        card_dict['color'] = card_html.contents[2].div.contents[8].contents[-1].get_text().strip()
        card_dict['id'] = card_html.contents[2].div.contents[10].contents[-1].get_text().strip()
        card_dict['rarity'] = card_html.contents[2].div.contents[12].contents[-1].get_text().strip()
        card_dict['cost'] = int(card_html.contents[2].div.contents[16].contents[-1].get_text().strip())
        card_dict['effect'] = ""
        for i in range(3, len(card_html)):
            if (len(card_html.contents[i].get_text().strip()) == 0):
                continue
            card_dict['effect'] += get_effect(str(card_html.contents[i]).strip())
            card_dict['effect'] += '\n'

    else:
        return
    # print("MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM")
    # print("--------------------------------------------------")
    # for k in card_dict:
    #     if (k == 'effect'):
    #         print(k + ": ")
    #         print(card_dict[k])
    #     else:
    #         print(k + ": " + str(card_dict[k]))
    # print("--------------------------------------------------")
    # print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")

    folder_name = "database/" + pack + "/" + card_dict['id']
    os.system("mkdir -p " + folder_name)
    request.urlretrieve(card_dict['img_url'], filename=folder_name + "/" + card_dict['id'] + ".jpg")
    with open(folder_name + "/data.pkl", "wb") as f:
        pickle.dump(card_dict, f)




def main(pack):
    os.system("mkdir -p database/" + pack)
    os.system("rm -rf dataabse/" + pack + "/*")

    request_url = "http://digimon.card.moe/Package/" + pack
    html = request.urlopen(request_url)
    soup = BeautifulSoup(html.read(), "lxml")
    card_list = soup.find_all('div', class_='list')[0]
    for i in tqdm(range(len(card_list.contents))):
        card = card_list.contents[i]
        card_url = "http://digimon.card.moe" + card.h2.a['href']
        get_single_card(pack, card_url)
        time.sleep(random.random() * 5)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--pack", type=str)
    args = parser.parse_args()

    main(args.pack)