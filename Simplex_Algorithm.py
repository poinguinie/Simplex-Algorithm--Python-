import re

INFINITY = 10000000


class SimplexAlgorithm:

    def __init__(self):
        self.mode = ""
        self.modeConditionStr = None
        self.modeCondition = []
        self.condition = []
        self.artificial = []
        self.matrix = []
        self.ratio = []
        self.pivot = 0
        self.surplusVarIndex = 0
        self.result = []

    def inputFromUser(self):
        # 상수와 변수의 곱에서 * 연산은 생략 합니다. 또한 상수와 변수를 붙혀 입력해 주세요.
        # 예) 2 * x1 (X) , 2x1 (O)
        # 입력 값 중 상수가 0인 경우도 0으로 표기해 주세요.
        # 예) x1 + 0x2 <= 3
        self.mode = input("입력 모드를 설정해 주세요: (최대: max, 최소: min): ")
        self.modeConditionStr = input("구하고자 하는 최대 값을 적어 주세요: ")
        self.modeCondition = self.getCondition(self.modeConditionStr)
        self.result = [0 for _ in range(len(self.modeCondition))]

        while True:
            cond = input("조건 식들을 적어 주세요: (-1 입력시 조건식 입력 종료)\n")
            if cond == "-1":
                break
            self.condition.append(self.getCondition(cond))

        self.initMatrix()

    def initCondition(self, mode, modeCondition, conditions):
        self.mode = mode
        self.modeConditionStr = modeCondition
        self.modeCondition = self.getCondition(modeCondition)

        self.result = [0 for _ in range(len(self.modeCondition))]
        for condition in conditions:
            self.condition.append(self.getCondition(condition))

        self.initMatrix()

    def initMatrix(self):
        self.artificial = [0 for _ in range(len(self.condition))]

        self.makeMatrix()
        self.makeRatio()

    def clearData(self):
        self.modeConditionStr = None
        self.modeCondition = []
        self.condition = []
        self.matrix = []
        self.ratio = []
        self.pivot = 0
        self.result = []

    def getCondition(self, condition):
        if "<=" in condition:
            mode = -1
        elif ">=" in condition:
            mode = 1
        elif "=" in condition:
            mode = 0
        else:
            mode = -10
        condition = condition.replace('*', '+').replace('/', '+').replace('<=', '+').replace('>=', '+').replace('=',
                                                                                                                '+')
        operand = condition.strip().split('+')
        operand = list(map(self.conditionReplace, operand))

        operand.append(mode)

        return operand

    def conditionReplace(self, item):
        item = item.strip()
        item = re.sub('[x-z]+[0-9]+', "", item)
        if item == '':
            item = 1
        elif item == '-':
            item = -1

        return float(item)

    def makeMatrix(self):
        for r in range(0, len(self.condition)):
            row = []
            for c in range(0, len(self.modeCondition) - 1):
                row.append(self.condition[r][c])
            # surplusVar: 잉여 변수
            surplusVar = [0 for _ in range(len(self.condition))]
            # artificialVar: 인위 변수
            artificialVar = [0 for _ in range(len(self.condition))]
            if self.condition[r][-1] == -1:
                # <=
                surplusVar[r] = 1
                self.artificial[r] = 0
            elif self.condition[r][-1] == 0:
                # =
                artificialVar[r] = 1
                self.artificial[r] = (-1) * INFINITY
            elif self.condition[r][-1] == 1:
                # >=
                surplusVar[r] = -1
                artificialVar[r] = 1
                self.artificial[r] = (-1) * INFINITY
            row += surplusVar
            row += artificialVar
            row.append(self.condition[r][-2])

            self.matrix.append(row)

        m = self.modeCondition[0:-1]
        c = list(map(lambda x: x * -1, m))
        # append surplusVar in matrix
        c += [0 for _ in range(len(self.condition))]
        # append artificialVar in matrix
        c += self.artificial
        c.append(0)

        self.matrix.append(c)

        z = [0 for _ in range(len(self.matrix[0]))]
        t = [0 for _ in range(len(self.matrix[0]))]

        self.matrix.append(z)
        self.matrix.append(t)

        self.calcZ()
        self.matrix[-1] = self.calcCMinusZ()

    def hasNegative(self):
        for i in range(len(self.matrix[-1]) - 1):
            if self.matrix[-1][i] < 0:
                return True

        return False

    def hasPositive(self):
        for i in range(len(self.matrix[-1]) - 1):
            if self.matrix[-1][i] > 0:
                return True

        return False

    def findPivot(self):
        temp = [self.matrix[-1][i] for i in range(len(self.modeCondition) - 1)]
        temp = list(map(lambda x: abs(x), temp))
        return temp.index(max(temp))

    def makeRatio(self):
        r = []
        for row in range(0, len(self.condition)):
            r.append(self.matrix[row][-1] / self.matrix[row][self.pivot])

        r.append(self.matrix[-1][-1] / self.matrix[-1][self.pivot])
        self.ratio = r

    def findMinIndex(self):
        index = 0
        minimum = self.ratio[0]
        for i in range(0, len(self.ratio) - 1):
            if self.ratio[i] < 0:
                continue
            if minimum > self.ratio[i]:
                index = i
                minimum = self.ratio[i]

        return index

    def makeElementMatrix(self, pivot):
        p = float(self.matrix[pivot][self.pivot])

        if p != 1:
            for i in range(0, len(self.matrix[pivot])):
                self.matrix[pivot][i] = self.matrix[pivot][i] * (1 / p)

        p = self.matrix[pivot][self.pivot]

        for r in range(0, len(self.condition)):
            if r == pivot:
                continue
            b = (self.matrix[r][self.pivot] / p) * (-1)
            for c in range(0, len(self.matrix[r])):
                self.matrix[r][c] = self.matrix[r][c] + (self.matrix[pivot][c] * b)

        b = (self.matrix[-1][self.pivot] / p) * (-1)
        for c in range(0, len(self.matrix[-1])):
            self.matrix[-1][c] = self.matrix[-1][c] + (self.matrix[pivot][c] * b)

    def calcZ(self):
        z = [0 for _ in range(len(self.matrix[0]))]
        for r in range(0, len(self.condition)):
            for c in range(0, len(z)):
                z[c] += self.artificial[r] * self.matrix[r][c]

        self.matrix[-2] = z

    def calcCMinusZ(self):
        t = [0 for _ in range(len(self.matrix[-1]))]
        for i in range(0, len(t)):
            t[i] = self.matrix[-3][i] - self.matrix[-2][i]
        return t

    def setArtificial(self, pivotRowIndex):
        if pivotRowIndex != -1:
            self.artificial[pivotRowIndex] = self.matrix[-3][self.pivot]

        if self.matrix[-1][0] == 0.0 and self.matrix[-1][1] == 0.0:
            self.artificial = list(map(lambda x: 0 if x == INFINITY else x, self.artificial))

    def setResult(self):
        self.result[0] = self.matrix[-1][-1]
        for r in range(0, len(self.matrix)):
            for c in range(0, len(self.modeCondition) - 1):
                if self.matrix[r][c] == 1.0:
                    self.result[c + 1] = self.matrix[r][-1]

    def printResult(self):
        if self.mode == "max":
            print('{0}의 최대값: {1:0.3f}'.format(self.modeConditionStr, self.result[0]))
        elif self.mode == "min":
            print('{0}의 최소값: {1:0.3f}'.format(self.modeConditionStr, self.result[0]))

        for i in range(0, len(self.result) - 1):
            print('이때의 x{0} 값: {1:0.3f}'.format(i + 1, self.result[i + 1]))

    def findOptical(self):
        for i in range(len(self.modeCondition) - 1, len(self.condition)):
            if self.matrix[-1][i] > 0:
                return i

        return 0

    def simplex_algorithm(self):
        if self.matrix[-1][0] != 0.0 or self.matrix[-1][1] != 0.0:
            self.pivot = self.findPivot()
            self.makeRatio()
            pivotRowIndex = self.findMinIndex()
            self.setArtificial(pivotRowIndex)
        else:
            self.pivot = (len(self.modeCondition) - 1) + self.findOptical()
            self.makeRatio()
            self.setArtificial(-1)
            pivotRowIndex = self.artificial.index(INFINITY * -1)

        self.makeElementMatrix(pivotRowIndex)
        self.calcZ()
        self.calcCMinusZ()

    def run(self):
        # self.inputFromUser()
        if self.mode == "max":
            while self.hasNegative():
                self.simplex_algorithm()
        elif self.mode == "min":
            while self.hasPositive():
                self.simplex_algorithm()

        self.setResult()
        self.printResult()


# s = SimplexAlgorithm()
# s.run()
