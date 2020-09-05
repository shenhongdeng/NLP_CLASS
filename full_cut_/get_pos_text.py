IN1=open("train.txt","r",encoding="gb18030",errors='ignore')
IN2=open("test.txt","r",encoding="gb18030",errors='ignore')
OUT1=open("pos_text_train.txt","w+")
OUT2=open("pos_text_test.txt","w+")
def makeLabel(text):
    out_text = []
    if len(text) == 1:
        out_text.append('S')
    else:
        out_text += ['B'] + ['I'] * (len(text) - 2) + ['E']
    return out_text
for line in IN1.readlines():
    try:
        single_sen = line.strip()
        if not single_sen:
            continue
        else:
            single_sen=single_sen.split()
        line_state = []
        OUT1.write("^BEGIN/^^" + " ")
        for word in single_sen:
            for i in range(len(word)):
                temp = word[i] + "/" + makeLabel(word)[i]  # [B,E,B,E,S]
                OUT1.write(temp+" ")
        OUT1.write(" $END/$$\n")
    except UnicodeDecodeError:
        continue
for line in IN2.readlines():
    try:
        single_sen = line.strip()
        if not single_sen:
            continue
        else:
            single_sen=single_sen.split()
        line_state = []
        OUT2.write("^BEGIN/^^" + " ")
        for word in single_sen:
            for i in range(len(word)):
                temp = word[i] + "/" + makeLabel(word)[i]  # [B,E,B,E,S]
                OUT2.write(temp+" ")
        OUT2.write(" $END/$$\n")
    except UnicodeDecodeError:
        continue
OUT1.close()
OUT2.close()
