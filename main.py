import math
import os

THE_BEGINNING_OF_THE_WORD = "  "
THE_LETTER_OF_THE_WORD = "##"
MAX_ROW_TABLE = 5
WIDTH = 100


def getScore(frequencyAB, frequencyA, frequencyB) -> float:
    return round(frequencyAB / (frequencyA * frequencyB), 4)


def divisionWordIntoSymbols(word) -> list:
    global THE_BEGINNING_OF_THE_WORD, THE_LETTER_OF_THE_WORD
    return [
        f'{THE_LETTER_OF_THE_WORD}{symbol}' if idx != 0 else f'{THE_BEGINNING_OF_THE_WORD}{symbol}'
        for idx, symbol in enumerate(list(word))
    ]


def normalizeListWords(listWords) -> list:
    return [word.upper().strip() for word in listWords]


def convertListWordsToListSymbols(listWords) -> list:
    ListSymbols = []
    for word in listWords:
        [ListSymbols.append(symbol) for symbol in word]
    return ListSymbols


def wordPeace__start(dictionary, listCases):
    global THE_BEGINNING_OF_THE_WORD
    results = []
    allWordString = "".join(listCases)
    # Is dictionary is empty
    if len(dictionary) == 0:
        dictionary = list(set(listCases))
    # let's go through the pairs of buildings (tokens)
    for tokenNumber in range(len(listCases) - 1):
        # getting  tokens
        tokenA = listCases[tokenNumber]
        tokenB = listCases[tokenNumber + 1]
        tokenAB = tokenA + tokenB
        # we check whether token B is the beginning of the word
        if THE_BEGINNING_OF_THE_WORD in tokenB:
            # skip a pair of tokens
            continue
        # counting points
        freqA = listCases.count(tokenA)
        freqB = listCases.count(tokenB)
        freqAB = allWordString.count(tokenAB)
        results.append({
            'tokenA': tokenA,
            'tokenB': tokenB,
            'tokenAB': tokenAB,
            'resultToken': f'{tokenA}{tokenB.replace(THE_LETTER_OF_THE_WORD, "")}',
            'score': getScore(frequencyAB=freqAB, frequencyA=freqA, frequencyB=freqB)
        })
    # we are looking for a candidate to unite
    maxResult = max(results, key=lambda result: result['score'])
    # adding a new token to the dictionary
    dictionary.append(maxResult['resultToken'])
    # changing the list of buildings
    newListCases = []
    flag = False
    for tokenNumber in range(len(listCases) - 1):
        # if the letter is involved in the union, then do not add it to the list
        if flag:
            flag = False
            continue
        # getting  tokens
        tokenA = listCases[tokenNumber]
        tokenB = listCases[tokenNumber + 1]
        # if this is a candidate for unification
        if tokenA == maxResult['tokenA'] and tokenB == maxResult['tokenB']:
            # adding a new token to the list of enclosures
            newListCases.append(maxResult['resultToken'])
            # we say that the next element should not be added
            flag = True
        else:
            # adding the unmodified token to the list of enclosures
            newListCases.append(tokenA)

    return dictionary, newListCases, maxResult, results


def printTable(dictionary):
    global MAX_ROW_TABLE, WIDTH
    result = ""
    if len(dictionary) > MAX_ROW_TABLE:
        table = []
        countColumn = int(math.ceil(len(dictionary) / MAX_ROW_TABLE))
        maxCountElementsTable = MAX_ROW_TABLE * countColumn
        maxLen = len(max(dictionary, key=len))
        for numberWord in range(len(dictionary)):
            if len(dictionary[numberWord]) != maxLen:
                dictionary[numberWord] += ' ' * (maxLen - len(dictionary[numberWord]))
        if maxCountElementsTable != len(dictionary):
            for i in range(maxCountElementsTable - len(dictionary)):
                dictionary.append(' ' * maxLen)
        for column in range(countColumn):
            table.append(dictionary[column * MAX_ROW_TABLE:column * MAX_ROW_TABLE + MAX_ROW_TABLE])
        for row in range(MAX_ROW_TABLE):
            text = ""
            for column in range(countColumn):
                if column != 0:
                    text += " | "
                text += table[column][row]
            text = printMessages(text=text)
            result += text if '\n' in text else text + '\n'
            result += '= ' + "-" * (WIDTH - 4) + ' =\n'
    else:

        for idx, word in enumerate(dictionary):
            text = printMessages(f"{idx + 1}) {word}", 'left')
            result += text if '\n' in text else text + '\n'
    return result


