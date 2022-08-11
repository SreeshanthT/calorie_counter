# Calorie Counter
## Create Virtual Env
create:

```sh
python -m pip install --user virtualenv
py -m venv <venv>
```
make sure you are in project directory

activate:
```sh
.\<venv>\Scripts\activate
```
## Installation
Install Required Packages. we have a requirement.txt file that contain all required packages list with its versions
```sh
pip install -r requirements.txt
```
After the installation we need to run the project before that reconfirm you are activated the virtual env and you are in project direction and find out there manage.py python file

## Run server
Before run server we need to create out database here i am using sqlite.
so we need to run migration commands are:
```sh
python manage.py makemigrations
python manage.py migrate
```
after that we need to create a superuser by using the command:
```sh
python manage.py createsuperuser
```
follow the commands and create a superuser after that we can run the server:
```sh
python manage.py runserver 
```
here the default port number is 8000 if we want to change the port no we can type the port number after the runserver command:
```sh
python manage.py runserver [port_number]
```
The url be like:[http://127.0.0.1:8000/]

## Sitemap
Register:
- [http://127.0.0.1:8000/register/]
use method POST, 
requests:
        {
            "username": "",
            "password": "",
            "password2": "",
            "email": "",
            "first_name": "",
            "last_name": ""
        }

Login:
- [http://127.0.0.1:8000/login/]
user method POST
{
"username":"user_name",
"password":"xxxx"
}

Admin:
- [http://127.0.0.1:8000/admin/]
user superuser for auth credentials

Manage Food item and Activity:
- [http://127.0.0.1:8000/food-item]
- [http://127.0.0.1:8000/activity]

Manage Food Routine:
- list food routine [http://127.0.0.1:8000/food-routine-add/] methd GET
- add food routine [http://127.0.0.1:8000/food-routine-add/] methd POST
requests:
{
"food_item":<id_of_prepopulated_food>
}
- view food routine [http://127.0.0.1:8000/food-routine-<id>/] method GET
- edit food routine [http://127.0.0.1:8000/food-routine-<id>/] method POST
requests:
{
"food_item":<id_of_prepopulated_food>
}

Manage Activity Routine:
- list activity routine [http://127.0.0.1:8000/activity-routine-add/] methd GET
- add food routine [http://127.0.0.1:8000/activity-routine-add/] methd POST
requests:
{
"activity":<id_of_prepopulated_activity>
}
- view food routine [http://127.0.0.1:8000/activity-routine-<id>/] method GET
- edit food routine [http://127.0.0.1:8000/activity-routine-<id>/] method POST
requests:
{
"activity":<id_of_prepopulated_activity>,
'status':<1/2>,
}
status: 1- activity started
status: 1- activity finished

List status of calorie:
- [http://127.0.0.1:8000/my-calorie-status/] method GET

we can filter if you need use the query parameters be like
- [http://127.0.0.1:8000/my-calorie-status/?date_from=yyyy-mm-dd&date_to=yyyy-mm-dd]
- [http://127.0.0.1:8000/my-calorie-status/?last_week]
- [http://127.0.0.1:8000/my-calorie-status/?month=<1-12>]
- [http://127.0.0.1:8000/my-calorie-status/?year=yyyy]