import json
'''
程序用于将两个json文件拼接在一起
'''


with open('D:/pycorrector/pycorrector/macbert/output/SIGHAN+Wang271K中文纠错数据集/train.json', 'r+', encoding='utf8') as f:#文件1，为拼接后存储新文件的地址
    strtemp = f.read()
    content = json.loads(strtemp)
    content = json.dumps(content, indent=4, ensure_ascii=False)  # 将list转为str

    f.seek(0)  # 指向文本开头，这两行的用处是因为r+只能读写原文的内容并向后追加，加入后就能实现更改前两行的内容
    f.truncate()  # 清除文本

    # content.rstrip("]")
    # rst.strip("[")
    '''此部分是因为rst和content必须转变为str才能写入，就会存在原文件最后一行多余的]以及新文件第一行多余的[，并且中间少了，连接'''
    content = content[:len(content) - 2]
    content = content + ","
    #print('type of content: ' +str(type(content)))
    #print('type of rst:' + str(type(rst)))
    with open('D:/pycorrector/pycorrector/macbert/output/trainbig26f.json', 'r',#文件2，用于提供需要拼接的内容
              encoding='utf8') as f1:
        tmp = f1.read()
        contentadd = json.loads(tmp)
        contentadd = json.dumps(contentadd, indent=4, ensure_ascii=False)
    contentadd = contentadd[1:]
    contentadd = content + contentadd
    # rst = rst[:len(rst)-2]
    # print(rst)
    f.write(contentadd)
    print("success!")