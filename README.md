<h1>Chatbot for consulting candidates seeking jobs on pasona.vn website</h1>

<p>This chatbot is integrated on pasona.vn website to be an AI assistant answering the web visitors/ job seekers' job-related inquiries (salary, open positions...). The chatbot applies a fine-tuned BERT model to categorize the main topic of the message, and direct to specific response process based on each topic to interact with the database. This repository contains both the frontend and backend design: the frontend languages are HTML, CSS, Javascript; the backend ones are Python, SQL. For the message processing, many NLP techniques have been combined, and for topic classification issue, a fine-tuned BERT model is applied. The author will introduce how the chatbot operates, source code's structure, and some highlights in the backend process, focusing on NLP techniques and ML model. The full report is written in Vietnamese.</p>

<h2><b>Table of content:</b></h2>
<ol>
  <li>Workflow of the chatbot</li>
  <li>Source code summary</li>
</ol>

<ol>
<li><h2>Workflow of the chatbot</h2>
<div>
  <div align='center'>
    <p>
    <img src='https://github.com/MinhThanh2404/Chatbot-for-consulting-candidates-seeking-jobs-on-pasona.vn-website/assets/126949248/92d8d496-5306-4363-b0c9-6bde117f3051'/>
    </p>
    <p><i>chatbot icon appears on the website</i></p>
  </div>
  <p>
    When customers access the homepage of the Pasona.vn website, in the bottom right corner of the screen, the blinking Chatbot icon will appear. When customers click on the icon, the system will display a greeting and invite customers to fill out the contact information form. The system will proceed to verify and process the data: If the phone number and email already exist in the company's database, it will check and update other information with the stored information in the contact information data table if there's any difference between the form submission and the current data in database. Finally, the system retrieves the customer code and saves it to the local storage. If the phone number and email do not exist in the company's database, a new data row will be created, storing the contact information of the new customer. Then, the system retrieves the customer code and saves it to the local storage.
  </p>
  <div align='center'>
    <p>
      <img src='https://github.com/MinhThanh2404/Chatbot-for-consulting-candidates-seeking-jobs-on-pasona.vn-website/assets/126949248/ad5ce5f3-1ffb-41a0-bdf7-6c36482dc427'/>
    </p>
    <p>
      <i>contact form</i>
    </p>
  </div>

  <p>
    After filling out the contact information, the system will continue to display a form with a format similar to the Job Page, allowing the customer to enter job search criteria (not all fields are required). At this point, the system will call the "search job" API on the Job Page to perform the query and display the search results (in a mobile interface). Simultaneously, the system will store the job search information in the data repository (job_search_history table) (if the customer does not perform a search, no search history will be saved).<br/>
  </p>
  <div align='center'>
    <p>
      <img src='https://github.com/MinhThanh2404/Chatbot-for-consulting-candidates-seeking-jobs-on-pasona.vn-website/assets/126949248/29eacfa7-88c5-4c09-aa50-ca534d146433'/>
    </p>
    <p>
      <i>search job form</i>
    </p>
    <p>
      <img src='https://github.com/MinhThanh2404/Chatbot-for-consulting-candidates-seeking-jobs-on-pasona.vn-website/assets/126949248/5af79edc-1762-4668-869c-29393889d054'/>
    </p>
    <p>
      <i>search job result</i>
    </p>
  </div>
<p>
  Below the displayed search results, the system will ask the customer if they have any more questions and provide three options: <br/>
</p>
<div align='center'>
  <p>
    <img src='https://github.com/MinhThanh2404/Chatbot-for-consulting-candidates-seeking-jobs-on-pasona.vn-website/assets/126949248/ef6df962-3d01-4e1d-9be0-3c994fff3e15'/>
  </p>
  <p>
    <i>3 options</i>
  </p>
