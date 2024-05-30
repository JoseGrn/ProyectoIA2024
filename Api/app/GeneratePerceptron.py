import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
from DataNormalizer import DataNormalizer

vocab_size = 38000

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
x_val = X[:38000]
partial_x_train = X[38000:]
print(len(y))
y_val = y[:38000]
partial_y_train = y[38000:]

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
                    epochs=20,
                    batch_size=512,
                    validation_data=(x_val, y_val),
                    verbose=1)


# Función para predecir la validez de un nuevo comentario
def predict_review(review_text):
    review_vector = data_normalizer.preprocess_single_review(review_text)
    prediction = model.predict(review_vector)
    return 'FRESH' if prediction < 0.5 else 'ROTTEN'

# Ejemplo de uso
nuevo_review = "This movie was absolutely fantastic! I loved every moment of it."
print(predict_review(nuevo_review))

review_1 = "The plot was quite boring and the characters were not well-developed."
print(predict_review(review_1))

review_2 = "An excellent film with stunning visuals and a captivating storyline."
print(predict_review(review_2))

review_3 = "It was a waste of time. I wouldn't recommend it to anyone."
print(predict_review(review_3))

review_4 = "A masterpiece! The director did an incredible job with this movie."
print(predict_review(review_4))

review_5 = "The movie had some good moments, but overall it fell short of expectations."
print(predict_review(review_5))