import codecs
import jieba
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer

# 加载原始词汇表
vocab_path = r"D:\cnn_lstm\vocabulary.txt"
vocab_dict = {}
with codecs.open(vocab_path, "r", "utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 2:
            word, index = parts
            vocab_dict[word] = int(index)

# 读取新的数据集并分词
data_path = r"E:\cnn_lstm\data\data.csv"
df = pd.read_csv(data_path)
new_texts = [" ".join(jieba.lcut(text.strip(), cut_all=False)) for text in df['text']]

# 使用现有词汇表并添加新词
tokenizer = Tokenizer()
tokenizer.word_index = vocab_dict  # 加载已有词汇表
tokenizer.fit_on_texts(new_texts)  # 在新文本上进行拟合，以添加新词汇

# 更新后的词汇表
updated_vocab_dict = tokenizer.word_index

# 保存更新后的词汇表
with codecs.open(vocab_path, "w", "utf-8") as f:
    for word, index in updated_vocab_dict.items():
        f.write(f"{word} {index}\n")

print("词汇表已更新并保存。")
