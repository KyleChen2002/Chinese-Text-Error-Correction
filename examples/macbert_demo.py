# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""
import sys

sys.path.append("..")
from pycorrector.macbert.macbert_corrector import MacBertCorrector


def use_origin_transformers():
    # 原生transformers库调用
    import operator
    import torch
    from transformers import BertTokenizerFast, BertForMaskedLM
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    tokenizer = BertTokenizerFast.from_pretrained("shibing624/macbert4csc-base-chinese")
    model = BertForMaskedLM.from_pretrained("shibing624/macbert4csc-base-chinese")
    model.to(device)

    texts = ["今天新情很好", "你找到你最喜欢的工作，我也很高心。", "我不唉“看 琅擤琊榜”"]

    text_tokens = tokenizer(texts, padding=True, return_tensors='pt').to(device)
    with torch.no_grad():
        outputs = model(**text_tokens)

    def get_errors(corrected_text, origin_text):
        sub_details = []
        for i, ori_char in enumerate(origin_text):
            if ori_char in [' ', '“', '”', '‘', '’', '\n', '…', '—', '擤']:
                # add unk word
                corrected_text = corrected_text[:i] + ori_char + corrected_text[i:]
                continue
            if i >= len(corrected_text):
                break
            if ori_char != corrected_text[i]:
                if ori_char.lower() == corrected_text[i]:
                    # pass english upper char
                    corrected_text = corrected_text[:i] + ori_char + corrected_text[i + 1:]
                    continue
                sub_details.append((ori_char, corrected_text[i], i, i + 1))
        sub_details = sorted(sub_details, key=operator.itemgetter(2))
        return corrected_text, sub_details

    result = []
    for ids, (i, text) in zip(outputs.logits, enumerate(texts)):
        _text = tokenizer.decode((torch.argmax(ids, dim=-1) * text_tokens.attention_mask[i]),
                                 skip_special_tokens=True).replace(' ', '')
        corrected_text, details = get_errors(_text, text)
        print(text, ' => ', corrected_text, details)
        result.append((corrected_text, details))
    print(result)
    return result


if __name__ == '__main__':
    # 原生transformers库调用
    #use_origin_transformers()

    # pycorrector封装调用
    error_sentences = [
        '为鼓励各部门创收、提高费用之出的收入转化率，经总经办审议，财务部新出台政侧',
        '我们大佳伙一起出门',
        '您好，您的问题正在处理中，请您稍厚。感谢您的理解与支持',
        '真麻烦你了。希望你们好好的跳无',
        '少先队员因该为老人让坐',
        '机七学习是人工智能领遇最能体现智能的一个分知',
        '一只小鱼船浮在平净的河面上',
        '我的家乡是有明的渔米之乡',
        '少先队员因该为老人让坐',
        '少 先  队 员 因 该 为 老人让坐',
        '机七学习是人工智能领遇最能体现智能的一个分知',
        '今天心情很好',
        '老是较书。',
        '遇到一位很棒的奴生跟我聊天。',
        '他的语说的很好，法语也不错',
        '他法语说的很好，的语也不错',
        '他们的吵翻很不错，再说他们做的咖喱鸡也好吃',
        '影像小孩子想的快，学习管理的斑法',
        '餐厅的换经费产适合约会',
        '走路真的麻坊，我也没有喝的东西，在家汪了',
        '因为爸爸在看录音机，所以我没得看',
        '不过在许多传统国家，女人向未得到平等',
    ]

    error_sentences = [ '''
随着时针的转动，我们即将告别充满挑站、奋发有为的2021年，迎来充满希望、奋发进取的2022年。在此，我代表中粮资本班子，向过去一年为公司发展付出辛勤劳动的全体同事以及你们的家人表示衷心的感谢和祝福，致以最诚挚的新年问候！
2021年，是中粮资本“十四五”发展的开局之年，也是我们实现三年高质量发展的收官之年，对中粮资本具有重大意义。这一年，国际国内经济形势错综复杂，金融行业强监管、强转型、强竞争持续深化，新冠肺炎疫情反复多点爆发，寿险、信托、期货、基金等行业出现新变化、新趋势、新要求，企业转形发展迫在眉睫，中粮资本负重承压前行。这一年,中粮资本坚决贯彻落实集团党组的决策部署，努力克服内外部不利因素，紧盯“十四五” 战略目标，持续深化改革，主动把握市场机遇，加快核心业务转型发展，主要经营指标实现超同期、超历史、超预算，圆满完成开局之年的各项经营任务。这一年，中粮资本建设活力组织，打造金融铁军，全体员工齐心协力，苦干实干，在进取中实现价值，在拼搏中彰显精神，活力、铁军文化深入人心。
还是这一年，中粮资本各项事业蓬勃发展，捷报频传。在本部成立数字化中心，全面启动中粮资本整体层面的数字化建设，围绕科技赋能业务、提升价值创造开展了多项卓有成效的工作。中英人寿坚持创新探索第二成长曲线，战略研讨明确发展目标，康养项目扎实推进。中粮信托在做好受托服务的同时，全力探索创新驱动，标品业务布局初现成效，各条线逐渐转型升级均衡发展，财富管理多元化资金渠道取得明显成效。中粮期货客户结构持续优化，金融客户布局提速，创新步伐加快，“保险+期货+订单+信贷”模式入选中期协“期货经营机构服务实体经济优秀案例”。中怡保险经纪在巩固现有业务的同时不断强化自身创新能力，完善行业聚焦策略，成立中怡書院，市场品牌和业务发展能力显著提升。中粮基金完成新消费基金组建和胡杨基金参股工作，胡杨子基金、主题基金等多只子基金组建取得新突破。中粮资本（香港）、深圳明诚完成核心团队组建，设立海南基金公司，大湾区基金业务统筹发展格局初步显现。中粮金科的粮信、升悦、农粮数字贸易及云飞票四大平台业务与集团粮油食品业务全面对接，供应链金融业务再上新台阶。
沦海当前，必当扬帆破浪，任重道远，更需砥砺前行，展望新的一年，中央经济工作会议提出坚持稳中求进工作总基调，金融严监管防风险依然是主旋律。中粮资本要认真贯彻落实国家和集团相关工作要求，坚持稳健经营发展，强化机制体系流程建设，提升核心竞争力和价值创造水平，持续推动公司高质量发展。
激情与汗水铸造过去，理性和坚强方可成就未来，新的一年，让我们携手奋进，为公司的事业发展，为每位员工的梦想与激情努力拼搏、贡献力量。
最后，祝各位同事和家人新年快乐，阖家幸服，身体健康，万事如意！
谢谢大家！
''' ]
    error_sentences = error_sentences[0].split('，')
    m = MacBertCorrector()
    for line in error_sentences:
        correct_sent, err = m.macbert_correct(line)
        print("query:{} => {} err:{}".format(line, correct_sent, err))
