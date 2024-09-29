import jionlp as jio
import json
import re
'''
v1.0版本已经可以完成单个txt的分句，每句话生成三个错误样本以及转json操作
'''

def creatDataset_sentence(stro,rst):
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

    temp1 = []
    if str1=="":
        pass
    else:
        for i in range(len(str1)):
            if stro[i] != str1[i]:
                temp1.append(i)

        rst.append({'id': "-",
                    'original_text': str1,
                    'wrong_ids': temp1,
                    'correct_text': stro})
    temp2 = []
    if str2=="":
        pass
    else:
        for i in range(len(str2)):
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
        for i in range(len(str3)):
            if stro[i] != str3[i]:
                temp3.append(i)
        rst.append({'id': "-",
                    'original_text': str3,
                    'wrong_ids': temp3,
                    'correct_text': stro})

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



def main():
    rst = []
    with open('C:/Users/Chen Junkai/Desktop/trainDataSet.txt') as f:
        read_data=f.read()
        read_data=read_data.split("\n")
        read_data = "".join(read_data)
        #read_data.replace(r"\n","").replace(r"\r", "")
        #read_data.replace("\\r\\n","")
        a =re.split(r"[。！]",read_data)
        #a = read_data.strip('\n').split("。")
        for strof in a:
        #for i in range(len(a)):
            #temp = a[i:i+1]
            #strof = ''.join(temp)
            if strof == '' or strof[0] == "（" or "0" <= strof[0] <= "9" or len(strof) <= 10:
                continue
            creatDataset_sentence(strof, rst)
    rst = json.dumps(rst, indent=4, ensure_ascii=False)
    print(type(rst))
    #print(rst)
    #rst.rstrip(" ]")
    #rst = rst[:len(rst)-2]
    #rst = rst+","
    # sav e_json(rst, '../output/cged.json')
    with open('D:/pycorrector/pycorrector/macbert/output/TestRejoin.json', 'w', encoding='utf-8') as result_file:
        result_file.write(rst)
        print("success")
if __name__ == '__main__':
    main()

