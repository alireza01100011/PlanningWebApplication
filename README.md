license :

``` 
  The most important rule: for any commercial use! or public service you must buy application template [sneat] 
  from original source (https://themeselection.com/item/sneat-bootstrap-html-admin-template/).
  
  The backend codes are completely free and copying is allowed with reference to the source!
```

## Planning web application | Time Management
![image](https://github.com/alireza01100011/ToDo-flask/assets/95130614/70bfdef9-c95e-463e-9190-de8e6057cf4a)

### --- Desktop ---
<img src="https://github.com/alireza01100011/ToDo-flask/assets/95130614/3638ca0f-b8c6-4395-b882-2db2d9ad4e3e" width="49%"></img>
<img src="https://github.com/alireza01100011/ToDo-flask/assets/95130614/f4357e66-5613-48fd-8ea5-5c6e66e6fc6c" width="49%"></img>

<img src="https://github.com/alireza01100011/ToDo-flask/assets/95130614/cbad97fe-6a99-4816-a211-496cd8965172" width="49%"></img>
<img src="https://github.com/alireza01100011/ToDo-flask/assets/95130614/9226fbce-af75-4e2b-941c-cbdea0beed8d" width="49%"></img>

<img src="https://github.com/alireza01100011/ToDo-flask/assets/95130614/4dac7456-ec12-4424-a62f-fb91d980403e" width="49%"></img>
<img src="https://github.com/alireza01100011/ToDo-flask/assets/95130614/000b2bcd-056b-4699-bd70-00f08822ec88" width="49%"></img>


### --- Mobile ---

<img src="https://github.com/alireza01100011/ToDo-flask/assets/95130614/e4ef4666-2fb7-4dfe-a553-50fc0c1001f8" width="30%"></img>
<img src="https://github.com/alireza01100011/ToDo-flask/assets/95130614/7d66a9bb-cdfe-42fc-9e56-cca215de0947" width="30%"></img>
<img src="https://github.com/alireza01100011/ToDo-flask/assets/95130614/7491d70d-1a46-4eb1-bbfe-def55312797f" width="30%"></img>


<img src="https://github.com/alireza01100011/ToDo-flask/assets/95130614/201fa8f9-d22b-432d-861f-7e0139a584d8" width="30%"></img>
<img src="https://github.com/alireza01100011/ToDo-flask/assets/95130614/f1d4d78e-c561-4bea-9ad9-4b461640a336" width="30%"></img>
<img src="https://github.com/alireza01100011/ToDo-flask/assets/95130614/13ac9e35-1e23-4a30-979c-ff3ee5097dc3" width="30%"></img>



This application is developed with the Flask framework and uses Python 3.10. It uses SQLalchemy ORM to communicate with the database.


## Database model :
![image](https://github.com/alireza01100011/ToDo-flask/assets/95130614/5a6e0207-8717-4b9a-85a4-341943c9a0c9)

  * The data is stored in the database in the form of (groups - tasks - events) pickled

      For example: an event is first converted into this class, in the next step it is converted into a pickle, and finally it is stored in the database.
    
      ![image](https://github.com/alireza01100011/ToDo-flask/assets/95130614/d9494f6f-8037-48b8-bd83-799053088ab5)

  * Note: The classes are stored in a list and then they are pickled
    
      ![image](https://github.com/alireza01100011/ToDo-flask/assets/95130614/4a508244-3e27-4f27-a0bf-afb46ab8e273)

<br><br>
## Run 

### First, fill in the configuration files : 
  * /.env -> For Method.1 <br>
  * /app/.env -> For Method.2 <br>
    
### Method.1 For Develoop And Test :
  > `cd app`<br>
  > `python3 pip install -r requirements.txt`<br>
  > `python3 -m flask db init && python3 -m flask db migrate && python3 -m flask db upgrade`<br>
  > `python3 -m flask db run --debug`<br>
### Method.2 For Product Use :
  * Simple command : <br>
  > `docker-compose up --build -d`

<br><br><br><br>
### Todo :
  - Forget PassWord <br>
  - Leave handling of static files to Engenic <br>
  - Add profile picture for users <br>
  - Building the base class and reducing the code size of the section {app.mod_application.memory_management} <br>
  - Optimization


