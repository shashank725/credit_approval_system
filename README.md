<h1 align="center">Credit Approval System</h1>
<h4 align="center">This project is based on creating a credit approval system based on past data as well as future transactions</h4>

<br>
<p align="center">
<img src="https://badges.frapsoft.com/os/v1/open-source.svg?v=103"/> <br><br>
<a href="https://www.python.org/" target="blank"><img align="center" src="http://ForTheBadge.com/images/badges/made-with-python.svg" alt="python"/></a>
<a href="https://www.djangoproject.com/" target="blank"><img align="center" src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="django" height="37" width="90"/></a>
</p>

### Project Setup : (Without Docker)

Prerequisites
1. python3
2. pip3


3. Clone the project.

    ```shell
    git clone https://github.com/shashank725/credit_approval_system.git
    ```
    

4. Create a virtual environment with venv (install virtualenv, if its not installed) inside the project floder.
  
    ```shell
    cd credit_approval_system
    ```
  
   #### For Linux/Mac OSX (Any one of these)
    ```shell
    pip install virtualenv
    python3 -m venv venv
    ```
    ```
    sudo apt-get install python3-venv
    python3 -m venv venv
    ```
  
   #### For Windows
    ```shell
    pip install virtualenv
    python -m venv venv
    ```


5. Activate the virtual environemnt.

    #### For Linux/Mac OSX
    ```shell
    source venv/bin/activate
    ```

    #### For Windows
    ```shell
    venv\Scripts\activate
    ```
   
6. Install the requirements.

    ```shell
    pip install -r requirements.txt
    ```
 
7. Run the Migrations

    ```shell
    python manage.py makemigrations --settings=credit_approval_system.settings_dev
    python manage.py migrate --settings=credit_approval_system.settings_dev
    ```

8. Run the development server

    ```
    python manage.py runserver --settings=credit_approval_system.settings_dev
    ```
9. Head to server http://127.0.0.1:8000

<br>

### Run Celery:
```
celery -A credit_approval_system worker -l info
```

### Run Redis:

```
redis-server ()
```

```
redis-cli
KEYS *
GET celery-task-meta-<task-id>
```