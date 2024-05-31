import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
import nltk

nltk.download('omw-1.4')
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
    def __init__(self, review_file):
        self.review_file = review_file
        self.label_encoders = {}
        self.numerical_columns = ['review_score']
        self.categorical_columns = ['review_type', 'critic_name']
        self.vocabulario = {}
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

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

    def preprocess_reviews(self, df):
        df['review_content'] = df['review_content'].apply(lambda x: self.clean_text(x))

        comentarios_preprocesados = [self.clean_text(comentario) for comentario in df['review_content'].astype(str)]

        # Construir vocabulario
        vocabulario = {word for comentario in comentarios_preprocesados for word in comentario.split()}
        self.vocabulario = {word: idx for idx, word in enumerate(vocabulario)}

        # Convertir comentarios a números
        def text_to_numbers(comentario, vocabulario):
            return [vocabulario[word] for word in comentario.split() if word in vocabulario]

        comentarios_numericos = [text_to_numbers(comentario, self.vocabulario) for comentario in comentarios_preprocesados]

        # Convertir a vectores de longitud fija (por ejemplo, con padding o truncamiento)
        max_length = max(len(comentario) for comentario in comentarios_numericos)
        comentarios_vectores = np.zeros((len(comentarios_numericos), max_length), dtype=int)

        for i, comentario in enumerate(comentarios_numericos):
            length = min(len(comentario), max_length)
            comentarios_vectores[i, :length] = comentario[:length]

        return df, comentarios_vectores

    def clean_text(self, text):
        if isinstance(text, str):
            tokens = word_tokenize(text)
            tokens = [word.lower() for word in tokens if word.isalpha()]
            tokens = [self.lemmatizer.lemmatize(word) for word in tokens if word not in self.stop_words]
            clean_text = ' '.join(tokens)
            return clean_text
        else:
            return ''

    def prepare_data(self):
        df = self.load_and_clean_reviews_data()
        df = self.encode_categorical(df)
        df, review_sequences = self.preprocess_reviews(df)

        X = review_sequences  # Ahora X será solo las secuencias de texto convertidas a números
        y = df['review_type'].values
        return X, y

    def preprocess_single_review(self, review_text):
        clean_review = self.clean_text(review_text)
        review_numbers = [self.vocabulario.get(word, 0) for word in clean_review.split()]
        max_length = max(len(review_numbers), 256)
        review_vector = np.zeros((1, max_length), dtype=int)
        review_vector[0, :len(review_numbers)] = review_numbers[:max_length]
        return review_vector