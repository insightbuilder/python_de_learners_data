import re
import math
import json
import os
import concurrent
from concurrent.futures import ProcessPoolExecutor
import requests
import numpy as np

from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

def procesarEntrada():
    entrada = []
    while len(entrada) != 5:
        entrada = [int(a) for a in input()[:5] if int(a) in range(0, 3)]
    return entrada


def generatePattern(entrada, word):
    pattern = ""
    procesed = {}

    for j in range(len(entrada)):
        letra = word[j]
        if letra not in procesed:
            condition = [k for k in range(j + 1, len(entrada)) if word[k] == letra and entrada[k] == 2]
            if entrada[j] == 0:
                if condition == []: procesed[letra] = 0
            else:
                procesed[letra] = 0
            pattern += [f"(?=[^{letra}]*$)" if condition == [] else f"(?!.{{{j}}}{letra})",
                        f"(?!.{{{j}}}{letra})(?=.*{letra})" + "".join(f"(?!.{{{i}}}{letra})" for i in [k for k in range(j + 1, len(entrada)) if word[k] == letra and entrada[k] in [0, 1]]),
                        f"(?=.{{{j}}}{letra})" + "".join(f"(?!.{{{i}}}{letra})" for i in [k for k in range(j + 1, len(entrada)) if word[k] == letra and entrada[k] in [0, 1]])][
                entrada[j]]
    return f"^{pattern}.*$"


def scoreWord(word, d):
    combinations = ["00000", "00001", "00002", "00010", "00011", "00012", "00020", "00021", "00022", "00100", "00101",
                    "00102", "00110", "00111", "00112", "00120", "00121", "00122", "00200", "00201", "00202", "00210",
                    "00211", "00212", "00220", "00221", "00222", "01000", "01001", "01002", "01010", "01011", "01012",
                    "01020", "01021", "01022", "01100", "01101", "01102", "01110", "01111", "01112", "01120", "01121",
                    "01122", "01200", "01201", "01202", "01210", "01211", "01212", "01220", "01221", "01222", "02000",
                    "02001", "02002", "02010", "02011", "02012", "02020", "02021", "02022", "02100", "02101", "02102",
                    "02110", "02111", "02112", "02120", "02121", "02122", "02200", "02201", "02202", "02210", "02211",
                    "02212", "02220", "02221", "02222", "10000", "10001", "10002", "10010", "10011", "10012", "10020",
                    "10021", "10022", "10100", "10101", "10102", "10110", "10111", "10112", "10120", "10121", "10122",
                    "10200", "10201", "10202", "10210", "10211", "10212", "10220", "10221", "10222", "11000", "11001",
                    "11002", "11010", "11011", "11012", "11020", "11021", "11022", "11100", "11101", "11102", "11110",
                    "11111", "11112", "11120", "11121", "11122", "11200", "11201", "11202", "11210", "11211", "11212",
                    "11220", "11221", "11222", "12000", "12001", "12002", "12010", "12011", "12012", "12020", "12021",
                    "12022", "12100", "12101", "12102", "12110", "12111", "12112", "12120", "12121", "12122", "12200",
                    "12201", "12202", "12210", "12211", "12212", "12220", "12221", "12222", "20000", "20001", "20002",
                    "20010", "20011", "20012", "20020", "20021", "20022", "20100", "20101", "20102", "20110", "20111",
                    "20112", "20120", "20121", "20122", "20200", "20201", "20202", "20210", "20211", "20212", "20220",
                    "20221", "20222", "21000", "21001", "21002", "21010", "21011", "21012", "21020", "21021", "21022",
                    "21100", "21101", "21102", "21110", "21111", "21112", "21120", "21121", "21122", "21200", "21201",
                    "21202", "21210", "21211", "21212", "21220", "21221", "21222", "22000", "22001", "22002", "22010",
                    "22011", "22012", "22020", "22021", "22022", "22100", "22101", "22102", "22110", "22111", "22112",
                    "22120", "22121", "22122", "22200", "22201", "22202", "22210", "22211", "22212", "22220", "22221",
                    "22222"]
    finalScore = 0

    for c in combinations:
        entrada = [int(i) for i in c]
        pattern = generatePattern(entrada, word)
        p = 0
        for i in d.keys(): p += 1 if re.match(pattern, i) else 0
        p /= len(d)
        finalScore += p * math.log(p, 2) if p > 0 else 0
    # print(f"{word}:{finalScore}")
    return finalScore


def paralelDict(item, d):
    return {i: scoreWord(i, d) for i in item}


def updateDict(d, pattern):
    d = {k: 0 for (k, v) in d.items() if re.match(pattern, k)}

    n = os.cpu_count()
    chunkSize = math.ceil(len(d) / n)
    out = {}
    with ProcessPoolExecutor(n) as executor:
        futures = [executor.submit(paralelDict, list(d.keys())[chunkSize * i:chunkSize * (i + 1)], d) for i in range(n)]
        for future in concurrent.futures.as_completed(futures):
            out.update(future.result())
        executor.shutdown()
    return out


def validarEntrada(entrada, word, globalPattern):
    procesed = {}
    for i in range(len(entrada)):
        letra = word[i]
        if letra not in procesed:
            if entrada[i] == 0:
                if (f"(?=.{{{i}}}{letra})" in globalPattern) or (f"(?=.*{letra})" in globalPattern and not max(
                        [entrada[j] == 2 and word[j] == letra for j in range(i + 1, len(entrada))] + [False])) or max([entrada[j] == 1 and word[j] == letra for j in range(i + 1, len(entrada))] + [False]):
                    print(f"Error en 0 letra {letra}")
                    return False
            elif entrada[i] == 1:
                if f"(?=.{{{i}}}{letra})" in globalPattern:
                    return False
            elif entrada[i] == 2:
                if f"(?!.{{{i}}}{letra})" in globalPattern or f"(?=[^{letra}]*$)" in globalPattern:
                    print(f"Error en 2 letra {letra}")
                    return False
            procesed[letra] = 0
    return True

if __name__ == '__main__':
  graph = GraphvizOutput()
  graph.output_file = "file3.png"

  with PyCallGraph(output=graph):
    intentos = 6
    d = json.loads(requests.get("https://media.githubusercontent.com/media/cardstdani/practica-java/main/Data/DictScoreData.txt").text)
    globalPattern = ""
    for intento in range(intentos):
        print(len(d), d, len(d))
        word = max(d, key=d.get)
        print(word, d[word])

        entrada = procesarEntrada()
        pattern = generatePattern(entrada, word)
        if validarEntrada(entrada, word, globalPattern):
            globalPattern += pattern[1:-3]
            try:
              d=json.loads(requests.get(f"https://media.githubusercontent.com/media/cardstdani/practica-java/main/Data/MaxTree/Dict{intento+1}-{''.join([str(a) for a in entrada])}.txt").text)
            except:
              d = updateDict(d, pattern)
        else:
            print("Error detectado, entrada inconsistente")
            intento -= 1
        if entrada == [2, 2, 2, 2, 2]:
            break