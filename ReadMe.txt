To Setup, firstly install all required packages from requirements.txt file.

1. After successfull installing, you have to setup your database settings, here I am using
Postgresql, for this you have to change database name, user and password in settings.py file.

2. Now run makemigrations/migrate cmd and then create superuser for accessing admin profile.

3. Now, hit this api "http://127.0.0.1:8000/download" : this api will first authenticate the
google account and then connect to the google drive and fetch all the "pdf" files associated
with the account to the app root and then extract the content of pdf files using Apache Tika
and after this it will index pdf using Elasticsearch service.

4. Now you can hit "http://127.0.0.1:8000/search?q=<pan-number>" : this api will search query
parameter value in pdf content and if this parameter match with any pdf's content then it will
return the list of google drive documents link of related parameter matched file.

NOTE 1 : Here I dont have any AWS credentials so I am unable to use AWS service so for this I used
Elasticsearch in my localhost and all the pdf indexed in the same. So for using Elasticsearch in
local you have to install it on your local,
(I followed https://phoenixnap.com/kb/install-elasticsearch-ubuntu for installing Elasticsearch
in my local)

NOTE 2 : In project root directory you have to save your client_secrets.json file which contains
your google drive API keys.