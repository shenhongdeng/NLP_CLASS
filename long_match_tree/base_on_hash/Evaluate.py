import json
from long_match_tree.base_on_hash.back_match import split_sen_by_back
from long_match_tree.base_on_hash.forward_match import split_sen_by_forward

def load_forward_tree_dict():#加载正向匹配的词典树
    In1 = open("dict_forward_tree.json", "r")
    dict_forward_tree = json.load(In1)
    In1.close()
    return dict_forward_tree
def load_back_tree_dict():#加载反向匹配的词典树
    In2 = open("dict_back_tree.json", "r")
    dict_back_tree = json.load(In2)
    In2.close()
    return dict_back_tree

def load_test_text():#把测试集读入
    sen_list=[]
    f = open("test.txt", "r")
    for line in f:
        single_sen = line.strip()
        if not single_sen:
            continue
        else:
            sen_list.append(single_sen.split())
    return sen_list

def makeLabel(sen_list):#给每个词进行BIES的标注
    sen_label=[]
    for word in sen_list:
        word_label = []
        if len(word) == 1:
            word_label.append('S')
        else:
            word_label += ['B'] + ['I'] * (len(word) - 2) + ['E']
        sen_label+=word_label
    return sen_label

def check_label(sen_test_label,predict_label):#用来核对标注是否正确
    temp_total_cnt_test=0
    temp_total_cnt_predict=0
    temp_correct_cnt=0
    for label_tuple in zip(sen_test_label, predict_label):
        if label_tuple[0] == 'E' or label_tuple[0] == 'S':  # 测试集上分了词的位置
            temp_total_cnt_test += 1
        if label_tuple[1] == 'E' or label_tuple[1] == 'S':  # 预测的分词的个数
            temp_total_cnt_predict += 1
            if label_tuple[1] == label_tuple[0]:  # 预测的和测试集上的分的位置一样的,标对的
                temp_correct_cnt += 1
    return temp_total_cnt_test,temp_total_cnt_predict,temp_correct_cnt

def get_evaluation_index_by_forward(all_sen_list):#得到正向匹配在精确率，召回率以及F1值上的表现
    dict_forward_tree=load_forward_tree_dict()
    total_cnt_test=0
    total_cnt_predict=0
    correct_cnt=0
    for sen_list in all_sen_list:
        sen_test_label=makeLabel(sen_list)
        predict_word_list=split_sen_by_forward("".join(sen_list),dict_forward_tree)
        predict_label=makeLabel(predict_word_list)
        temp_total_cnt_test, temp_total_cnt_predict, temp_correct_cnt=check_label(sen_test_label,predict_label)
        total_cnt_test +=temp_total_cnt_test
        total_cnt_predict += temp_total_cnt_predict
        correct_cnt+=temp_correct_cnt
    accuracy = correct_cnt / total_cnt_predict
    recall = correct_cnt / total_cnt_test
    F1=recall * accuracy * 2 / (accuracy + recall)
    return accuracy,recall,F1

def get_evaluation_index_by_back(all_sen_list):#得到反向匹配在精确率，召回率以及F1值上的表现
    dict_back_tree=load_back_tree_dict()
    total_cnt_test=0
    total_cnt_predict=0
    correct_cnt=0
    for sen_list in all_sen_list:
        sen_test_label=makeLabel(sen_list)
        predict_word_list=split_sen_by_back("".join(sen_list),dict_back_tree)
        predict_label=makeLabel(predict_word_list)
        temp_total_cnt_test, temp_total_cnt_predict, temp_correct_cnt=check_label(sen_test_label,predict_label)
        total_cnt_test +=temp_total_cnt_test
        total_cnt_predict += temp_total_cnt_predict
        correct_cnt+=temp_correct_cnt
    accuracy = correct_cnt / total_cnt_predict
    recall = correct_cnt / total_cnt_test
    F1=recall * accuracy * 2 / (accuracy + recall)
    return accuracy,recall,F1

def evaluate_on_test_data():#整体打印
    all_sen_list=load_test_text()
    forward_acc,forward_recall,forward_F1=get_evaluation_index_by_forward(all_sen_list)
    back_acc, back_recall, back_F1 = get_evaluation_index_by_back(all_sen_list)
    print("Precision of forward cut:", forward_acc)#准确率
    print("Recall of forward cut:", forward_recall)#召回率
    print("F1 of forward cut:", forward_F1)#F1值
    print("\n")
    print("Precision of back cut:", back_acc)#准确率
    print("Recall of back cut:", back_recall)#召回率
    print("F1 of back cut:", back_F1)#F1值

evaluate_on_test_data()
