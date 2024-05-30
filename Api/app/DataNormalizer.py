import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
import nltk

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')


def clean_review_score(value):
    try:
        if isinstance(value, str):
            if '/' in value:
                num, denom = value.split('/')
                denom_value = float(denom)
                if denom_value > 0:
                    return float(num) / denom_value
                else:
                    return 0
            elif re.match(r'^[A-F]$', value, re.IGNORECASE):
                return letter_grade_to_numeric(value)
            else:
                return float(value)
        return float(value)
    except ValueError:
        return np.nan


def letter_grade_to_numeric(grade):
    grade = grade.upper()
    mapping = {
        'A': 4.0,
        'B': 3.0,
        'C': 2.0,
        'D': 1.0,
        'F': 0.0
    }
    return mapping.get(grade, np.nan)


def fill_missing_values(df, column, fill_value):
    df[column] = df[column].fillna(fill_value)
    return df


class dataNormalizer:
    def _init_(self, review_file):
        self.review_file = review_file
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.numerical_columns = ['review_score']
        self.categorical_columns = ['review_type', 'critic_name']

    def load_and_clean_reviews_data(self):
        reviews_df = pd.read_csv(self.review_file)
        reviews_df = self.clean_reviews_data(reviews_df)
        return reviews_df

    def clean_reviews_data(self, df):
        df = fill_missing_values(df, 'critic_name', 'Unknown Critic')
        df['review_score'] = df['review_score'].apply(clean_review_score)
        df['review_score'] = df['review_score'].fillna(df['review_score'].mean())
        return df

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
        stop_words = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()

        df['review_content'] = df['review_content'].apply(lambda x: self.clean_text(x, stop_words, lemmatizer))

        comentarios_preprocesados = [self.clean_text(comentario, stop_words, lemmatizer) for comentario in df['review_content'].astype(str)]

        # Construir vocabulario
        vocabulario = {word for comentario in comentarios_preprocesados for word in comentario.split()}
        vocabulario = {word: idx for idx, word in enumerate(vocabulario)}

        # Convertir comentarios a números
        def text_to_numbers(comentario, vocabulario):
            return [vocabulario[word] for word in comentario.split() if word in vocabulario]

        comentarios_numericos = [text_to_numbers(comentario, vocabulario) for comentario in comentarios_preprocesados]

        # Convertir a vectores de longitud fija (por ejemplo, con padding o truncamiento)
        max_length = max(len(comentario) for comentario in comentarios_numericos)
        comentarios_vectores = np.zeros((len(comentarios_numericos), max_length))

        for i, comentario in enumerate(comentarios_numericos):
            length = min(len(comentario), max_length)
            comentarios_vectores[i, :length] = comentario[:length]

        # Escalar los datos
        comentarios_vectores_escalados = self.scaler.fit_transform(comentarios_vectores)

        return df, comentarios_vectores_escalados

    def clean_text(self, text, stop_words, lemmatizer):
        if isinstance(text, str):
            tokens = word_tokenize(text)
            tokens = [word.lower() for word in tokens if word.isalpha()]
            tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
            clean_text = ' '.join(tokens)
            return clean_text
        else:
            return ''

    def prepare_data(self):
        df = self.load_and_clean_reviews_data()
        df = self.encode_categorical(df)
        df = self.normalize_numerical(df)
        df, review_sequences = self.preprocess_reviews(df)

        X = review_sequences  # Ahora X será solo las secuencias de texto convertidas a números
        y = df['review_type'].values
        return X, y


# class Perceptron:
#     def _init_(self, input_size, learning_rate=0.1, epochs=100):
#         self.weights = np.zeros(input_size + 1)
#         self.learning_rate = learning_rate
#         self.epochs = epochs

#     def activation_function(self, x):
#         return 1 if x >= 0 else 0

#     def predict(self, inputs):
#         summation = np.dot(inputs, self.weights[1:]) + self.weights[0]
#         return self.activation_function(summation)

#     def train(self, training_inputs, labels):
#         for _ in range(self.epochs):
#             for inputs, label in zip(training_inputs, labels):
#                 prediction = self.predict(inputs)
#                 self.weights[1:] += self.learning_rate * (label - prediction) * inputs
#                 self.weights[0] += self.learning_rate * (label - prediction)


# Instancia y uso de la clase DataNormalizer
# data_normalizer = DataNormalizer('C:/Users/Admin TI/Downloads/rotten_tomatoes_critic_reviews_p.csv')
# X, y = data_normalizer.prepare_data()

# print(X)
# print(y)

# # Crear y entrenar el perceptrón
# input_size = X.shape[1]
# perceptron = Perceptron(input_size)
# perceptron.train(X, y)

# # Probar el perceptrón con algunos ejemplos
# test_inputs = np.array([X[0], X[1]])  # Usa algunos datos de prueba
# print("Predicciones:", [perceptron.predict(x) for x in test_inputs])