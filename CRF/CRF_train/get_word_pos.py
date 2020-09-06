f1=open("pos_text_train.txt","r")
f2=open("pos_text_test.txt","r")
out1=open("CRF_train.txt","w+",encoding="utf8")
out2=open("CRF_test.txt","w+",encoding="utf8")
for line in f1:
    line=line.strip()
    if not line:
        continue
    else:
        sen=line.split()
    sen=sen[1:-1]
    for word_pos in sen:
        word=word_pos[0]
        pos=word_pos[2]
        out1.write(word+"	"+pos+"\n")
    out1.write("\n")
out1.close()
for line in f2:
    line=line.strip()
    if not line:
        continue
    else:
        sen=line.split()
    sen=sen[1:-1]
    for word_pos in sen:
        word=word_pos[0]
        pos=word_pos[2]
        out2.write(word+"	"+pos+"\n")
    out2.write("\n")
out2.close()