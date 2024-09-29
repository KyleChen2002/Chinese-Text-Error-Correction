import jionlp as jio
import json
import re
'''
v2.0版本加入了append操作，可以自动在原来的.json文件后添加list，扩展数据集（确保原先的.json已经存在内容）
'''

def creatDataset_sentence(stro,rst):
    '''
    rest = jio.remove_parentheses(stro)
    rest = ''.join(rest)
    res = jio.homophone_substitution(rest)
    '''
    res = jio.homophone_substitution(stro)  #调用jionlp包生成混淆的同音词，默认生成三个list类型的错误样本
    res1 = res[:1]  #res1-3是提取三个混淆同音词的错误样本
    res2 = res[1:2]
    res3 = res[2:3]
    stro = str(stro)    #将数据转换成str格式
    str1 = ''.join(res1)
    str2 = ''.join(res2)
    str3 = ''.join(res3)

    temp1 = []
    if str1 == "":
        pass
    else:
        for i in range(len(str1)-1):        #找到与原文不匹配的部分，认为是错误部分，将其添加到rst中
            if stro[i] != str1[i]:
                temp1.append(i)

        rst.append({'id': "-",
                    'original_text': str1,
                    'wrong_ids': temp1,
                    'correct_text': stro})
    temp2 = []
    if str2 == "":
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
    if str3 == "":
        pass
    else:
        for i in range(len(str3)-1):
            if stro[i] != str3[i]:
                temp3.append(i)
        rst.append({'id': "-",
                    'original_text': str3,
                    'wrong_ids': temp3,
                    'correct_text': stro})

def main():
    rst = []
    print(type(rst))
    # with open('C:/Users/Chen Junkai/Desktop/trainDataSetbig26.txt') as f: #原始的txt数据
    with open('D:/Programming/SoftwareEngineering/train74.txt') as f:  # 原始的txt数据
        read_data = f.read()
        read_data = read_data.split("\n")     #去掉回车的\n
        read_data = "".join(read_data)
        a = re.split(r"[。！]",read_data)     #用。以及！切割长字符串
        for strof in a:
            if strof == '' or strof[0] == "（" or "0" <= strof[0] <= "9" or len(strof) <= 10 or len(strof) >= 80:    #筛选传入的字符，如果开头带有（，数字认为样本不够干净，去除这句话
                continue                                                                                            #同时长度大于80也会去除该句话，因为过长会导致训练出错
            creatDataset_sentence(strof, rst)   #生成错误样本的list，结果在rst中
    rst = json.dumps(rst, indent=4, ensure_ascii=False)

    with open('D:/pycorrector/pycorrector/macbert/output/train74.json', 'r+', encoding='utf8') as f:  # 输入需要添加数据集的.json文件
        strtemp = f.read()

        if strtemp == '':
            rst = json.dumps(rst, indent=4, ensure_ascii=False)

        else:
            content = json.loads(strtemp)
            content = json.dumps(content, indent=4, ensure_ascii=False)  # 将list转为str

            f.seek(0)  # 指向文本开头，这两行的用处是因为r+只能读写原文的内容并向后追加，加入后就能实现更改前两行的内容
            f.truncate()  # 清除文本

            '''此部分是因为rst和content必须转变为str才能写入，就会存在原文件最后一行多余的]以及新文件第一行多余的[，并且中间少了，连接'''
            content = content[:len(content) - 2]
            content = content + ","
            rst = rst[1:]
            rst = content + rst
        f.write(rst)
        print("success!")

if __name__ == '__main__':
    main()

