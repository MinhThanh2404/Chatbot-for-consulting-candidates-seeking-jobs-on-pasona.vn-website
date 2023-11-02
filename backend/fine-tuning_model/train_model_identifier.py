"""
- Usage: identify the main topic of the cleaned message
- Structure:
    + Class UpdatePretrainedModel(), def train_and_save_model(): declare how the model will be fine-tuned; consider params and epoches
    + main: open only 1 section so as not to meet the conflict
        * to load and clean the raw training dataset, and save the cleaned data to a new file 
        ( because processing cleaning text is time-consuming, we will use this new file as the official training dataset): open from Prepare training dataset START to Prepare training dataset END
        *  to visualize the cleaned training dataset (identify abnormal pattern): open from Visualization... START to Visualization... END
        * to fine-tune the model and export the model file: open from fine-tuning model START to fine-tuning model END
        * to evaluate the model: open from Evaluate the model START to Evaluate the model END
        
"""


import torch
from transformers import BertForSequenceClassification, BertTokenizer
from torch.utils.data import DataLoader, TensorDataset
import pandas as pd
from services.process_text_service import raw_text_clean
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns


class UpdatePretrainedModel():

    def train_and_save_model(new_input_texts, new_labels, save_path, num_classes, batch_size=32, learning_rate=1e-5):
        # Load pre-trained BERT model and tokenizer
        model_name = 'bert-base-uncased'

        model = BertForSequenceClassification.from_pretrained(
            model_name, num_labels=num_classes)
        # # Load pre-trained weights into the modified model
        # model.load_state_dict(model.state_dict())
        tokenizer = BertTokenizer.from_pretrained(model_name)

        # Tokenize new input_texts
        new_tokenized_texts = [tokenizer.encode(
            text, add_special_tokens=True) for text in new_input_texts]

        max_length = 128  # Adjust this based on your model's input requirements
        new_tokenized_texts = [tokenizer.encode_plus(text, add_special_tokens=True, max_length=max_length, pad_to_max_length=True)[
            'input_ids'] for text in new_input_texts]

        # Convert to tensors and create a DataLoader
        new_input_ids = torch.tensor(new_tokenized_texts)
        new_labels = torch.tensor(new_labels)
        new_dataset = TensorDataset(new_input_ids, new_labels)
        new_dataloader = DataLoader(new_dataset, batch_size=32, shuffle=True)

        # Define loss function and optimizer
        criterion = torch.nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)

        # Initialize empty lists to store loss values
        losses = []
        # Fine-tuning loop with new data
        num_epochs = 201
        for epoch in range(num_epochs):
            running_loss = 0.0
            model.train()
            for batch_input_ids, batch_labels in new_dataloader:
                optimizer.zero_grad()
                outputs = model(input_ids=batch_input_ids, labels=batch_labels)
                loss = outputs.loss
                loss.backward()
                optimizer.step()

                # store loss value
                running_loss += loss.item()

                # Calculate average loss for the epoch
                if epoch % 50 == 0:
                    epoch_loss = running_loss / len(new_dataloader)
                    losses.append(epoch_loss)
                    # Print and visualize the loss for each epoch
                    print(f"Epoch [{epoch}/{num_epochs}] Loss: {epoch_loss}")

        # # Visualize the loss
        # plt.figure(figsize=(12, 6))

        # # Loss plot
        # plt.subplot(1, 2, 1)
        # plt.plot(losses, label='Training Loss')
        # plt.xlabel('Epochs')
        # plt.ylabel('Loss')
        # plt.title('Loss Over Time')
        # plt.legend()

        # plt.tight_layout()
        # plt.show()

        # Save the model using torch.save()
        torch.save(model.state_dict(), save_path)

        return save_path


# Prepare training dataset START

    # data preprocessing START