def printMessages(text, align='center'):
    global WIDTH
    result = ""
    widthText = WIDTH - 4
    align = align.strip().lower()
    if align == 'center':
        if len(text) > widthText:
            countIteration = len(text) / widthText
            countIteration = math.ceil(countIteration)
            countIteration = int(countIteration)
            for i in range(countIteration):
                textLine = text[i * widthText:i * widthText + widthText]
                if len(textLine) != widthText:
                    countSpace = (widthText - len(textLine))
                    if countSpace % 2 == 0:
                        countSpace = int(countSpace / 2)
                        textLine = ' ' * countSpace + textLine + ' ' * countSpace
                    else:
                        countSpace = int((countSpace - 1) / 2)
                        textLine = ' ' * countSpace + textLine + ' ' + ' ' * countSpace

                result += f"= {textLine} =\n"
        else:
            countSpace = (widthText - len(text))
            if countSpace % 2 == 0:
                countSpace = int(countSpace / 2)
                textLine = ' ' * countSpace + text + ' ' * countSpace
            else:
                countSpace = int((countSpace - 1) / 2)
                textLine = ' ' * countSpace + text + ' ' + ' ' * countSpace
            result += f"= {textLine} ="
    elif align == 'left':
        if len(text) > widthText:
            countIteration = len(text) / widthText
            countIteration = math.ceil(countIteration)
            countIteration = int(countIteration)
            for i in range(countIteration):
                textLine = text[i * widthText:i * widthText + widthText]
                if len(textLine) != widthText:
                    textLine += ' ' * (widthText - len(textLine))
                result += f"= {textLine} =\n"
        else:
            result += f"= {text}{' ' * (widthText - len(text))} ="
    else:
        result = text
    return result


def main():
    global WIDTH, THE_BEGINNING_OF_THE_WORD
    listWords = [
        'ЗАРОСЛИ',
        'МОРЖ',
        'МОРОЖЕННОЕ',
        'ЛЕСОПОВАЛ',
        'ЛЕС',
        'ЛЕДОХОД',
        'ГОРЕЦ',
        'ГОРА',
        'МОРОЗЫ',
        'РОЗА',
    ]
    # listWords = [
    #     'huggingface',
    #     'hugging',
    #     'face',
    #     'hug',
    #     'hugger',
    #     'learning',
    #     'learner',
    #     'learners',
    #     'learn',
    # ]

    dictionary = []
    os.system('cls')
    print("=" * WIDTH)
    print(printMessages(f"Word Peace token generation"))
    print(printMessages(f"By Skrebnev Leonid FITU 4-5Б"))
    print("=" * WIDTH)

    newListWords = input("new list words(yes or no)?: ")
    if 'yes' in newListWords or 'y' in newListWords:
        newListWords = []
        while True:
            newWord = input("Enter word(q - stop typing): ")
            if 'q' in newWord:
                if len(newListWords) != 0:
                    listWords = newListWords
                break
            newListWords.append(newWord)
    listWords = normalizeListWords(listWords=listWords)
    listCases = [divisionWordIntoSymbols(word) for word in listWords]
    listCases = convertListWordsToListSymbols(listWords=listCases)
    print("=" * WIDTH)
    print(printMessages(f"list words"))
    print("=" * WIDTH)
    print(printTable(listWords))
    print("=" * WIDTH)

    showCalculations = input("show calculations(yes or no)?: ")
    pauseInIteration = input("should I ask for a message at each iteration(yes or no)?: ")
    try:
        countIteration = int(input("How iteration?: "))
    except Exception as e:
        countIteration = 2
        print("=" * WIDTH)
        print(printMessages(f"an error occurred while entering iterations so the default value was set {countIteration}",
                         'left'))
        print("=" * WIDTH)
    for iterationNumber in range(1, countIteration + 1):
        if iterationNumber != 1 and not ('no' in pauseInIteration or 'n' in pauseInIteration):
            print("=" * WIDTH)
            print(printMessages(f"Word Peace token generation"))
            print(printMessages(f"By Skrebnev Leonid FITU 4-5Б"))
            print("=" * WIDTH)
        dictionary, listCases, result, resultsIteration = wordPeace__start(dictionary=dictionary, listCases=listCases)
        dictionary = [val if len(val.strip()) > 0 else None for val in list(set(dictionary))]
        if None in dictionary:
            dictionary.pop(dictionary.index(None))
        print("=" * WIDTH)
        print(printMessages(f"iteration #{iterationNumber}"))
        print("=" * WIDTH)
        print(printMessages(f"the found token: {result['resultToken']}", 'left'))
        print(printMessages(f"with the score: {result['score']}", 'left'))
        print("=" * WIDTH)
        print(printMessages("dictionary"))
        print("=" * WIDTH)
        print(printTable(dictionary))
        print("=" * WIDTH)
        print(printMessages("cases"))
        print("=" * WIDTH)
        cases = ' '.join(listCases).split(THE_BEGINNING_OF_THE_WORD)
        print(printTable(cases))
        print("=" * WIDTH)
        if 'yes' in showCalculations or 'y' in showCalculations:
            resultsIteration.sort(key=lambda value: value['score'], reverse=True)
            for idx, resultIteration in enumerate(resultsIteration):
                print(printMessages(f"{idx + 1}) {resultIteration['tokenAB']} - {resultIteration['score']}", 'left'))
                if (idx + 1) % MAX_ROW_TABLE == 0:
                    print(printMessages("", 'left'))
            print("=" * WIDTH)
        if not ('no' in pauseInIteration or 'n' in pauseInIteration):
            key = str(input("to continue, press any button or press 'no' to exit: ")).strip().lower()
            if 'no' in key or 'n' in key:
                break
            os.system('cls')


if __name__ == '__main__':
    main()
