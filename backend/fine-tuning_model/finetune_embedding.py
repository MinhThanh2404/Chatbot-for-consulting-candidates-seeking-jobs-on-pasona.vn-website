import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from gensim.models import Word2Vec
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
import torch
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split

# Sample data
topic_train_data = pd.read_excel('new3_clean_training_data.xlsx', sheet_name="Sheet1")

# Step 1: Preprocess with n-grams and word2vec
corpus = topic_train_data['clean_text'].tolist()
vectorizer = CountVectorizer(ngram_range=(1, 2))
X = vectorizer.fit_transform(corpus)

# Train Word2Vec on the corpus
word2vec_model = Word2Vec([doc.split() for doc in corpus], vector_size=100, window=5, min_count=1, sg=0)

# Create an embedding layer with Word2Vec embeddings
embedding_matrix = np.zeros((len(vectorizer.get_feature_names_out()), 100))
for i, word in enumerate(vectorizer.get_feature_names_out()):
    if word in word2vec_model.wv:
        embedding_matrix[i] = word2vec_model.wv[word]

# Step 2: Load BERT model and tokenizer
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2)

# Step 3: Combine with BERT
bert_embeddings = []
for text in corpus:
    inputs = tokenizer(text, return_tensors="pt", padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
        bert_embeddings.append(embeddings)

combined_embeddings = np.concatenate([X.toarray(), bert_embeddings, embedding_matrix], axis=1)

# Step 4: Fine-tuning
X_train, X_val, y_train, y_val = train_test_split(combined_embeddings, topic_train_data['label'].tolist(), test_size=0.2)
train_dataset = TensorDataset(torch.tensor(X_train), torch.tensor(y_train))
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

optimizer = AdamW(model.parameters(), lr=1e-5)
criterion = torch.nn.CrossEntropyLoss()

for epoch in range(5):
    model.train()
    for inputs, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs, labels=labels)
        loss = criterion(outputs.logits, labels)
        loss.backward()
        optimizer.step()

# Evaluation
model.eval()
# Evaluate on validation set...

# Save the model
model.save_pretrained('combined_bert_model')
