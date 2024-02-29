
with open("words_alpha.txt") as f:
    allWords = {line.strip() for line in f}

toRemove = set()
for w in allWords:
    if len(w) != 5: toRemove.add(w)
allWords -= toRemove

words = {a for a in allWords} 

def getGoal ():  
    goal = " "
    while goal not in allWords and goal != "":
        goal = input("Word to search for (leave blank if unknown): ")
        if goal not in allWords and goal != "":
            rank = {w:0 for w in allWords}
            for w in allWords:
                for i in range(0, len(goal)):
                    if i < len(w) and goal[i] == w[i]: rank[w] += 2
                    elif goal[i] in w: rank[w] += 1
                rank[w] -= len(w) - len(goal)
            rank = sorted(rank.items(), key=lambda x : x[1], reverse=True)
            inp = input("Did you mean " + str(list(zip(map(lambda x : x[0], rank[:5]), range(0, 5)))) + "? (Give the number if so, blank if not): ")
            goal = rank[int(inp)][0] if int(inp) in range(0, 5) else " "
    return goal

def generatePos (word, goal):
    pos = ""
    for i in range(0, len(word)):
        if i < len(goal) and word[i] == goal[i]: pos += '='
        elif word[i] in goal: pos += '+'
        else: pos += '-'
    return pos

def pruneWords(guess):
    toRemove = set()
    for i in range(0, len(guess)):
        [c,p] = guess[i]
        for w in words:
            if p == '+' and (c not in w or (i < len(w) and c == w[i])): toRemove.add(w)
            elif p == '-' and c in w: toRemove.add(w)
            elif p == '=' and (i >= len(w) or c != w[i]): toRemove.add(w)
    for i in toRemove:
        words.remove(i)

def letterFreq():
    count = {(chr(i),p) : 0 for i in range(ord('a'), ord('z')+1) for p in range(0, 5)}
    for (c,p) in count.keys():
        for w in words:
            count[(c, p)] += 1 if p < len(w) and c == w[p] else 0
    return sorted(count.items(), key = lambda x : x[1], reverse = True)

def findNextWord(count):
    if len(words) == 1: return [(list(words)[0], 0)]

    rank = {c : 10 if c in words else 0 for c in allWords}
    for w in allWords:
        for ((c, p), v) in count:
            if p < len(w) and c == w[p]: rank[w] += 1.5*v
            elif c in w: rank[w] += v
    return sorted(rank.items(), key = lambda x : x[1], reverse = True)[:5]

word = ""
pos = " "
attempt = 0
goal = getGoal()
if goal != "":
    print("Looking for '" + goal + "'")

while pos != len(goal)*'=' and pos != "DONE":
    attempt += 1

    print(100*'-')

    freq = letterFreq()
    bestGuess = findNextWord(freq)

    if len(words) < 50 : print("Possible words left:    " + str(words))
    print ("#Possible words left: " + str(len(words)))
    print ("Five best guesses: " + str(bestGuess))

    word = " "
    while word not in allWords or word == "":
        word = input("Tried word:   ") if word != "" else bestGuess[0][0]

    pos = input("Result (Blank = '-', Orange = '+', Green = '=', Finished = 'DONE'):   ") if goal == "" else generatePos(word, goal)

    print ("Result: " + str((word, pos)))

    pruneWords(list(zip(word, pos)))

print("\nWord '{0}' found in {1} attempts".format(goal, attempt))
input("\nPress Enter to continue...")