</div>
<ul>
  <li><b>"Search job"</b>: Continue searching for jobs using the available template. The system will display the job search template for the customer to enter search information.</li>
  <li><b>"Chat with chatbot"</b>: If the customer has other questions besides job searching, instead of interacting with customer service staff, the system will be the one to receive the question and provide an answer. When the customer selects this option, the system will open a message composition box and a send message button. The customer enters the message content into the message composition box, and the system will process the message, interact with the data repository, and return a response, as well as store the message content, message analysis, and response. After providing a response, the system will ask the customer if they have any more questions, along with three options.<br/>
    <div align='center'>
      <p>
        <img src='https://github.com/MinhThanh2404/Chatbot-for-consulting-candidates-seeking-jobs-on-pasona.vn-website/assets/126949248/171e06ea-1d52-4649-98b9-0ba5237c0f34'/>
      </p>
      <p>
        <i>the customer sends the question and system is in the procress</i>
      </p>
      <p>
        <img src='https://github.com/MinhThanh2404/Chatbot-for-consulting-candidates-seeking-jobs-on-pasona.vn-website/assets/126949248/98a5a8dc-3650-4ab3-91fd-087ef6b1a870'/>
      </p>
      <p>
        <i>the response from chatbot</i>
      </p>
    </div>
  </li>
  <li><b>"End chat"</b>: If the customer no longer needs to use the chatbot, they can choose to end the conversation. At this point, the system will disable the message composition box and send message button. Additionally, the system will invite the customer to rate their chatbot experience using a 5-point scale represented by 5 stars. Whatever star the customer selects, the system will store the value (score) of that star and update it in the "rating" column in the customer contact table. Finally, a thank you message will be displayed, and the conversation will end.
    <div align='center'>
      <p>
        <img src='https://github.com/MinhThanh2404/Chatbot-for-consulting-candidates-seeking-jobs-on-pasona.vn-website/assets/126949248/d9d28d3f-14ab-4d2f-8cc5-822fa31151f8'/>
      </p>
      <p>
        <i>rating section</i>
      </p>
    </div>
  </li>
</ul>
</p>
</li>
</div>
<br/>

