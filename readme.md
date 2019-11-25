Use below steps to run this program:
1. Create virtual environment using this command.
    virtualenv env_name --python=python3
2. Activate the environment
    source env_name/bin/activate
3. Install all the requirements using pip
    pip install -r requirements.txt
4. No need to migrate as I'm using document base database sqlite.
5. Use command to run the project
    python manage.py runserver


Following URLs are there for different purposes:
1. /users/login
2. /users/register

4. /api/v1/users/login
5. /api/v1/users/signup