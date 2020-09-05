import json
f1=open("pos2pos.json","r")
pos2pos=json.load(f1)
f2=open("name_list.json","r")
name_set=set(json.load(f2))
f3=open("word_list.json","r")
word_set=set(json.load(f3))

def makeLabel(text):
    out_text = []
    if len(text) == 1:
        out_text.append('S')
    else:
        out_text += ['B'] + ['I'] * (len(text) - 2) + ['E']
    return out_text
#正反向最大匹配
def back_cut_and_forward_cut(text,word2pos):
    index = len(text)
    wind_size = 32
    while index > 0:
        word = None
        if wind_size > index:
            wind_size = index
        for size in range(wind_size, 0, -1):
            piece = text[(index - size):index]
            if piece in name_set or piece in word_set:
                word = piece
                POSs=makeLabel(word)
                for i in range(len(word)):
                    if not word2pos.get(word[i]):
                        word2pos[word[i]] = list()
                    if POSs[i] not in word2pos[word[i]]:
                        word2pos[word[i]].append(POSs[i])
                index -= size
                break
        if word is None:
            unmatched_word=text[(index - 1):index]
            word2pos[unmatched_word]=list(('B','I','E','S'))
            index -= 1
    index = 0
    if wind_size>len(text):
        wind_size=len(text)
    while index < len(text):
        word = None
        for size in range(wind_size, 0, -1):
            piece = text[index:index + size]
            if piece in name_set or piece in word_set:
                word = piece
                POSs = makeLabel(word)
                for i in range(len(word)):
                    if not word2pos.get(word[i]):
                        word2pos[word[i]] = list()
                    if POSs[i] not in word2pos[word[i]]:
                        word2pos[word[i]].append(POSs[i])
                index += size
                break
        if word is None:
            unmatched_word=text[index:index+1]
            word2pos[unmatched_word]=list(('B','I','E','S'))
            index+=1

def GetCandidate(word, POSs,word2pos):
    if word2pos.get(word):
        for pos in word2pos[word]:
            POSs.append(pos)

def BuildLattice(sentence, Lattice,word2pos):
    List=[]
    for i in sentence:
        List.append(i)
    List.insert(0, "^BEGIN")
    List.append("$END")
    for word in List:
        POSs = []  # 该字对应所有序号[B,I..]
        GetCandidate(word, POSs,word2pos)
        if len(POSs) == 0:
            POSs = ['B','I','E','S']
        Column = []
        for POS in POSs:
            Unit = []
            Unit.append(POS)
            Unit.append(word)
            Unit.append(-100.0)  # total_pro
            Unit.append(0)  # index
            Column.append(Unit)  # 就是POS，word，概率，指针的四元组的初始化
        Lattice.append(Column)  # 网格里的每一层
    return 1
def Get_Transfer_Prob(pos_cur, pos_head):
    Ret = -100.0
    if pos2pos.get(pos_head).get(pos_cur):
        Ret = pos2pos[pos_head][pos_cur]
    return Ret

def SearchLattice(Lattice):  # 网格和概率传入
    for i in range(1, len(Lattice)):
        for j in range(len(Lattice[i])):
            Prob = 0.0
            Max = -1000
            pos_cur = Lattice[i][j][0]
            word_cur = Lattice[i][j][1]
            for k in range(len(Lattice[i - 1])):
                pos_head = Lattice[i - 1][k][0]
                Prob = Get_Transfer_Prob(pos_cur, pos_head) + Lattice[i - 1][k][2]  # 表里面拿概率，加上一层的概率
                if Prob > Max:
                    Lattice[i][j][3] = k  # 存的是上一层的index
                    Max = Prob
            Lattice[i][j][2] = Max

def BackLattice(Lattice):  # 回溯输出答案的过程
    Unit = []
    ColumnNo = len(Lattice) - 1  # 到最后一层
    Unit = Lattice[ColumnNo][len(Lattice[ColumnNo]) - 1]
    RetArray = []
    while ColumnNo > 0:
        if Unit[0] != "$$":  # 到达结尾
            RetArray.insert(0, (Unit[0], Unit[1]))
        Unit = Lattice[ColumnNo - 1][Unit[3]]
        ColumnNo -= 1
    final_show = []
    #final_pos = []
    for i in RetArray:
        final_show.append(i[1] + "/" + i[0])
        #final_pos.append(i[0])
    Ret = " ".join(final_show)
    return Ret
def get_accuracy_on_test_data():
    f=open("pos_text_test.txt","r")
    total_cnt = 0
    correct_cnt = 0
    total_cnt_test=0
    for line in f:
        single_sen = line.strip()
        if not single_sen :
            continue
        else :
            single_sen=single_sen.split()
        single_sen=single_sen[1:-1]
        sen_word=[]
        for unit in single_sen:
            sen_word.append(unit[0])
        sen="".join(sen_word)
        predic=split_word(sen).split()
        predic=predic[:-1]
        for word_tuple in zip(single_sen,predic):
            if word_tuple[0][2] == 'E' or word_tuple[0][2] == 'S':
                total_cnt_test+=1
            if word_tuple[1][2]=='E' or word_tuple[1][2]=='S':
                total_cnt+=1
                if word_tuple[1][2]==word_tuple[0][2]:
                    correct_cnt+=1
    accuracy=correct_cnt/total_cnt
    call_back=correct_cnt/total_cnt_test
    print("Precision:",accuracy)
    print("Recall:",call_back)
    print("F1:",call_back*accuracy*2/(accuracy+call_back))





def split_word(sentence):
    word2pos = {}
    back_cut_and_forward_cut(sentence,word2pos)
    Lattice = []
    BuildLattice(sentence, Lattice, word2pos)
    SearchLattice(Lattice)
    return BackLattice(Lattice)


def main():
    get_accuracy_on_test_data()
    while 1:
        sentence = input("Pls Input the sentence (press q to quit):")
        if sentence == "q":
            break
        x=split_word(sentence).split()[:-1]
        print(x)
        y = []
        for i in x:
            if i[2] == 'S' or i[2] == 'E':#记得要两次i[2]
                y.append(i[0] + "/")
            else:
                y.append(i[0])
        temp="".join(y)
        print(temp)
main()