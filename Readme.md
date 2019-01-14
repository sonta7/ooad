# Readme

### what environment do I need

pycharm,  mysql , mysql workbench,  django 2.1 



## how to import the database

in fact you have two choice:



1. By using mysql workbench. 

![image-20190102124809131](./image-20190102124809131.png)

Data import/restore  

![image-20190102124842676](./image-20190102124842676.png)

import from self-contained file  which contains in the root folder. 



2. python manage.py migrate  

   on the command line, then run the selected python file.  ![image-20190102125053196](./image-20190102125053196.png)



   Keep your configuration right ! 

   ![image-20190102125136373](./image-20190102125136373.png)





## Admin model 

![image-20190102125327394](./image-20190102125327394.png)

Create a super user this way, then enter http://127.0.0.1:8000/admin/, a easy way for u to manage the database and see the model structure.  You can dive into it to add some data manually.  USE IT TO CREATE AN STUDENT ACCOUNT, we have no register page available for others but super user. 

![image-20190102125448706](./image-20190102125448706.png)

## Anything I need to change?	

![image-20190102130114248](./image-20190102130114248.png)

change to your own USER & PASSWORD



## Structure

all html file in  ./templates

all js/css  file in ./static

all model information in ./login/models.py

all logic code in ./login/views.py