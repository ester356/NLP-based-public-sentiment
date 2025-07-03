import codecs
import jieba
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# 加载分词器和词汇表
vocab_path = r"E:\cnn_lstm\vocabulary.txt"
vocab_dict = {}
with codecs.open(vocab_path, "r", "utf-8") as f:
    for line in f:
        # 去掉空白字符并按空格分割
        parts = line.strip().split()
        if len(parts) == 2:  # 只处理包含两个元素的行
            word, index = parts
            vocab_dict[word] = int(index)
        else:
            print(f"跳过格式不正确的行: {line}")

# 加载并预处理 data.csv 数据
data_path = r"D:\cnn_lstm\train\data_test.csv"
df = pd.read_csv(data_path)

# 分词和数值化
texts = [" ".join(jieba.lcut(text.strip(), cut_all=False)) for text in df['text']]
labels = df['label'].values

# 加载分词器
tokenizer = Tokenizer()
tokenizer.word_index = vocab_dict  # 使用之前保存的词汇表
sequences = tokenizer.texts_to_sequences(texts)
max_document_length = 200
x_new = pad_sequences(sequences, maxlen=max_document_length, padding='post')

# 将标签转为 one-hot 编码
y_new = np.zeros((len(labels), 3))
for idx, label in enumerate(labels):
    y_new[idx, label] = 1

# 加载保存的模型
model_path = r"D:\cnn_lstm\models\cnn_bilstm.h5"
model = load_model(model_path)
model.summary()

# 预测结果
predictions = model.predict(x_new)
predict_class = np.argmax(predictions, axis=1)

# 计算评价指标
y_true = np.argmax(y_new, axis=1)
accuracy = accuracy_score(y_true, predict_class)
precision = precision_score(y_true, predict_class, average='macro')
recall = recall_score(y_true, predict_class, average='macro')
f1 = f1_score(y_true, predict_class, average='macro')

print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-Score: {f1:.4f}")
