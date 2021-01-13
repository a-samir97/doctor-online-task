# Doctor Online Task 

### How to run project ?
- Assuming you have pip library and you can make virtual environment to this project 

- Install dependencies from requirenments.txt 

  > pip install -r requirenments.txt

- Create database in mysql server and edit configuration in db.cnf file 

- Run these command to make database migrations 
  > python3 manage.py makemigrations
  
  > python3 manage.py migrate 

- (Optional) if you want to make superuser to login in admin dashboard, run this command 
  > python3 manage.py createsuperuser

- Finally, to run server
  > python3 manage.py runserver
_______________________________________________________________________________________________

### How to use application ?
- If you want to see swagger documentation 
  
  - > /docs/
  
- User can signup
  
  - > /api/users/signup/ 
  - > user need to put username, password, first_name, last_name, user_type ('D' for Doctor and 'P' for Patient)
  
- User can login 
  
  - > /api/users/login/
  - > user login by username and password

- Doctor can create sessions 
  - > doctor can create, delete, update, get session via this URL
  - > /api/sessions
  - > doctor need to send title, price, date, start_time, end_time, session_type( 'D' for Daily or 'W'for Weekly)

- Patient Book session
  - > /api/sessions/book/<session_id>

- To get all Booked sessions 
  - > /api/sessions/booked/
 
- To get all available sessions
  - > /api/sessions/available/
____________________________________________________________________________________________________

### Tools
- Python 
- Django
- Django Rest Framework
- MySQL
