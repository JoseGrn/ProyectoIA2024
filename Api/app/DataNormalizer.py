import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

class DataNormalizer:
    def __init__(self, movie_file, review_file):
        self.movie_file = movie_file
        self.review_file = review_file
        self.label_encoders = {}
        self.scaler = MinMaxScaler()
        self.tokenizer = Tokenizer(num_words=5000)
        self.numerical_columns = ['runtime', 'tomatometer_rating', 'tomatometer_count', 'audience_rating', 'audience_count', 'tomatometer_top_critics_count', 'tomatometer_fresh_critics_count', 'tomatometer_rotten_critics_count', 'review_score']
        self.categorical_columns = ['movie_title', 'content_rating', 'genres', 'directors', 'authors', 'actors', 'publisher_name', 'review_type', 'critic_name']
        
    def load_and_merge_data(self):
        movies_df = pd.read_csv(self.movie_file)
        reviews_df = pd.read_csv(self.review_file)
        combined_df = pd.merge(movies_df, reviews_df, on='rotten_tomatoes_link')
        return combined_df

    def encode_categorical(self, df):
        for column in self.categorical_columns:
            le = LabelEncoder()
            df[column] = le.fit_transform(df[column].astype(str))
            self.label_encoders[column] = le
        return df

    def normalize_numerical(self, df):
        df[self.numerical_columns] = self.scaler.fit_transform(df[self.numerical_columns])
        return df

    def preprocess_reviews(self, df):
        self.tokenizer.fit_on_texts(df['review_content'].astype(str))
        sequences = self.tokenizer.texts_to_sequences(df['review_content'].astype(str))
        padded_sequences = pad_sequences(sequences, maxlen=256, padding='post')
        df['review_content'] = list(padded_sequences)
        return df

    def prepare_data(self):
        df = self.load_and_merge_data()
        df = self.encode_categorical(df)
        df = self.normalize_numerical(df)
        df = self.preprocess_reviews(df)
        X = df.drop(columns=['review_content']).values
        y = df['review_type'].values
        return X, y

class Perceptron:
    def __init__(self, input_size, learning_rate=0.1, epochs=100):
        self.weights = np.zeros(input_size + 1)
        self.learning_rate = learning_rate
        self.epochs = epochs

    def activation_function(self, x):
        return 1 if x >= 0 else 0

    def predict(self, inputs):
        summation = np.dot(inputs, self.weights[1:]) + self.weights[0]
        return self.activation_function(summation)

    def train(self, training_inputs, labels):
        for _ in range(self.epochs):
            for inputs, label in zip(training_inputs, labels):
                prediction = self.predict(inputs)
                self.weights[1:] += self.learning_rate * (label - prediction) * inputs
                self.weights[0] += self.learning_rate * (label - prediction)

# Uso de las clases
data_normalizer = DataNormalizer(
    'C:/Users/Admin TI/Downloads/rotten_tomatoes_movies.csv',
    'C:/Users/Admin TI/Downloads/rotten_tomatoes_critic_reviews.csv'
)
X, y = data_normalizer.prepare_data()

# Crear y entrenar el perceptrón
input_size = X.shape[1]
perceptron = Perceptron(input_size)
perceptron.train(X, y)

# Probar el perceptrón con algunos ejemplos
test_inputs = np.array([X[0], X[1]])  # Usa algunos datos de prueba
print("Predicciones:", [perceptron.predict(x) for x in test_inputs])
