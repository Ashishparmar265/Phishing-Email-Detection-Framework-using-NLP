import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import joblib

from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping

class PhishingLSTM:
    def __init__(self, max_words=10000, max_len=100, embedding_dim=128):
        self.max_words = max_words
        self.max_len = max_len
        self.embedding_dim = embedding_dim
        self.tokenizer = Tokenizer(num_words=max_words)
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential([
            Embedding(self.max_words, self.embedding_dim, input_length=self.max_len),
            Bidirectional(LSTM(64, return_sequences=True)),
            Dropout(0.3),
            BatchNormalization(),
            Bidirectional(LSTM(32)),
            Dropout(0.3),
            BatchNormalization(),
            Dense(64, activation='relu'),
            Dropout(0.5),
            Dense(1, activation='sigmoid')
        ])
        # Using a slightly lower learning rate for better calibration
        optimizer = tf.keras.optimizers.Adam(learning_rate=0.0005)
        model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
        return model

    def fit(self, texts, labels, epochs=10, batch_size=32, validation_split=0.2):
        self.tokenizer.fit_on_texts(texts)
        sequences = self.tokenizer.texts_to_sequences(texts)
        X = pad_sequences(sequences, maxlen=self.max_len)
        y = np.array(labels)
        
        # Early stopping to prevent overfitting
        early_stop = EarlyStopping(
            monitor='val_loss', 
            patience=3, 
            restore_best_weights=True,
            verbose=1
        )
        
        return self.model.fit(
            X, y, 
            epochs=epochs, 
            batch_size=batch_size, 
            validation_split=validation_split,
            callbacks=[early_stop]
        )

    def predict(self, texts):
        sequences = self.tokenizer.texts_to_sequences(texts)
        X = pad_sequences(sequences, maxlen=self.max_len)
        return self.model.predict(X)

    def save(self, path="models/lstm_phishing"):
        self.model.save(f"{path}.h5")
        with open(f"{path}_tokenizer.pkl", "wb") as f:
            joblib.dump(self.tokenizer, f)

if __name__ == "__main__":
    # Example usage with dummy data
    texts = ["Urgent verify your account", "Meeting tomorrow morning", "Click here for free prize", "The report is attached"]
    labels = [1, 0, 1, 0]
    
    lstm = PhishingLSTM()
    lstm.fit(texts, labels, epochs=2)
    print("LSTM Model training example complete.")
