import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
from DataNormalizer import dataNormalizer



vocab_size = 460000

model = keras.Sequential()
model.add(keras.layers.Embedding(vocab_size, 16))
model.add(keras.layers.GlobalAveragePooling1D())
model.add(keras.layers.Dense(16, activation=tf.nn.relu))
model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))

model.summary()

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['acc'])

data_normalizer = dataNormalizer()
data_normalizer._init_('C:/Users/josed/Downloads/rotten_tomatoes_critic_reviews.csv')
X, y = data_normalizer.prepare_data()

print(len(X))
x_val = X[:460000]
partial_x_train = X[460000:]
print(len(y))
y_val = y[:460000]
partial_y_train = y[460000:]

print(x_val[0])
print(x_val)
print(y_val[0])
print(y_val)

# x_val = x_val.astype(np.float32)
# partial_x_train = partial_x_train.astype(np.float32)

# y_val = y_val.astype(np.float32)
# partial_y_train = partial_y_train.astype(np.float32)

print(len(x_val))
print(len(y_val))
print(len(partial_x_train))
print(len(partial_y_train))

history = model.fit(partial_x_train,
                    partial_y_train,
                    epochs=20,
                    batch_size=512,
                    validation_data=(x_val, y_val),
                    verbose=1)

# results = model.evaluate(test_data, test_labels)

# print(results)

# history_dict = history.history
# history_dict.keys()

# acc = history_dict['acc']
# val_acc = history_dict['val_acc']
# loss = history_dict['loss']
# val_loss = history_dict['val_loss']

# epochs = range(1, len(acc) + 1)

# # "bo" is for "blue dot"
# plt.plot(epochs, loss, 'bo', label='Training loss')
# # b is for "solid blue line"
# plt.plot(epochs, val_loss, 'b', label='Validation loss')
# plt.title('Training and validation loss')
# plt.xlabel('Epochs')
# plt.ylabel('Loss')
# plt.legend()

# plt.show()

# plt.clf()   # clear figure

# plt.plot(epochs, acc, 'bo', label='Training acc')
# plt.plot(epochs, val_acc, 'b', label='Validation acc')
# plt.title('Training and validation accuracy')
# plt.xlabel('Epochs')
# plt.ylabel('Accuracy')
# plt.legend()

# plt.show()