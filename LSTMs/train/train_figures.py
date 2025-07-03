import codecs
import jieba
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Embedding, Conv1D, GlobalMaxPooling1D, MaxPooling1D, LSTM
from tensorflow.keras.layers import Bidirectional
from tensorflow.keras import backend as K
from tensorflow.keras.metrics import Precision, Recall
import matplotlib.pyplot as plt


# 数据路径
datapaths = r"D:\cnn_lstm\data\data_train\\"
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
with codecs.open(r"D:\cnn_lstm\vocabulary.txt", "w", "utf-8") as f:
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
    # LSTM(lstm_output_size),
    Bidirectional(LSTM(lstm_output_size)),  # Use BiLSTM
    Dense(num_classes),
    Activation("sigmoid")
])

model.compile(loss="categorical_crossentropy", optimizer="adam",  metrics=['accuracy', Precision(), Recall()])

print("Train ....................")

# 训练模型并保存训练过程信息
history = model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.2)

# 使用历史记录计算 F1 分数
precision = np.array(history.history['precision'])
recall = np.array(history.history['recall'])
val_precision = np.array(history.history['val_precision'])
val_recall = np.array(history.history['val_recall'])

# 计算训练和验证集上的 F1 分数
f1_score = 2 * (precision * recall) / (precision + recall + K.epsilon())
val_f1_score = 2 * (val_precision * val_recall) / (val_precision + val_recall + K.epsilon())

# 绘制训练和验证的损失曲线
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

# 保存图像
plt.savefig(r"D:\cnn_lstm\loss_plot.png")  # 保存为指定路径和文件名
plt.show()  # 显示图像

# 绘制训练和验证的准确率、精确率、召回率和 F1 分数曲线
plt.figure(figsize=(14, 10))

# 准确率
plt.subplot(2, 2, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

# 精确率
plt.subplot(2, 2, 2)
plt.plot(history.history['precision'], label='Training Precision')
plt.plot(history.history['val_precision'], label='Validation Precision')
plt.title('Model Precision')
plt.xlabel('Epoch')
plt.ylabel('Precision')
plt.legend()

# 召回率
plt.subplot(2, 2, 3)
plt.plot(history.history['recall'], label='Training Recall')
plt.plot(history.history['val_recall'], label='Validation Recall')
plt.title('Model Recall')
plt.xlabel('Epoch')
plt.ylabel('Recall')
plt.legend()

# F1 分数
plt.subplot(2, 2, 4)
plt.plot(f1_score, label='Training F1 Score')
plt.plot(val_f1_score, label='Validation F1 Score')
plt.title('Model F1 Score')
plt.xlabel('Epoch')
plt.ylabel('F1 Score')
plt.legend()

# 保存和显示图像
plt.tight_layout()
plt.savefig(r"D:\cnn_lstm\training_metrics.png")  # 保存图片
plt.show()

# 评估模型
score, acc, precision, recall = model.evaluate(x_test, y_test, batch_size=batch_size)
print(f"预测得分(损失): {score}")
print(f"预测准确率: {acc}")
print(f"预测查准率: {precision}")
print(f"预测查全率: {recall}")
print(f"预测F1得分: {2 * (precision * recall) / (precision + recall + K.epsilon())}")

# 预测结果
predictions = model.predict(x_test)
print("测试集的预测结果")
print(predictions)

# 获取预测类别
predict_class = np.argmax(predictions, axis=1)
print("测试集的预测类别")
print(predict_class)
