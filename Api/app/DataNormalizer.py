import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.impute import KNNImputer
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


class DataNormalizer:
    def __init__(self, movie_file, review_file):
        self.movie_file = movie_file
        self.review_file = review_file
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.tokenizer = Tokenizer(num_words=5000)
        self.numerical_columns = ['runtime', 'tomatometer_rating', 'tomatometer_count', 'audience_rating',
                                  'audience_count']
        self.categorical_columns = ['content_rating', 'genres', 'directors', 'authors', 'actors',
                                    'publisher_name', 'review_type', 'critic_name']

    def load_and_merge_data(self):
        movies_df = pd.read_csv(self.movie_file)
        movies_df = self.clean_movies_data(movies_df)
        reviews_df = pd.read_csv(self.review_file)
        reviews_df = self.clean_reviews_data(reviews_df)
        combined_df = pd.merge(movies_df, reviews_df, on='rotten_tomatoes_link')
        return combined_df

    def clean_movies_data(self, df):
        df.drop(['movie_info', 'critics_consensus', 'production_company', 'tomatometer_status',
                 'audience_status', 'tomatometer_top_critics_count', 'tomatometer_fresh_critics_count',
                 'tomatometer_rotten_critics_count'], axis=1, inplace=True)

        df['original_release_date'] = pd.to_datetime(df['original_release_date'], errors='coerce')
        df['streaming_release_date'] = pd.to_datetime(df['streaming_release_date'], errors='coerce')

        df['original_release_date'] = df['original_release_date'].apply(
            lambda x: x.toordinal() if pd.notnull(x) else np.nan)
        df['streaming_release_date'] = df['streaming_release_date'].apply(
            lambda x: x.toordinal() if pd.notnull(x) else np.nan)

        imputer = KNNImputer(n_neighbors=5)
        df[['runtime']] = imputer.fit_transform(df[['runtime']])

        return df

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

        self.tokenizer.fit_on_texts(df['review_content'].astype(str))
        sequences = self.tokenizer.texts_to_sequences(df['review_content'].astype(str))
        padded_sequences = pad_sequences(sequences, maxlen=256, padding='post')

        return df, padded_sequences

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
        df = self.load_and_merge_data()
        df = self.encode_categorical(df)
        df = self.normalize_numerical(df)
        df, review_sequences = self.preprocess_reviews(df)

        df.drop(columns=['movie_title', 'rotten_tomatoes_link'], inplace=True)

        X = df.drop(columns=['review_content']).values
        X = np.hstack((X, review_sequences))
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


data_normalizer = DataNormalizer(
    'C:/Users/Admin TI/Downloads/rotten_tomatoes_movies.csv',
    'C:/Users/Admin TI/Downloads/rotten_tomatoes_critic_reviews.csv'
)
X, y = data_normalizer.prepare_data()

print(X)
print(y)

# Crear y entrenar el perceptrón
# input_size = X.shape[1]
# perceptron = Perceptron(input_size)
# perceptron.train(X, y)

# Probar el perceptrón con algunos ejemplos
# test_inputs = np.array([X[0], X[1]])  # Usa algunos datos de prueba
# print("Predicciones:", [perceptron.predict(x) for x in test_inputs])
