import pandas as pd
from harvesttext import HarvestText
import re
import opencc  # 导入 OpenCC 库

ht = HarvestText()

# 初始化 OpenCC 转换器
cc = opencc.OpenCC('t2s.json')  # t2s.json 用于繁体转简体


# 数据清洗函数
def clearData(content=''):
    content = cc.convert(content)  # 繁体转简体
    content = ht.clean_text(content, emoji=False)  # 过滤@后字符

    # 合并正则表达式，去除网站链接和#号之间的内容
    content = re.sub(r'(https?://[^\s]+|#.*?#)', '', content)

    # 去除《》符号
    content = content.replace('《', '').replace('》', '')

    return content


# 读取 CSV 文件并处理
def process_csv(input_file, output_file, text_column):
    # 读取 CSV 文件
    df = pd.read_csv(input_file)

    # 检查是否存在指定的文本列
    if text_column not in df.columns:
        raise ValueError(f"CSV 文件中没有找到列: {text_column}")

    # 对指定列的数据进行清洗
    df[text_column] = df[text_column].apply(clearData)

    # 将清洗后的数据保存为新的 CSV 文件
    df.to_csv(output_file, index=False)

    print(f"处理后的数据已保存到 {output_file}")


# 使用例
input_file = './data/input.csv'  # 输入文件路径
output_file = './data/output.csv'  # 输出文件路径
text_column = 'text'  # 假设 CSV 文件中包含一个名为 'text' 的列需要清洗

process_csv(input_file, output_file, text_column)
