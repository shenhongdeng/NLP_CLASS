import re#导入正则模块
class CRF:#定义CRF类
    Feature = {}#用来存放特征实例
    Weight = []#用来存放每个特征实例的权值
    STATE = ["B", "E", "I", "S"]#四种标注状态
    STATE2ID = {"B": 0, "E": 1, "I": 2, "S": 3}#标注状态对应的序号。在后面取对应标注装的权重的时候用
    def CRFInit(self, Model):#model就是my_model.txt文件
        Inp = open(Model, "r", encoding="utf-8")
        for Line in Inp:
            Line = Line.strip()
            match1 = re.search("(\d+)\s([^:]+):(.*)",Line)#用来提取特征实例，一个括号配对代表一个group
            match2 = re.search("(-?\d+\.\d+)",Line)#用来提取权值
            if match2:#是权值
                self.Weight.append(float(match2.group(0)))#0就是整个字符串返回
            elif match1:#是特征
                if not self.Feature.get(match1.group(2)):
                    self.Feature[match1.group(2)] = {}
                self.Feature[match1.group(2)][match1.group(3)] = int(match1.group(1))#1，2，3就分别表示对应的权值的行数序号，模板类型，以及字
        #模板类型：{字：权值序号}
        Inp.close()
    def GetStateProb(self, HZArray, No, State):
        Prob = 0.0
        #这边就是看看这个状态下有没有对应各个特征模板下的实例，有的话就进去提取出来，把对应的权值都加入到Prob里面
        if self.Feature["U01"].get(HZArray[No - 1]):#找到前一个字
            Prob += self.Weight[self.Feature["U01"][HZArray[No - 1]] + self.STATE2ID[State]]#每一个特征实例有对应4个状态比如，16-20，要看是哪个state还要再加，才能找到对应的权重
        if self.Feature["U02"].get(HZArray[No]):
            Prob += self.Weight[self.Feature["U02"][HZArray[No]] + self.STATE2ID[State]]
        if self.Feature["U04"].get(HZArray[No - 1] + "/" + HZArray[No]):#04是有两个字的，特征实例有一个斜杠记得要加
            Prob += self.Weight[self.Feature["U04"][HZArray[No - 1] + "/" + HZArray[No]] + self.STATE2ID[State]]
        if No < len(HZArray) - 1:#U03,U05设计到取后一个字，所以要注意有没有到最后一列，如果到最后一列就不用进入这两个特征模板下的实例提取了
            if self.Feature["U03"].get(HZArray[No + 1]):
                Prob += self.Weight[self.Feature["U03"][HZArray[No + 1]] + self.STATE2ID[State]]
            if self.Feature["U05"].get(HZArray[No] + "/" + HZArray[No + 1]):
                Prob += self.Weight[self.Feature["U05"][HZArray[No] + "/" + HZArray[No + 1]] + self.STATE2ID[State]]
        return Prob

    def GetTransitionProb(self, State1, State2):#得到状态转移概率
        ID = 4 * self.STATE2ID[State1] + self.STATE2ID[State2]#前面16行中的其中一种，训练出来的my_model.txt下，前16行对应的是转移概率
        return self.Weight[ID]

    def Format(self, RetArray):
        Ret=""
        for Unit in RetArray:
            if Unit[0] == "S" or Unit[0]=="E":
                Ret+=Unit[3]+'/'#对应的字
            elif Unit[0] == "B" or Unit[0]=="I":
                #Ret+=" "
                Ret+=Unit[3]
            # else:
            #     Ret+=Unit[3]
        Ret=re.sub("^\s","",Ret)#替代
        Ret=re.sub("\s$","",Ret)
        return 	Ret
        

    def Viterbi(self, Sentence):
        HZArray = []#用来装字的
        Lattice = []#建的网格
        RetArray = []#返回的序列
        self.Sent2Array(Sentence, HZArray)
        self.BuildLattice(HZArray, Lattice)
        self.SearchLattice(Lattice, HZArray)#把表格上的每个信息都填上
        self.GetRet(Lattice, RetArray)#找到最优的序列，并返回给RetArray
        Ret = self.Format(RetArray)
        return Ret

    def Sent2Array(self, Sentence, HZArray):#切成字[_B-1,....,_B+1]
        HZArray.append("_B-1")
        for i in range(len(Sentence)):
            HZArray.append(Sentence[i])
        HZArray.append("_B+1")

    def BuildLattice(self, HZArray, Lattice):
        for HZ in HZArray:
            HZs = []
            Column = []
            for S in self.STATE:#把每一种state也就是B,I,E,S都添加进去，因为是一个全排列的东西，每一个都是一个四元组(状态，概率，index,字)
                Unit = []
                Unit.append(S)#标注
                Unit.append(-100.0)#概率
                Unit.append(0)#索引
                Unit.append(HZ)#汉字
                Column.append(Unit)#该列
            Lattice.append(Column)

    def SearchLattice(self, Lattice, HZArray):
        for i in range(1, len(Lattice)):#跳过第一列
            for j in range(len(Lattice[i])):#每一列里的所有的情况
                Prob = 0.0
                Max = -1000
                for k in range(len(Lattice[i - 1])):#前一列
                    TransitionProb = self.GetTransitionProb(Lattice[i - 1][k][0], Lattice[i][j][0])#状态转移的概率
                    StateProb = self.GetStateProb(HZArray, i, Lattice[i][j][0])#这个就是从状态到观察序列的一个权值，他直接把整个汉字的词序列给传入进去了，实现了CRF的关键(关联上下文)
                    Prob = StateProb + TransitionProb + Lattice[i - 1][k][1]   #👆当前的状态，当前的列
                    if Prob > Max:
                        Lattice[i][j][2] = k
                        Max = Prob
                Lattice[i][j][1] = Max

    def GetRet(self, Lattice, RetArray):
        Unit = []
        ColumnNo = len(Lattice) - 1
        Unit = Lattice[ColumnNo][len(Lattice[ColumnNo]) - 1]#从_B+1开始回溯，他已经把最优的路径已经保存下来了
        while ColumnNo > 0:
            if Unit[3] != "_B+1":
                RetArray.insert(0, Unit)#把每一个state从头往前插入进去了(前插),(四元组)
            Unit = Lattice[ColumnNo - 1][Unit[2]]#index对应的state，每一个都是一个四元组
            ColumnNo -= 1


def Main():
    obCRF = CRF()
    print("Init....", end="")
    obCRF.CRFInit("my_model.txt")
    print("Done!")
    while 1:
        Sentence=input("Pls:")
        if Sentence == "q":
            break
        Ret=obCRF.Viterbi(Sentence)
        print(Ret)

Main()