<li>
  <h2>Source code summary</h2>
  <h3><i>Frontend</i></h3>
  <p>
    Originally, this chatbot is an element belonging to the footer of the website. However, in this repository, the chatbot will be extracted independently. Here's the structure of frontend folder:
  </p>
  <div align='center'>
    <p>
      <img src='https://github.com/MinhThanh2404/Chatbot-for-consulting-candidates-seeking-jobs-on-pasona.vn-website/assets/126949248/326f2d11-f75b-4d20-b2e2-6a66a0dbcd38'/>
    </p>
    <p>
      <i>frontend source code</i>
    </p>
    <p>
      <img src='https://github.com/MinhThanh2404/Chatbot-for-consulting-candidates-seeking-jobs-on-pasona.vn-website/assets/126949248/6c770ef2-b7c3-42d3-a6f7-609c60cda587'/>
    </p>
    <p>
      <i>a sample function to call API from server</i>
    </p>
  </div>

  <h3><i>Backend</i></h3>
  <div align='center'>
    <p>
      <img src='https://github.com/MinhThanh2404/Chatbot-for-consulting-candidates-seeking-jobs-on-pasona.vn-website/assets/126949248/652e99de-0377-437d-a85a-96c46c6329dd'/>
    </p>
    <p>
      <i>backend source code</i>
    </p>
  </div>
  
  <ul>
    <li>app.py: Sets up environment variables, connects to the database, and registers blueprints for routes.</li>
    <li>.env: Contains information about keys and accounts of third-party applications linked to the program.</li>
    <li>In the routes folder, the file chat.py specifies functions and methods for each endpoint.</li>
    <li>In the controller folder, the file chat_controller.py defines the functions called in the routes section. Each function will define the types of input data and the functions (services) that will be applied to process that input data.</li>
    <li>In the services folder, each file corresponds to a stage in the chatbot process. Each file will define objects and functions that perform specific operations (adding, updating, deleting, etc.).</li>
    <li>In the model folder, each file corresponds to a data table used in the chatbot process. Each file will define the columns of each table and the data types of each data field.</li>
    <li>In the utils folder, the files will define the structure (format) of input/output data.</li>
    <li>The fine-tuning_model folder contains fine-tuned files for the deep learning natural language processing (NLP) model. The files in this folder will not run together with the entire chatbot program but will be run separately at a specific time to improve the model.</li>
  </ul>
  
  <p><i><b>Execution flow</b>: Routes -> controllers -> utils -> services -> models -> controllers -> utils -> routes.</i></p>

  <h3><b>Fine-tuning deel learning BERT model:</b></h3>
  <div>
    <p>
      After processing, cleaning, and extracting the original messages, retaining the message keywords, the the author will classify the message topics to direct them to various processing steps corresponding to each topic. Currently, there are two main topics: 'amount' and 'salary', and an additional topic for message unrelated to recruitment and employment, labeled as 'trivia'. Including this 'trivia' topic reduces processing time; the system, upon recognizing a message belonging to the 'trivia' topic, will transfer it directly to storing the message and automatically respond, 'Sorry, your request is beyond our knowledge. We are in the progress of expanding our intelligence. Thanks for your resource.'<br/>
    In cases where messages are classified as 'amount' or 'salary', the system will perform deeper language analysis to identify the objects and their roles in the SQL query.This is a data classification problem, where the training dataset is pre-labeled. We'll apply a deep learning model to 'learn' the characteristics of each class from the training dataset, allowing us to classify test data.<br/>
    Given the absence of historical data regarding customer queries on the company's website, in the first trial, the author aim to leverage existing functions and libraries to save time in preparing the training data and fine-tuning deep learning models. They choose the 'synset()' function from the WordNet library to detect synonyms related to the topics 'amount' and 'salary'. However, the synonyms list from this library is limited, and many human-understood words or phrases pertaining to a topic might not be synonymous. Consequently, the 'synset()' function's understanding of these words or phrases is restricted, unable to discern their synonymous relationships.<br/>
    Realizing that the available NLTK libraries might not specifically meet the chatbot's processing needs, the author will create a training dataset consisting of questions potentially sent by customers using the chatbot. They'll label the dataset's topics and fine-tune a pre-trained deep learning model to classify and identify the message topics.<br/>
    The training dataset comprises 322 messages: 111 'amount,' 111 'salary,' and 100 'trivia.' Before training, this dataset will undergo cleaning using the 'clean_data()' function defined in Task 3. Post-training, the author will employ the 'WordCloud()' function from the wordcloud library to visualize common words for each topic, facilitating adjustment in case of excessive similarity between two classes.
    </p>
    <p>
      After obtaining the training dataset, the author proceeds to explore and choose a deep learning model. In this case, the author will select the BERT model. Leveraging the knowledge acquired in Machine Learning, Artificial Intelligence, and deep learning models, the author proceeds to fine-tune the BERT model to suit the classification problem (message topic identification).<br/>
      Each deep learning model serving a task will be stored in separate files within the 'fine-tuning_model' folder. The message topic identification model will be saved in the file 'train_model_modifier.py'. First, necessary libraries such as torch, transformers, and tensorflow are installed via the command <i>"pip install torch tensorflow transformers"</i> and essential modules are imported like torch, BertForSequenceClassification, BertTokenizer, tensorflow, and some modules essential for representation and model evaluation.<br/>
      For the current classification task, the original model will be fine-tuned by adding a classification layer at the end of the model, and the output of the main model will be the input to this classification layer. A class named UpdatePretrainedModel is created, in which a function named train_and_save_model() is defined with the following input parameters:
      <ul>
        <li>new_input_texts: set of cleaned messages</li>
        <li>new_labels: set of corresponding labels for the input messages</li>
        <li>save_path: file name to contain the tuned model</li>
        <li>num_classes: number of classes (labels) in the classification part</li>
        <li>batch_size: number of data samples in one training iteration</li>
        <li>learning_rate: a hyperparameter used in training neural networks. Its value is a positive number, usually between 0 and 1.</li>
      </ul>
    Next, the model name for fine-tuning, 'bert-base-uncased', is declared, and the pre-trained BERT model is loaded for classification by invoking BertForSequenceClassification.from_pretrained() with input parameters comprising the model name (previously declared) and the number of labels equal to the number of classes in the training data sample. The input data is processed using the tokenizer() function of the model to transform it into a form suitable for inputting into the model. Both the tokenized input messages and labeled data (already encoded) are converted into PyTorch tensors and combined into a TensorDataset. The 'Dataloader' will feed the TensorDataset into the model, addressing the issue of selecting the number of data samples and shuffling data during training.<br/>
    Subsequently, the loss function 'CrossEntropyLoss' and the optimizer 'Adam' are defined. The optimizer function updates the model's weights based on gradients during the backpropagation process.<br/>
    <b>Backpropagation</b>, short for "backward propagation of errors," is a common method used in training artificial neural networks in conjunction with an optimization method like gradient descent. This method calculates the gradient of the loss function with respect to all relevant weights in that neural network. This gradient is used in the optimization method to update the weights, aiming to minimize the loss function.<br/>
    Once the input factors are prepared, the training loop begins. Here, the number of epoch loops during training is set to 200, and the loss metric is saved every 50 loops to monitor whether the model is overfitting or not. At the beginning of each epoch, the loss metric is reset to 0, and the model is put into training mode. The inner loop iterates through batches of data samples. For each batch, the optimizer's gradient is zeroed, the model's output and the loss metric are calculated. Then, the backpropagation process is executed, updating the optimizer's weights and the total loss of that epoch.<br/>
    Upon completion of training for 200 epochs, the .save() function from torch is used to export the model file with the filename passed through the save_path parameter. The fine-tuning function concludes and returns the name of the fine-tuned model file.
    </p>
    <p>
      In the main() function, after cleaning the training data and saving the updated data to an Excel file, the file is opened as a DataFrame. The model fine-tuning function is called, passing in the necessary parameters. Upon completion of this function, a new .path file will appear in the directory. This file contains the fine-tuned model.<br/>
      The next step after successfully training the model is model evaluation. Here, the author utilizes a confusion matrix and calculates metrics like accuracy, precision, recall, and F1 score. Using the training dataset again, after declaring the use of the fine-tuned model, the author performs embedding steps and predicts labels for the messages. The prediction results are saved into a new column in the data table.<br/>
      <ul>
        <li>Accuracy is computed as the ratio of the number of correct predictions (true positives) to the total number of samples in the dataset. In this initial trial, the accuracy of predictions is at an average of 66%.</li>
        <li>The Confusion Matrix is a vital tool in evaluating the performance of a classification model in machine learning. It provides a comprehensive view of how the model predicts classes and offers information about the distribution of predictions compared to reality. Elements on the diagonal of the matrix represent the number of correctly predicted observations, while elements outside the main diagonal indicate the number of misclassified items into other classes. With this model, the 'salary' class is misclassified as 'amount' a lot, with only 1 out of 18 elements belonging to the 'salary' class being correctly labeled; the rest are labeled as 'amount'.</li>
      </ul>
    <div align='center'>
      <img src='https://github.com/MinhThanh2404/Chatbot-for-consulting-candidates-seeking-jobs-on-pasona.vn-website/assets/126949248/52298069-f0a2-403f-a61d-8b2651be67da'/>
    </div>  
    This indicates an issue with the training dataset, specifically that the 'amount' and 'salary' classes are quite similar at present, requiring a modification of the dataset to differentiate these two classes better. Looking at the word clouds of both classes, it's evident that the 'amount' and 'salary' classes share many common words (position, job, role). However, in the 'amount' class, common words represent topic content (open, total, position: the number of open job positions), whereas in the 'salary' class, common words are more generic and not related to salary (job, role, position... unrelated to salary).
    <div align='center'>
      <p>
        <img src='https://github.com/MinhThanh2404/Chatbot-for-consulting-candidates-seeking-jobs-on-pasona.vn-website/assets/126949248/8a1c83ac-5b61-4b9e-b76b-884053772d96'/>
      </p>
      <p><i>wordcloud of 'amount' topic</i></p>
      <p>
        <img src='https://github.com/MinhThanh2404/Chatbot-for-consulting-candidates-seeking-jobs-on-pasona.vn-website/assets/126949248/7e7fc13e-f66c-42a0-b87d-5eb5002991eb'/>
      </p>
      <p><i>wordcloud of 'salary' topic</i></p>
    </div>
    Therefore, the 'salary' class data needs to be modified. After modification, common words like average, standard, role... are more related to the salary theme, making this new data more acceptable.
    <div align='center'>
      <p>
        <img src='https://github.com/MinhThanh2404/Chatbot-for-consulting-candidates-seeking-jobs-on-pasona.vn-website/assets/126949248/fd3999f9-a106-4a49-8df7-72b39e1cc0ce'/>
      </p>
      <p><i>wordcloud of modified 'salary' topic</i></p>
    </div>
    Upon fine-tuning the model for the second time, the evaluation results are more promising. Specifically, the accuracy has increased to 99.38%, and there are no more misclassifications between the 'amount' and 'salary' classes. Although the 'trivia' class has 2 cases misclassified as 'amount', it's negligible and can be ignored. The second fine-tuned model is accepted and ready for deployment.
    <div align='center'>
      <img src='https://github.com/MinhThanh2404/Chatbot-for-consulting-candidates-seeking-jobs-on-pasona.vn-website/assets/126949248/bee0a98e-0d1c-4114-8aca-bbfdd0cf739a'/>
    </div>
  </p>
  <p>
    After fine-tuning the deep learning model, the author combines two methods of message topic identification into one function named `topic_identifier()`. This function takes two input parameters: a dictionary of topics (as during model fine-tuning, labels were encoded, and the model's predictions return numerical types, requiring a dictionary defining the encoded topics) and the cleaned message text. Initially, the `synsets()` function from the WordNet library is used to find any synonyms of the names of the three topics within the sentence. If a synonym is found, that word is replaced with the topic word, and the function returns the message with the replaced topic word. Otherwise, if no synonyms of any topic word are found, the fine-tuned model is utilized. The `topic_identifier()` function returns an object containing the identified topic word and the message.<br/>
    Within `chat_controller()`, the topic words are listed in a collection, and the `topic_identifier()` function is called to determine the message's topic. In the case where the topic word is 'trivia', the message is stored in the data store with a response of "Sorry," indicating the end of the chat session. Otherwise, the system continues the analysis, constructs an SQL query, and generates a response for the customer.
    <ul>
      <li>Messages unrelated to recruitment and job-related topics (trivia): Successful classification of these messages results in the message being correctly categorized and saved into the database. The chat session ends with a response of "Sorry, the information has not been updated in our intelligence."</li>
      <li>Messages inquiring about salary or the number of job openings: Successful classification of these messages.</li>
    </ul>
  </p>
  <div align='center'>
    <img src='https://github.com/MinhThanh2404/Chatbot-for-consulting-candidates-seeking-jobs-on-pasona.vn-website/assets/126949248/70902893-5724-4d65-9cc7-0f8421fe62d8'/>
  </div>
  
