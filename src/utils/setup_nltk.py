import nltk

def download_nltk_data():
    print("Downloading NLTK data...")
    nltk.download('punkt')
    nltk.download('punkt_tab')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    print("Done.")

if __name__ == "__main__":
    download_nltk_data()
