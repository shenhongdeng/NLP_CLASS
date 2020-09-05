import math
import json
IN1=open(r"pos_text_train.txt")
pos2pos={}
#calculate corresponding frequency
for sentence in IN1:
    word_pos_list=sentence.strip().split(" ")
    pos_list = []
    for wordpos in word_pos_list:
        word_pos = wordpos.split("/")
        pos_list.append(word_pos[-1])
    for i in range(len(pos_list)-1):
        if not pos2pos.get(pos_list[i]):
            pos2pos[pos_list[i]]={}
            pos2pos[pos_list[i]]['total'] = 0#total一开始放错位置效果比较差
        if not pos2pos.get(pos_list[i]).get(pos_list[i+1]):
            pos2pos[pos_list[i]][pos_list[i+1]]=0
        pos2pos[pos_list[i]][pos_list[i+1]] += 1
        pos2pos[pos_list[i]]['total'] += 1
# #calculate transfer pro
for head_pos in pos2pos.keys():#fromkyes()是用来新建词典的
    for follow_pos in pos2pos[head_pos].keys():
        if follow_pos=='total':continue
        pos2pos[head_pos][follow_pos]=math.log(pos2pos[head_pos][follow_pos]/pos2pos[head_pos]['total'])
out1=open("pos2pos.json","w+")
json.dump(pos2pos,out1)