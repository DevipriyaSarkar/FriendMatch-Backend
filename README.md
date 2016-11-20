# FriendMatch (Back End)
Flask server of FriendMatch with mySQL database

DBMS Project by [Devipriya Sarkar](https://github.com/DevipriyaSarkar) and [Namita Roy](https://github.com/namitaroy63)

# Setup Instructions

### mySQL Setup

1. Setup a mySQL user with username ```<your-mysql-database-user>``` and password ```<your-mysql-database-password>```.
2. Create a database ```<your-mysql-database-db>```.
3. Create the tables as in ```mysql_files/schema/schema.sql```.
4. Create the stored procedures as in ```mysql_files/stored_procedures```.
5. [Optional] For initial dummy data, data from ```mysql_files/data``` can be imported into respective tables.

### Flask setup

1. Make sure python 2.7 is installed on your system.
2. Install all the packages in ```requirements.txt```.  

 To install using pip, run ```pip install -r requirements.txt```.
 
3. Update the variables in ```app.py```,
 
 ```
 app.config['MYSQL_DATABASE_USER'] = '<your-mysql-database-user>'
 app.config['MYSQL_DATABASE_PASSWORD'] = '<your-mysql-database-password>'
 app.config['MYSQL_DATABASE_DB'] = '<your-mysql-database-db>'
 app.config['MYSQL_DATABASE_HOST'] = '<your-mysql-database-host>'
 ```

4. To run the application,
 
 ```  
 $ export FLASK_APP=app.py
 $ flask run
 * Running on http://0.0.0.0:5000/
 ```  
 
 If you are on Windows you need to use set instead of export.  
 Alternatively you can use python -m flask:  
 
 ```
 $ export FLASK_APP=app.py  
 $ python -m flask run  
 * Running on http://0.0.0.0:5000/  
 ```  

5. On Windows, run ```ipconfig``` on command prompt and note down the IPv4 Address ```<ip-address>```.

 On Linux, run ```ifconfig``` instead.  

6. Now head over to ```http://<ip-address>:5000``` to test if server is running. 



Now you should be able to run the Android app of FriendMatch. Download from [here] (https://github.com/DevipriyaSarkar/FriendMatch-Frontend/releases) and if you want to run the app on the local server just set up, click on "Have a local server?" and enter ```<ip-address>:<endpoint>``` in the input field, eg. ```192.168.1.107:5000```  .
