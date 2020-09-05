import json
def search(cur_dict,cur_num,cur_word,sen,cut_place,flag):#每次最大长度搜索一个词出来,cur_num表示当前匹配到第几个字了,sen表示当前传进来的原始句子,cut_place是用来存储最大的切分位置的，,flag是用来看是不是已经满足最大匹配了
    if  cur_word not in cur_dict.keys():#cur_word是当前字,cur_dict是上个字的字典的值,比如"中国人",cur_word是"人"，cur_dict是{'家':{},'人':{},...}，就是"国"的值
        if cur_num==len(sen)-1:#第一个字就不存在(注意)
            cut_place=len(sen)-1
        else:cut_place=cur_num+1
        flag=0
        return cut_place
    if flag==0:
        return cut_place
    cur_num-=1
    if cur_num==-1:
        cut_place=0
        return cut_place
    return search(cur_dict[cur_word],cur_num,sen[cur_num],sen,cut_place,flag)#递归调用
def split_sen_by_back(sen,dict_tree):#sen就是整个完整的句子(用户输入的),dict_tree是前面构建好的词典树
    ans_list = []
    origin_sen = sen
    while True:
        cut_place=search(dict_tree, len(sen)-1, sen[-1], sen, None, 1)#从最后一个字开始往前找
        ans_list.append(sen[cut_place:])
        sen = sen[:cut_place]#截断句子
        if len("".join(ans_list)) == len(origin_sen):#判断这个句子是不是已经分好词了
            break
    return ans_list[::-1]
def test():
    In=open("dict_back_tree.json","r")#把建好的词典树传入进来
    dict_back_tree=json.load(In)
    In.close()
    while True:
        sen=input("plz input a sentence (input q to quit):")
        if sen=='q':
            break
        ans_list=split_sen_by_back(sen,dict_back_tree)
        print("分词结果:",ans_list)
test()