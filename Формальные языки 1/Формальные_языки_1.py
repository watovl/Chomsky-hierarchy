import sys
import re

# неограниченная грамматика
def unlimited(rules, dataSymbols):
    for rule in rules:
        # если слева нету нетерминала, то возвращаем false
        if re.search("["+dataSymbols["nonterminal"]+"]", rule[0]) == None:
            return False
    return True

# контекстно-зависимая грамматика
def contextSensitive(rules, dataSymbols):
    for rule in rules:
        for i in range(len(rule) - 1):
            # левая часть больше правой
            if len(rule[0]) > len(rule[i + 1]):
                return False
    return True

# контекстно-свободная грамматика
def contextFree(rules, dataSymbols):
    for rule in rules:
        # нету только нетерминала слева
        if re.match("^["+dataSymbols["nonterminal"]+"]$", rule[0]) == None:
            return False
    return True

# регулярная грамматика
def regular(rules, dataSymbols):
    rightRegular = 1
    for rule in rules:
        if re.match("^["+dataSymbols["nonterminal"]+"]$", rule[0]) == None:
           return False
        else:
            for i in range(len(rule) - 1):
                # не леволинейная и была праволинейной
                if re.match("^["+dataSymbols["nonterminal"]+"]?["+dataSymbols["terminal"]+"]+$", rule[i+1]) == None or rightRegular == 2:
                    # не праволинейная и была леволинейной
                    if re.match("^["+dataSymbols["terminal"]+"]+["+dataSymbols["nonterminal"]+"]?$", rule[i+1]) == None or rightRegular == 0:
                        return False
                    # праволинейная
                    else:
                        rightRegular = 2
                # леволинейная
                else:
                    rightRegular = 0
    return True


print("Классификация Хомского для грамматики G = (T, N, P, S)")
print("Символ 'e' зарезервирован для пустого символа!")
dataSymbols = {}
dataSymbols["terminal"] = re.sub(r"(\[\[\]\\\/\^\$\.\|\?\*\+\(\)\{\}])", r"\\\1", input("Введите терминальные символы T: ").replace(" ", "")) + "e"
dataSymbols["nonterminal"] = input("Введите нетерминальные символы N: ").replace(" ", "")
dataSymbols["alphabet"] = dataSymbols["nonterminal"] + dataSymbols["terminal"]

count = int(input("Введите количество правил: "))
print("Знак следует обозначается '->', знак или '|'")
productionRules = []

pattern = "^[" + dataSymbols["alphabet"] + "]+ *-> *" + "(?:[" + dataSymbols["alphabet"] + "]+)(?:(?: *\| *)(?:[" + dataSymbols["alphabet"] + "]+))*$"
for i in range(count):
    inputString = input("Введите правило номер " + str(i + 1) +": ")
    # проверка корректности ввода
    if re.match(pattern, inputString):
        productionRules.append(re.split(r" *-> *| *\| *", inputString))
    else:
        print("Правило введено не верно!")
        sys.exit()

dataSymbols["start symbol"] = input("Введите начальный символ: ")

# сравнение первого символа первого правила с начальным символом
if productionRules[0][0] == dataSymbols["start symbol"]:
    # проверка на тип 0
    if unlimited(productionRules, dataSymbols):
        typeChomsky = 0
        # проверка на тип 3 - регулярность
        if regular(productionRules, dataSymbols):
            typeChomsky = 3
        # если не регулярная, проверяем на тип 2 - КС
        elif contextFree(productionRules, dataSymbols):
            typeChomsky = 2
        # если не КС, проверяем на тип 1 - КЗ
        elif contextSensitive(productionRules, dataSymbols):
            typeChomsky = 1
    else:
        print("Грамматика не подходит ни под один тип!")
        sys.exit()
else:
    print("Первый символ не соответствует начальному!")
    sys.exit()


typesChomsky = {
    0 : "тип 0 - неограниченная",
    1 : "тип 1 - контекстно-зависимая",
    2 : "тип 2 - контекстно-свободная",
    3 : "тип 3 - регулярная"
    }

print("\n\tДанная грамматика имеет " + typesChomsky[typeChomsky] + "\n")
