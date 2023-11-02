1. Cài đặt Python 3 và Nodejs
 - https://www.python.org/downloads/
 - https://nodejs.org/en

2. Cài đặt gói PM2
 - npm install -g nodemon

3. Cài đặt gói Flask, các thư viện cần thiết trong python
 - pip install flask sqlalchemy pymysql python-dotenv flask_sqlalchemy nltk emoji autocorrect stopwords torch tensorflow pandas scikit-learn transformers spacy matplotlib openpyxl flask-cors
 - #python -m spacy download en_core_web_lg
 - #python -m nltk download wordnet, punkt, stopwords, averaged_perceptron_tagger

4. Chạy API server
 - nodemon --exec python app.py

 ** Trong trường hợp phát sinh lỗi không thể thấy được python thì cần cấu hình đường dẫn cho thư mục bin của python.

 5. Trong trường hợp cập nhật training dataset và muốn fine-tune model:
 - mỗi model sẽ nằm trong 1 file riêng, fine-tune model nào thì chạy file của model đó
 - cách chạy: direct vào folder chứa các file model (fine-tuning model), ở terminal gõ lệnh: python <tên file.py> 
 - chi tiết cách chạy được note trên đầu mỗi file.