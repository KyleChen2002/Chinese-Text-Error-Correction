基于pycorrector的公文纠错软件
===========================
## 1.demo版本介绍
demo版本分成两种

Linux版：支持文档纠错和文本纠错，文档纠错只能定位到**对应的错误段落**，只支持上传docx文件

Windows版：支持文档纠错和文本纠错，文档纠错可以定位到对应的**错误句子**，支持上传**docx，pdf**文件
## 2.程序相关
### 2.1环境依赖包
#### 2.1.1pycorrector环境配置
cpu训练环境：参考pycorrector官方的readme.md

gpu环境要求：首先检查cuda版本，没有cuda自行安装。找到cuda版本对应的ptorch版本

云服务器环境部署：已在featurize平台完成部署，只需要将压缩包**上传到/work工作目录**下即可。解压后方可使用
#### 2.1.2自动生成数据集环境配置
1. jionlp（用于生成混淆同音词，产生错误的训练数据）
    
    `pip install jionlp`  
2. json（对训练所需的数据集.json进行操作）
    
    `pip install json`
#### 2.1.3显示纠错结果环境配置
文本纠错
1. difflib库
    
    `pip install difflib`

文档纠错

windows版：
1. win32com库（用于在word上生成批注）
    
    `pip install pywin32`

linux版：
2. docx库（用于在word上生成批注）
    
    `pip install python-docx`
    
    `pip install bayoo-docx`


### 2.2运行方式
#### 2.2.1训练启动方式
本机：
`python train.py`

featurize服务器：

`conda activate /cloud/test26`

`cd /cloud/pycorrector/pycorrector/macbert`

`python train.py`

#### 2.2.2训练结果模型
每轮训练都会保存ckpt文件，当达到目标的epoch后会生成新的pytorch_model.bin文件
model：`../pycorrector/pycorrector/macbert/output/macbert4csc/pytorch_model.bin`
ckpt：`../pycorrector/pycorrector/macbert/output/macbert4csc/epoch=轮数-val_loss=xxxx`


#### 2.2.3相关文件配置
1. 1)账号文件位置
    
    `../pycorrector/user_secret_file`
    
    2）账号文件修改
    新用户需添加：**用户名** otp totp:sha1:base32:WZWAD7BYIBWZTFZ57PFGJNU5T4:**密码**:xxx *
2. 1)config文件位置
    
    `../pycorrector/config.py`
    
    2)config文件修改
    需**修改UPLOAD_FOLDER文件夹**位置，应该位于flaskr文件夹下一级目录
4. 1)训练参数文件位置
    `../pycorrector/pycorrector/macbert/output/train_macbert4csc.yml`

    2)修改训练参数文件
    
    `HYPER_PARAMS:`超参数修改
    
    `DATASETS:`设置train，valid与test三个.json数据集的位置

    `SOLVER: BATCH_SIZE,MAX_EPOCHS`：
           `BATCH_SIZE`设定参照硬件性能（cpu训练--内存，gpu训练--显存），性能越强就可设置越高
           当训练出现`cuda out of memory`的错误，应降低BATCH_SIZE的数值。
           `MAX_EPOCHS`设定决定训练轮次，只有到预定参数才会停止训练。


#### 2.2.4启动服务方式
linux服务器：

`cd /data/pycorrector`

`pkill python3`

`sh start.sh`(调用app.py)

windows服务器：

`python appwin.py`


#### 2.2.5自定义数据集启动
`../pycorrector/tests/createDatasetTest_v2.0.py`

原始的公文样本需要存储在txt文件中，向程序指定存储的公文位置。之后还需要向程序指定需要append的.json数据集位置。



#### 2.2.6更换模型
windows版：
c:/user/.../.pycorrector/dataset/macbert_model/chinese_finetuned_correction/pytorch_model.bin

linux版：
/data/pycorrector/pycorrector/macbert/output/pytorch_model.bin



### 2.3可添加功能（仅供参考）
1. 定制自己的词典
2. 定位错误词句更加准确（windows版支持定位到对应的错误字）
3. 支持上传更多的文件版本（如图片，ppt）


### 2.4常见错误

creatDatasetv2.0新生成的.json文件训练出现batchsize问题，原因是数据集文件过长。检查json文件中的数据集，是否长度过长（超过128甚至于512）






