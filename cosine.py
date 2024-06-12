# Step 1: Install necessary packages (if not already installed)
# !pip install nltk
# !pip install gensim
# !pip install numpy

# Step 2: Import and download NLTK data (if not already done)
import nltk
nltk.download('punkt')

# Step 3: Import necessary libraries
import gensim.downloader as api
import numpy as np
from numpy.linalg import norm

# Load the pre-trained word vectors
model = api.load('word2vec-google-news-300')

# Define a function to compute the average vector for a sentence
def sentence_vector(sentence, model):
    tokens = nltk.word_tokenize(sentence)
    valid_vectors = [model[word] for word in tokens if word in model]
    if not valid_vectors:
        return np.zeros(model.vector_size)  # Return a zero vector if no valid words are found
    return np.mean(valid_vectors, axis=0)

# Step 4: Define the sentences
sentence1 = "This is an example sentence."
sentence2 = "This is another example."

# Step 5: Compute the sentence vectors
vector1 = sentence_vector(sentence1, model)
vector2 = sentence_vector(sentence2, model)

# Step 6: Calculate the cosine similarity between the two sentence vectors
cosine_similarity = np.dot(vector1, vector2) / (norm(vector1) * norm(vector2))

print(f"Cosine similarity between the sentences: {cosine_similarity}")
