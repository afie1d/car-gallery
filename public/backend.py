from flask import Flask, request, jsonify
import numpy as np
from scipy.optimize import linprog
import pandas as pd

app = Flask(__name__)

# Simulated data - you will use your backend search script to replace this
car_reviews = [
    {"name": "Tesla Model 3", "review": "Excellent electric vehicle with top-notch features."},
    {"name": "Ford Mustang", "review": "Powerful engine with a classic design."},
    {"name": "Honda Accord", "review": "Reliable sedan with great fuel economy."}
]

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    keywords = data.get('keywords', '').lower()

    # Filter cars based on the input keywords (you'll likely have your own search logic)
    results = [car for car in car_reviews if keywords in car['name'].lower() or keywords in car['review'].lower()]

    return jsonify(results)

# TODO: implement
def word_to_embedding(word, embeddings):
    return

def preprocess_text(t):
    t = t.lower().split()
    return [w.strip(".,!;:'") for w in t]

def get_bow(text, vocab):
    # create bag-of-words representation of text given a vocabulary
    bow = np.zeros(len(vocab))
    for word in text:
        if word in vocab:
            bow[vocab.index(word)] += 1
    
    # normalize
    bow /= np.sum(bow)
    return bow

def compute_distance_matrix(vocab, embeddings):
    # compute pairwaise distance matrix between words in vocabulary
    vocab_size = len(vocab)
    D = np.zeros((vocab_size, vocab_size))

    for i, w1 in enumerate(vocab):
        for j, w2 in enumerate(vocab):
            e1 = word_to_embedding(w1)
            e2 = word_to_embedding(w2)
            D[i, j] = np.dot(e1, e2)

    return D

def wmd(doc1, doc2, embeddings):
    doc1_tkns = preprocess_text(doc1)
    doc2_tkns = preprocess_text(doc2)

    vocab = list(set(doc1_tkns, doc2_tkns))
    bow1 = get_bow(doc1_tkns, vocab)
    bow2 = get_bow(doc2_tkns, vocab)

    D = compute_distance_matrix(vocab, embeddings)
    D = D.flatten()

    # constraints
    vocab_size = len(vocab)
    A_eq = np.zeros((2 * vocab_size, vocab_size ** 2))
    b_eq = np.conacatenate([bow1, bow2])

    # ensure row sums match bow1
    for i in range(vocab_size):
        A_eq[i, i * vocab_size:(i + 1) * vocab_size] = 1

    # ensure column sums match bow2
    for j in range(vocab_size):
        A_eq[vocab_size + j, j::vocab_size] = 1

    result = linprog(D, A_eq=A_eq, b_eq=b_eq, bounds=(0, None), method='highs')
    return result.fun

if __name__ == '__main__':
    app.run(debug=True)
