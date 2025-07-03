import codecs
import jieba
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Embedding, Conv1D, GlobalMaxPooling1D, MaxPooling1D, LSTM
from tensorflow.keras.layers import Bidirectional


# 数据路径
datapaths = r"D:\cnn_lstm\data\train\\"
positive_data = []
y_positive = []
neutral_data = []
y_neutral = []
negative_data = []
y_negative = []

print("#------------------------------------------------------#")
print("加载数据集")
with codecs.open(datapaths + "pos.csv", "r", "utf-8") as f1, \
     codecs.open(datapaths + "neutral.csv", "r", "utf-8") as f2, \
     codecs.open(datapaths + "neg.csv", "r", "utf-8") as f3:
    for line in f1:
        positive_data.append(" ".join(i for i in jieba.lcut(line.strip(), cut_all=False)))
        y_positive.append([1, 0, 0])
    for line in f2:
        neutral_data.append(" ".join(i for i in jieba.lcut(line.strip(), cut_all=False)))
        y_neutral.append([0, 1, 0])
    for line in f3:
        negative_data.append(" ".join(i for i in jieba.lcut(line.strip(), cut_all=False)))
        y_negative.append([0, 0, 1])

print("positive data:{}".format(len(positive_data)))
print("neutral data:{}".format(len(neutral_data)))
print("negative data:{}".format(len(negative_data)))

# 文本数据准备
x_text = positive_data + neutral_data + negative_data
y_label = y_positive + y_neutral + y_negative
print("#------------------------------------------------------#")
print("\n")

# 使用Tokenizer代替VocabularyProcessor
max_document_length = 200
tokenizer = Tokenizer()
tokenizer.fit_on_texts(x_text)
x = tokenizer.texts_to_sequences(x_text)
x = pad_sequences(x, maxlen=max_document_length, padding='post')
vocab_dict = tokenizer.word_index

# 保存词汇表
with codecs.open(r"E:\cnn_lstm\vocabulary.txt", "w", "utf-8") as f:
    for word, index in vocab_dict.items():
        f.write(f"{word} {index}\n")

print("#----------------------------------------------------------#")
print("\n")

# 数据集混洗
print("数据混洗")
np.random.seed(10)
y = np.array(y_label)
shuffle_indices = np.random.permutation(np.arange(len(y)))
x_shuffled = x[shuffle_indices]
y_shuffled = y[shuffle_indices]

# 划分训练集和测试集
test_sample_percentage = 0.2
test_sample_index = -1 * int(test_sample_percentage * float(len(y)))
x_train, x_test = x_shuffled[:test_sample_index], x_shuffled[test_sample_index:]
y_train, y_test = y_shuffled[:test_sample_index], y_shuffled[test_sample_index:]

print("训练和测试集划分完成。")
print("#----------------------------------------------------------#")
print("\n")

# 读取预训练词向量
print("读取預训练词向量矩阵")
pretrainpath = r"E:\cnn_lstm\sgns.wiki.bigram\\"
embedding_index = {}

with codecs.open(pretrainpath + "sgns.wiki.bigram", "r", "utf-8") as f:
    line = f.readline()
    nwords = int(line.strip().split(" ")[0])
    ndims = int(line.strip().split(" ")[1])
    for line in f:
        values = line.split()
        words = values[0]
        coefs = np.asarray(values[1:], dtype="float32")
        embedding_index[words] = coefs

print(f"预训练模型中Token总数：{nwords} = {len(embedding_index)}")
print(f"预训练模型的维度：{ndims}")
print("#----------------------------------------------------------#")
print("\n")

# 构建embedding matrix
embedding_matrix = np.zeros((len(vocab_dict) + 1, ndims))
notfoundword = 0
for word, i in vocab_dict.items():
    embedding_vector = embedding_index.get(word)
    if embedding_vector is not None:
        embedding_matrix[i] = embedding_vector
    else:
        notfoundword += 1
        embedding_matrix[i] = np.random.uniform(-1, 1, size=ndims)

print(f"词汇表中未找到单词个数：{notfoundword}")
print("#----------------------------------------------------------#")
print("\n")

# 搭建模型结构
print("Build model .................")
print("Embedding layer --- CNN layer --- LSTM layer --- Dense layer")
batch_size = 64
lstm_output_size = 128
embedding_dims = ndims
filters = 250
kernel_size = 3
dropout = 0.5
num_classes = 3
epochs = 5

model = Sequential([
    Embedding(len(vocab_dict) + 1, embedding_dims, weights=[embedding_matrix],
              input_length=max_document_length, trainable=False),
    Dropout(dropout),
    Conv1D(filters, kernel_size, padding="valid", activation="relu", strides=1),
    MaxPooling1D(),
    Bidirectional(LSTM(lstm_output_size)),  # Use BiLSTM
    Dense(num_classes),
    Activation("sigmoid")
])

model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

print("Train ....................")
# 在模型训练时加入回调
model.fit(
    x_train, y_train,
    batch_size=batch_size,
    epochs=epochs,
    validation_split=0.2
)
# 评估模型
score, acc = model.evaluate(x_test, y_test, batch_size=batch_size)
print(f"预测得分: {score}")
print(f"预测准确率: {acc}")

# 预测结果
predictions = model.predict(x_test)
print("测试集的预测结果")
print(predictions)

# 获取预测类别
predict_class = np.argmax(predictions, axis=1)
print("测试集的预测类别")
print(predict_class)

# 保存模型
# model.save(r"E:\cnn_lstm\models\cnn_bilstm.h5")
# print("保存模型")

# 输出模型总结和配置
print("输出模型总结")
print(model.summary())
print("输出模型配置信息")
print(model.get_config())