# # import raw training dataset
# topic_train_data = pd.read_excel('new3_clean_training_data.xlsx', sheet_name="Sheet1")
# print(topic_train_data)
# topic_train_data['clean_text'] = topic_train_data['question'].apply(lambda x: raw_text_clean.clean_data(x)['clean_text'])
# topic_train_data['clean_text'].fillna('none', inplace=True)
# #encode the label
# label_encoding = {'amount':0, "salary": 1, "trivia": 2}
# topic_train_data['label'] = topic_train_data['label'].map(label_encoding)

# excel_file_path = 'new2_clean_training_data.xlsx'
    # # Export the DataFrame to an Excel file
# topic_train_data.to_excel(excel_file_path, index=False)

    # data preprocessing END

# Prepare training dataset END


# Visualize - Generate the word cloud for specific class START

# # import cleaned training dataset (change excel file name)
# topic_train_data = pd.read_excel('new3_clean_training_data.xlsx', sheet_name="Sheet1")

# word_cloud_class = test_data[topic_train_data['label']==0]['clean_text']
# #modify the label to your desired label name

# wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(word_cloud_class))

# # Display the word cloud
# plt.figure(figsize=(10, 5))
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis('off')
# plt.show()

    # Visualization - Generate the word cloud for specific class END

#     # fine-tuning model START
# # import training dataset
# topic_train_data = pd.read_excel(
#     'new3_clean_training_data.xlsx', sheet_name="Sheet1")
# # change excel file name to the cleaned training dataset

# save_path = UpdatePretrainedModel.train_and_save_model(topic_train_data['clean_text'].tolist(
# ), topic_train_data['label'].tolist(), "fine-tuned-topic-model.pth", len(set(topic_train_data['label'].tolist())))
# # modify the model path file name

# # fine-tuning model END


# Evaluate the model START

# Load test dataset (change excel file name)
test_data = pd.read_excel('new3_clean_training_data.xlsx', sheet_name = "Sheet1")

model = BertForSequenceClassification.from_pretrained('bert-base-uncased',num_labels=len(set(test_data['label'].tolist())), from_tf=True)
model.load_state_dict(torch.load('fine-tune-topic-model.pth'))
model.eval()
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Tokenize and process text
input_texts = test_data['clean_text'].tolist()
encoded_inputs = tokenizer(input_texts, padding=True, truncation=True, return_tensors='pt')
input_ids = encoded_inputs['input_ids']
attention_mask = encoded_inputs['attention_mask']

# Get predictions
with torch.no_grad():
    outputs = model(input_ids, attention_mask=attention_mask)
    predicted_labels = torch.argmax(outputs.logits, dim=1).tolist()

# Add predicted labels to the DataFrame
test_data['predicted_label'] = predicted_labels

print(test_data)

#evaluation metrics
# Calculate accuracy
accuracy = accuracy_score(test_data['label'], test_data['predicted_label'])
print("Accuracy:", accuracy)

#confusion_matrix
def my_confusion_matrix(y_true, y_pred):
    N = np.unique(y_true).shape[0] # number of classes
    cm = np.zeros((N, N))
    for n in range(y_true.shape[0]):
        cm[y_true[n], y_pred[n]] += 1
    return cm

cnf_matrix = my_confusion_matrix(test_data['label'], test_data['predicted_label'])
print('Confusion matrix:')
print(cnf_matrix)

# Calculate Precision, Recall, and F1-Score for each class
precision_per_class = precision_score(test_data['label'], test_data['predicted_label'], average=None)
recall_per_class = recall_score(test_data['label'], test_data['predicted_label'], average=None)
f1_score_per_class = f1_score(test_data['label'], test_data['predicted_label'], average=None)

# Print the results
for class_label, precision, recall, f1 in zip(range(len(precision_per_class)), precision_per_class, recall_per_class, f1_score_per_class):
    print(f'Class {class_label}: Precision = {precision:.2f}, Recall = {recall:.2f}, F1-Score = {f1:.2f}')

# Calculate precision
precision = precision_score(test_data['label'], test_data['predicted_label'], average='macro')
print("Precision:", precision)

# Calculate recall
recall = recall_score(test_data['label'], test_data['predicted_label'], average='macro')
print("Recall:", recall)

# Evaluate the model END
