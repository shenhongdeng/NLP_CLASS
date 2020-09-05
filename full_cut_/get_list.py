import json
IN1=open("person.txt","r")
name_list=[]
for single in IN1:
    single_sen = single.strip()
    if not single_sen:
        continue
    else:
        single_sen = single_sen.split(",")
    name=single_sen[0]
    name_list.append(name)
IN1.close()
f1=open("name_list.json","w+")
json.dump(name_list,f1)
IN2=open("train.txt","r",encoding="gb18030")
word_list=[]
for line in IN2:
    single_sen = line.strip()
    if not single_sen:
        continue
    else:
        single_sen=single_sen.split(" ")
    for word in single_sen:
        word_list.append(word)

IN2.close()
f2=open("word_list.json","w+")
json.dump(word_list,f2)