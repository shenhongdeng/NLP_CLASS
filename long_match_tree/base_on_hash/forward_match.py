import json
def search(cur_dict,cur_num,cur_word,sen,cut_place,flag):
    if  cur_word not in cur_dict.keys():#cur_word是当前字,cur_dict是上个字的字典的值,比如"中国人",cur_word是"人"，cur_dict是{'家':{},'人':{},...}，就是"国"的值
        if cur_num==0:#第一个字就不存在(注意)
            cut_place=0
        else:cut_place=cur_num-1
        flag=0
        return cut_place
    if flag==0:
        return cut_place
    cur_num+=1
    if cur_num==len(sen):
        cut_place=len(sen)-1
        return cut_place
    return search(cur_dict[cur_word],cur_num,sen[cur_num],sen,cut_place,flag)
def split_sen_by_forward(sen,dict_tree):
    ans_list = []
    origin_sen = sen
    while True:
        cut_place=search(dict_tree, 0, sen[0], sen, None, 1)
        ans_list.append(sen[:cut_place+1])
        sen = sen[cut_place+1:]#截断句子
        if len("".join(ans_list)) == len(origin_sen):
            break
    return ans_list
def test():
    In=open("dict_forward_tree.json","r")
    dict_forward_tree=json.load(In)
    In.close()
    while True:
        sen=input("plz input a sentence (input q to quit):")
        if sen=='q':
            break
        ans_list=split_sen_by_forward(sen,dict_forward_tree)
        print("分词结果:",ans_list)

test()