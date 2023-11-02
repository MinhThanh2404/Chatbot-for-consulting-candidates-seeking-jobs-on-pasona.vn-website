#import libraries
import spacy
import spacy.cli
from nltk.corpus import wordnet
from transformers import BertForSequenceClassification, BertTokenizer
import torch
from torch.utils.data import DataLoader, TensorDataset


class Topic():
    def get_word_synonyms_from_sent(word, sent):
        for synset in wordnet.synsets(word):
            if "come" in synset.lemma_names():
                synset.lemma_names().pop(synset.lemma_names().index('come'))
            for lemma in synset.lemma_names():
                if lemma in sent:
                    sent = sent.replace(lemma, word)
                    # word_synonyms.append(lemma)]
                    return {"topic":word, "sent":sent}
        return {"topic":"", "sent":sent}
        
    def topic_identifier(class_dict, input_sent):
        """
        - label the string with its relevant topic
        - params:
            + new_input_text (list): new training data (object) ["New sentence 1.", "New sentence 2.", ...]
            + new_label_data (list): new training data (label) [0, 1, ...] (match the postion with the input text)
            + class_dict (dict): dict of labels/topics
            + input_sent (str): what to label
        - return: label (str)
        """
        #use wordnet.synsets to find the topic
        predicted_topic = ""
        for i in list(class_dict.values()):
            if Topic.get_word_synonyms_from_sent(i, input_sent)['topic'] != "":
                predicted_topic = Topic.get_word_synonyms_from_sent(i, input_sent)['topic']
                input_sent = Topic.get_word_synonyms_from_sent(i, input_sent)['sent']
                break

        if predicted_topic == "":
            #if the result returns null, try BERT
            model = BertForSequenceClassification.from_pretrained('bert-base-uncased',num_labels=len(list(class_dict.keys())), from_tf=True)
            model.load_state_dict(torch.load('fine-tune-topic-model.pth'))
            model.eval()
            tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

            # input_text = "Can you give me an idea of the average compensation for software managers in HCM?"
            encoded_input = tokenizer.encode_plus(input_sent, add_special_tokens=True, return_tensors='pt')
            # output = model(**encoded_input)
            # Perform topic classification
            with torch.no_grad():
                outputs = model(**encoded_input)

            # Get the predicted label (topic)
            predicted_label = torch.argmax(outputs.logits).item()

            # Get the topic based on the predicted label
            predicted_topic = class_dict[predicted_label]

        return {'topic':predicted_topic.strip(), 'label_sent': input_sent}

