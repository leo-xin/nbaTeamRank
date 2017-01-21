import requests
from bs4 import BeautifulSoup



def parse_battles(url):
    """
    从传入的url中，解析出对应页面中包含的比赛和比赛时间
    :param url:
    :return: list of tuple，tuple的第一个元素是是比赛时间，第二个是比赛详情
    """

    r = requests.get(url=url)
    r.encoding = "utf8"
    bsTree = BeautifulSoup(r.text, "lxml")
    relevancePart = bsTree.find_all(name=["div"], attrs={"class": "cheight"})
    battles = []
    for part in relevancePart:
        # 过滤掉没有font标签的部分
        if part.br is None:
            continue
        date = part.font.get_text()
        plays = part.find_all(name="a", attrs={"target": "_blank"})
        for play in plays:
            battles.append((date, play.get_text()))
    return battles


if __name__ == "__main__":
    from time import sleep
    from random import random

    outPath = "F:/battles15-16.txt"
    months = ["2015-10", "2015-11", "2015-12", "2016-01",
              "2016-02", "2016-03", "2016-04", "2016-05",
              "2016-06"]
    urls = ["http://www.stat-nba.com/gameList_simple-%s.html" %m
            for m in months]

    with open(outPath, mode="w", encoding="utf8") as handle:
        for url in urls:
            battleInOneMonth = parse_battles(url)
            sleep(random())
            for battle in battleInOneMonth:
                line = battle[0] + "," + battle[1]
                handle.write(line)
                handle.write("\n")