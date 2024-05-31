import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
from DataNormalizer import DataNormalizer


class SentimentModel:
    def __init__(self, vocab_size):
        self.vocab_legth = vocab_size
        self.model = keras.Sequential()
        self.data_normalizer = None

    def train(self, review_file):

        vocab_size = self.vocab_legth
        self.model.add(keras.layers.Embedding(vocab_size, 16))
        self.model.add(keras.layers.GlobalAveragePooling1D())
        self.model.add(keras.layers.Dense(16, activation=tf.nn.relu))
        self.model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))
        self.model.summary()
        self.model.compile(optimizer='adam',
                    loss='binary_crossentropy',
                    metrics=['acc'])
        self.data_normalizer = DataNormalizer(review_file)
        X, y = self.data_normalizer.prepare_data()

        X = np.clip(X, 0, vocab_size - 1)

        x_val = X[:vocab_size]
        partial_x_train = X[vocab_size:]
        y_val = y[:vocab_size]
        partial_y_train = y[vocab_size:]

        history = self.model.fit(partial_x_train,
                            partial_y_train,
                            epochs=20,
                            batch_size=512,
                            validation_data=(x_val, y_val),
                            verbose=1)
        return history

    def predict_review(self, review_text):
        if not self.data_normalizer:
            raise ValueError("The model must be trained before making predictions.")
        review_vector = self.data_normalizer.preprocess_single_review(review_text)
        prediction = self.model.predict(review_vector)
        return 'FRESH' if prediction < 0.5 else 'ROTTEN'


# Uso de la clase SentimentModel
sentiment_model = SentimentModel(38000)
history = sentiment_model.train('C:/Users/Admin TI/Downloads/rotten_tomatoes_critic_reviews_p.csv')

# Ejemplo de uso
nuevo_review = "This movie was absolutely fantastic! I loved every moment of it."
print(sentiment_model.predict_review(nuevo_review))

review_1 = "The plot was quite boring and the characters were not well-developed."
print(sentiment_model.predict_review(review_1))

review_2 = "An excellent film with stunning visuals and a captivating storyline."
print(sentiment_model.predict_review(review_2))

review_3 = "It was a waste of time. I wouldn't recommend it to anyone."
print(sentiment_model.predict_review(review_3))

review_4 = "A masterpiece! The director did an incredible job with this movie."
print(sentiment_model.predict_review(review_4))

review_5 = "The movie had some good moments, but overall it fell short of expectations."
print(sentiment_model.predict_review(review_5))