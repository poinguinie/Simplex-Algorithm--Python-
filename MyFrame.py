import tkinter as tk
from pandas import DataFrame
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Simplex_Algorithm import SimplexAlgorithm


class MyFrame:
    def __init__(self):
        self.ax = None
        self.line = None
        self.figure = None
        self.x = None
        self.axis = []
        self.modeCondition = None
        self.conditionListIndex = 0
        self.mode = "max"
        '''
            인터페이스 구현
        '''
        # 윈도우 살정
        self.window = tk.Tk()
        self.window.title("Simplex 알고리즘 구현")
        self.window.geometry("960x600+200+200")
        self.window.resizable(False, False)

        # 데이터 프레임 설정
        self.dataFrame = tk.Frame(self.window, bd=2)
        self.dataFrame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.modeBtn = tk.Button(self.dataFrame, text="모드 변경 (현재 최대)", command=self.modeSwitch)
        self.modeBtn.pack(side="top", fill="x", expand=False, ipady=5)

        # 데이터 프레임 안 속성 프레임 설정
        self.inputFrame = tk.Frame(self.dataFrame, relief="solid", bd=1, height=100)
        self.outputFrame = tk.Frame(self.dataFrame, relief="solid", bd=1, height=400)
        self.resultFrame = tk.Frame(self.dataFrame, relief="solid", bd=2, height=300)
        self.optionFrame = tk.Frame(self.dataFrame, relief="solid", bd=1, height=50)

        self.inputFrame.pack(side="top", fill="both", expand=False, padx=10, pady=10)
        self.outputFrame.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        self.resultFrame.pack(side="top", fill="both", expand=False, padx=10, pady=10)
        self.optionFrame.pack(side="bottom", fill="both", expand=False, padx=10, pady=10)
        self.optionFrame.propagate(0)

        # 입력 프레임 안 위젯 설정
        self.inputModeCondition = tk.Entry(self.inputFrame)
        self.setModeConditionBtn = tk.Button(self.inputFrame, text="최대 조건 입력", command=self.clickModeConditionBtn)
        self.inputCondition = tk.Entry(self.inputFrame)
        self.setConditionBtn = tk.Button(self.inputFrame, text="조건 입력", command=self.clickConditionBtn)

        self.inputModeCondition.pack(side="top", fill="x", padx=5, pady=5)
        self.setModeConditionBtn.pack(side="top", fill="x", padx=5, pady=5)
        self.inputCondition.pack(side="top", fill="x", padx=5, pady=5)
        self.setConditionBtn.pack(side="top", fill="x", padx=5, pady=5)

        # 출력 프레임 안 위젯 설정 (리스트 박스)
        self.modeConditionLabel = tk.Label(self.outputFrame, text="최대 조건")
        self.modeConditionListBox = tk.Listbox(self.outputFrame, height=0)
        self.conditionLabel = tk.Label(self.outputFrame, text="조건 리스트 박스")
        self.conditionListBox = tk.Listbox(self.outputFrame, height=0)

        self.modeConditionLabel.pack(side="top", fill="x", padx=5)
        self.modeConditionListBox.pack(side="top", fill="x", padx=5)
        self.conditionLabel.pack(side="top", fill="x", padx=5)
        self.conditionListBox.pack(side="top", fill="x", padx=5)

        # 결과 프레임 안 위젯 설정
        self.resultLabelTitle = tk.Label(self.resultFrame, text="결과값")
        self.resultLabelContent = tk.Label(self.resultFrame, text="\n\n\n\n")

        self.resultLabelTitle.pack(side="top", fill="x", padx=5, pady=3)
        self.resultLabelContent.pack(side="top", fill="both")

        # 설정 프레임 안 위젯 설정
        self.startBtn = tk.Button(self.optionFrame, text="Simplex Algorithm 구현", command=self.simplexAlgorithm)
        self.clearBtn = tk.Button(self.optionFrame, text="다시 하기", command=self.clearData)
        self.startBtn.pack(side="left", padx=20)
        self.clearBtn.pack(side="right", padx=20)

        '''
            그래프 설정
        '''
        self.initGraph()

        '''
            Simplex 알고리즘 초기화
        '''
        self.sa = SimplexAlgorithm()

    '''
        버튼 클릭 이벤트 메서드
    '''
    def modeSwitch(self):
        if self.mode == "max":
            self.mode = "min"
            self.modeBtn.config(text="모드 변경 (현재 최소)")
            self.modeConditionLabel.config(text="최소 조건")
            self.setModeConditionBtn.config(text="최소 조건 입력")
        else:
            self.mode = "max"
            self.modeBtn.config(text="모드 변경 (현재 최대)")
            self.modeConditionLabel.config(text="최대 조건")
            self.setModeConditionBtn.config(text="최대 조건 입력")

    def clickModeConditionBtn(self):
        if self.inputModeCondition.get() == "":
            return
        self.modeConditionListBox.insert(0, self.inputModeCondition.get())
        self.clearEntry(self.inputModeCondition)

    def clickConditionBtn(self):
        if self.inputCondition.get() == "":
            return

        input = self.inputCondition.get()
        self.conditionListBox.insert(self.conditionListIndex, input)
        self.drawGraph(input)
        self.conditionListIndex += 1
        self.clearEntry(self.inputCondition)

    def clearEntry(self, entry):
        entry.delete(0, len(entry.get()))

    def clearData(self):
        self.modeConditionListBox.delete(0, self.modeConditionListBox.size())
        self.conditionListBox.delete(0, self.conditionListBox.size())

        self.resultLabelContent.config(text="\n\n\n\n")
        self.sa.clearData()

        self.ax.cla()

        self.ax.grid(color='grey', alpha=.5, linestyle='--')

        self.ax.set_xlabel('x1 axis')
        self.ax.set_ylabel('x2 axis')

        self.ax.set_title('Linear Programming')

        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    def simplexAlgorithm(self):
        self.modeCondition = self.modeConditionListBox.get(0)
        conditions = self.conditionListBox.get(0, self.conditionListIndex - 1)
        self.sa.initCondition(self.mode, self.modeCondition, list(conditions))
        self.sa.run()

        self.printResult()

    def printResult(self):
        result = self.sa.result
        varLength = len(self.sa.modeCondition)

        self.ax.scatter(result[1], result[2], c='red', s=100)

        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

        purposeCondition = self.modeConditionListBox.get(0, 0)
        purposeCondition = purposeCondition[0] + "=" + str("{0:0.3f}").format(result[0])

        self.modeConditionListBox.delete(0, 0)
        self.modeConditionListBox.insert(0, purposeCondition)

        purposeFunction = self.sa.modeCondition[0:2]

        x1 = (purposeFunction[0] / purposeFunction[1]) * (-1)

        self.ax.plot(self.x, x1 * self.x + (result[0] / purposeFunction[1]), label=purposeCondition)

        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

        text = '\'{0}\'의 최대값: {1:0.3f}\n'.format(self.modeCondition, result[0])
        for i in range(varLength - 1):
            text += '그에 대한 x{0}의 값: {1:0.3f}\n'.format(i + 1, result[i + 1])

        self.resultLabelContent.config(text=text)

    '''
        그래프 관련 메서드
    '''
    def initGraph(self):

        self.x = np.array(range(0, 200))

        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot()

        self.ax.grid(color='grey', alpha=.5, linestyle='--')

        self.ax.set_xlabel('x1 axis')
        self.ax.set_ylabel('x2 axis')

        self.ax.set_title('Linear Programming')

        self.line = FigureCanvasTkAgg(self.figure, self.window)
        self.line.draw()
        self.line.get_tk_widget().pack(side="left", fill="both", expand=True)

    def drawGraph(self, cond):
        fun = self.sa.getCondition(cond)
        print(fun)

        x1 = (-1) * (fun[0] / fun[1])
        b = fun[2] / fun[1]

        self.ax.set_xlim([0, b * 2])
        self.ax.set_ylim([0, b * 2])

        self.ax.plot(self.x, x1 * self.x + b, label=cond)

        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    '''
        동작 메서드
    '''
    def run(self):
        self.window.mainloop()


f = MyFrame()
# f.setGraphFrame()
f.run()
