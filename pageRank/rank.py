from re import compile
from igraph import Graph
from collections import defaultdict

inputFile = "F:/battles15-16.txt"


SCORE_PATTEN = compile("[0-9]+")
TEAM76_PATTEN = compile("76人")

def preprocess():
    """
    从battles中读比赛数据，将它整理成模型需要的形式
    将每一场比赛组成一个tuple，输者在前，赢者在后
    :return: list of tuple
    """
    res = []
    with open(inputFile, encoding="utf8", mode="r") as handle:
        for line in handle:


            line = TEAM76_PATTEN.sub("七六人", line.strip())

            doubleSide = line.split(",")[1]
            # 比赛一方
            oneSide = doubleSide.split("-")[0]
            # 一方得分
            oneScore = SCORE_PATTEN.findall(oneSide)[0]
            # 比赛另一方
            otherSide = doubleSide.split("-")[1]
            # 另一方得分
            otherScore = SCORE_PATTEN.findall(otherSide)[0]

            oneTeam = SCORE_PATTEN.sub("", oneSide)
            otherTeam = SCORE_PATTEN.sub("", otherSide)
            if int(oneScore) < int(otherScore):
                res.append((oneTeam, otherTeam))
            else:
                res.append((otherTeam, oneTeam))
    return res

edges = preprocess()

edgesAndWeight = defaultdict(int)
for loser, winner in edges:
    edgesAndWeight[(loser, winner)] = +1

teams = list(set([elem[1] for elem in edges]))
vNum = len(teams)


battleG = Graph(vNum, directed=True)
battleG.vs["name"] = teams
battleG.add_edges(edges)

# for pair, weight in edgesAndWeight.items():
#     loser = pair[0]
#     winner = pair[1]
#     battleG.add_edge(loser, winner, weight = weight)


ranks = battleG.pagerank(damping=0.85, vertices=teams, niter=1500)

teamRankPair = [(team, rank) for team, rank in zip(teams, ranks)]

for team, rank in sorted(teamRankPair, key=lambda x: x[1], reverse=True):
    print(team, rank)


team = "凯尔特"
print(battleG.outdegree(team), battleG.indegree(team))

