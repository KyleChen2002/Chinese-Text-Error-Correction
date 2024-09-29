import jionlp as jio
import json
import re
import pandas as pd
import csv
'''
v2.0版本加入了append操作，可以自动在原来的.json文件后添加list，扩展数据集
希望完成数据集清洗操作
'''

def creatDataset_valid(stro,rst):
    res = jio.homophone_substitution(stro)
    res1 = res[:1]
    rst = res + res1
    with open('C:/Users/Chen Junkai/Desktop/test.tsv', 'wt') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(rst)
    #return rst


def creatDataset_sentence(stro,strf):
    '''
    rest = jio.remove_parentheses(stro)
    rest = ''.join(rest)
    res = jio.homophone_substitution(rest)
    '''
    res = jio.homophone_substitution(stro)
    res1 = res[:1]
    res2 = res[1:2]
    res3 = res[2:3]
    stro = str(stro)
    str1 = ''.join(res1)
    str2 = ''.join(res2)
    str3 = ''.join(res3)


    strf1 = str1+' '+stro
    strf2 = str2+' '+stro
    strf3 = str3 + ' ' + stro
    strf += strf1+'\n'+strf2+'\n'+strf3+'\n'

    return strf
    #print(strf)

    '''
    temp1 = []
    for i in range(len(str1) - 1):
        if stro[i] != str1[i]:
            temp1.append(i)
    
    rst.append({'id': "-",
                'original_text': str1,
                'wrong_ids': temp1,
                'correct_text': stro})
    
        #print(type(rst))
    temp2 = []
    if str2=="":
        pass
    else:
        for i in range(len(str2)-1):
            if stro[i] != str2[i]:
                temp2.append(i)
        rst.append({'id': "-",
                    'original_text': str2,
                    'wrong_ids': temp2,
                    'correct_text': stro})

    temp3 = []
    if str3=="":
        pass
    else:
        for i in range(len(str3)-1):
            if stro[i] != str3[i]:
                temp3.append(i)
        rst.append({'id': "-",
                    'original_text': str3,
                    'wrong_ids': temp3,
                    'correct_text': stro})
    '''
'''
def appendDataset_test(stro,rst):
    choose=input("right or wrong")
    temperr = []
    if choose == "wrong":
        wrongWord=input("input the wrong word")
        for i in range(len(stro)):
            for a in wrongword:
                if a == stro[i]:
                    temperr.append[i]
        rst.append({'id': "-",
                    'original_text': str3,
                    'wrong_ids': temperr,
                    'correct_text': stro})
    else:
        for i in range(len(stro)):

'''


'''
def main():
    strf = ""
    #rst = []
    #print(type(rst))
    with open('C:/Users/Chen Junkai/Desktop/trainDataSet1.txt') as f: #原始的txt数据
        read_data = f.read()
        read_data = read_data.split("\n")     #去掉回车的\n
        read_data = "".join(read_data)
        #read_data.replace(r"\n","").replace(r"\r", "")
        #read_data.replace("\\r\\n","")
        a = re.split(r"[。！]",read_data)
        #a = read_data.strip('\n').split("。")
        for strof in a:
        #for i in range(len(a)):
            #temp = a[i:i+1]
            #strof = ''.join(temp)
            if strof == '' or strof[0] == "（" or "0" <= strof[0] <= "9" or len(strof) <= 10 or len(strof) >= 80:
                continue
            strf = creatDataset_sentence(strof, strf)
            #creatDataset_valid(strof,rst)
    print(strf)
    with open('C:/Users/Chen Junkai/Desktop/test.txt', 'w', encoding='utf8') as f1:
        f1.write(strf)

'''
def main():
    with open('C:/Users/Chen Junkai/Desktop/test.tsv', 'w+', encoding="utf8") as t:
        with open("C:/Users/Chen Junkai/Desktop/test.txt", 'r', encoding='utf8') as f:
            # print(f.readlines())
            for line in f.readlines():
                # print(line)
                line_list = line.strip('\n').split()  # 去掉str左右端的空格并以空格分割成list
                # print(line_list)
                hbaseRowID_list = line_list[0:2]  # 取前三个list中的元素
                # print(hbaseRowID_list)
                # hbaseRowID = line_list[0]+line_list[1]+line_list[2]
                hbaseRowID = "-".join(hbaseRowID_list)  # 连接list
                # print(hbaseRowID)
                # print(type(line_list))
                # print(line_list)
                line_list[1] = hbaseRowID
                tsv_list = line_list[1:]
                tsv_list = '\t'.join(tsv_list)
                print(tsv_list)
                t.write(tsv_list + '\n')


if __name__ == '__main__':
    main()

