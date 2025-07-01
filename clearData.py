from harvesttext import HarvestText
import re
from pyhanlp import JClass  # 导入 HanLP 类

ht = HarvestText()

# 初始化 CharTable 用于繁体字转简体
CharTable = JClass('com.hankcs.hanlp.dictionary.other.CharTable')

def clearData(content=''):
    content = CharTable.convert(content)  # 繁体转简体
    content = ht.clean_text(content, emoji=False)  # 过滤@后字符

    # 合并正则表达式，去除网站链接和#号之间的内容
    content = re.sub(r'(https?://[^\s]+|#.*?#)', '', content)

    # 去除《》符号
    content = content.replace('《', '').replace('》', '')

    return content

