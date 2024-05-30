import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
from DataNormalizer import DataNormalizer

vocab_size = 14000

model = keras.Sequential()
model.add(keras.layers.Embedding(vocab_size, 16))
model.add(keras.layers.GlobalAveragePooling1D())
model.add(keras.layers.Dense(16, activation=tf.nn.relu))
model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))

model.summary()

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['acc'])

data_normalizer = DataNormalizer('C:/Users/Admin TI/Downloads/rotten_tomatoes_critic_reviews_p.csv')
X, y = data_normalizer.prepare_data()

# Asegúrate de que todos los valores en X estén en el rango [0, vocab_size-1]
X = np.clip(X, 0, vocab_size - 1)

print(X[0])
print(len(X))
x_val = X[:14000]
partial_x_train = X[14000:]
print(len(y))
y_val = y[:14000]
partial_y_train = y[14000:]

print(x_val[0])
print(x_val)
print(y_val[0])
print(y_val)

print(len(x_val))
print(len(y_val))
print(len(partial_x_train))
print(len(partial_y_train))

history = model.fit(partial_x_train,
                    partial_y_train,
                    epochs=30,
                    batch_size=512,
                    validation_data=(x_val, y_val),
                    verbose=1)
