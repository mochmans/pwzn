import os
import sys
import argparse
import pathlib
from numpy import append
import tqdm # type: ignore
from collections import defaultdict
from ascii_graph import Pyasciigraph # type: ignore
from ascii_graph import colors # type: ignore

parser = argparse.ArgumentParser(description='Histogram creator')
parser.add_argument('-f', '--filename', help='Filename to process', default = '___noFile___')
parser.add_argument('-H','--hentries',help='Histogram entries',type=int, default=5)
parser.add_argument('-l', '--limit', help='Length limit', type=int, default=0)
parser.add_argument('-I', '--ilist', help='Ignored words', nargs='*')
parser.add_argument('-W', '--wlist', help='Whitelisted strings', nargs='*')
parser.add_argument('-B','--blist',help='Blacklisted strings',nargs='*')
parser.add_argument('-D','--directory',help='Directory path',type=str , default=None)

args = parser.parse_args()

wordDict = defaultdict(int)
fileList = []

if args.directory != None:
    for root, dirs, files in os.walk(args.directory):
        for name in files:
            if name.endswith((".txt")):
                print(os.path.abspath(name))
                fileList.append(os.path.abspath(name))


def checkWhitelist(wlist,word):
    for wrd in wlist:
        if word.count(wrd) == 0:
            return False 

def checkBlacklist(blist,word):
    for wrd in blist:
        if word.count(wrd) > 0:
            return False 

def checkIgnorelist(ilist,word):
    for wrd in ilist:
        if word == wrd:
            return False

if args.filename != '___noFile___':
    with open(args.filename, 'r', encoding='utf8') as file:
        num_lines = sum(1 for _ in file)
        pbar = tqdm.tqdm(total=num_lines)
        file.seek(0)
        for line in file:
            pbar.update(1)
            for word in line.split():
                check = [True]
                if len(word) >= args.limit:
                    if args.wlist != None:
                        check.append(checkWhitelist(args.wlist,word))
                    if args.blist != None:
                        check.append(checkBlacklist(args.blist,word))
                    if args.ilist != None:
                        check.append(checkIgnorelist(args.ilist,word))
                else:
                    check = [False]
                if check.count(False) == 0:
                    wordDict[word] +=1
                    # if not word in wordDict:
                    #     wordDict.update({word : 1})
                    # else:
                    #     wordDict.update({word:wordDict.get(word)+1})

if args.directory != None:
    for filename in fileList:
        with open(filename, 'r', encoding='utf8') as file:
            num_lines = sum(1 for _ in file)
            pbar = tqdm.tqdm(total=num_lines)
            file.seek(0)
            for line in file:
                pbar.update(1)
                for word in line.split():
                    check = [True]
                    if len(word) >= args.limit:
                        if args.wlist != None:
                            check.append(checkWhitelist(args.wlist,word))
                        if args.blist != None:
                            check.append(checkBlacklist(args.blist,word))
                        if args.ilist != None:
                            check.append(checkIgnorelist(args.ilist,word))
                    else:
                        check = [False]
                    if check.count(False) == 0:
                        wordDict[word] +=1
       
if args.directory != None or args.filename != '___noFile___':

    colorsList = [colors.Blu, colors.Red, colors.Gre, colors.Yel, colors.Pur, colors.Cya, colors.Whi, colors.Bla]

    data =[]
    for x, y in wordDict.items():
            data.append((y,x))
    data.sort()
    sortedData = []

    if args.hentries > 20:
        args.hentries = 20

    for i in range(args.hentries):
        value, word = data[len(data)-1-i]
        sortInsert = (word, value, colorsList[i % 8])
        sortedData.append(sortInsert)

    graph = Pyasciigraph()

    for line in graph.graph('Word histogram', sortedData):
        print(line)


