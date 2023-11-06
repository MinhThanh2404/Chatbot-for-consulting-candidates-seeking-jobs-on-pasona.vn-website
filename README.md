<h1>Chatbot for consulting candidates seeking jobs on pasona.vn website</h1>

<p>This chatbot is integrated on pasona.vn website to be an AI assistant answering the web visitors/ job seekers' job-related inquiries (salary, open positions...). The chatbot applies a fine-tuned BERT model to categorize the main topic of the message, and direct to specific response process based on each topic to interact with the database. This repository contains both the frontend and backend design: the frontend languages are HTML, CSS, Javascript; the backend ones are Python, SQL. For the message processing, many NLP techniques have been combined, and for topic classification issue, a fine-tuned BERT model is applied. The author will introduce how the chatbot operates, source code's structure, and some highlights in the backend process, focusing on NLP techniques and ML model. The full report is written in Vietnamese.</p>

<h2><b>Table of content:</b></h2>
<ol>
  <li>Workflow of the chatbot</li>
  <li>Source code summary</li>
  <li>Development ideas</li>
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
