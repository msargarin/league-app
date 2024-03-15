# Basketball League App

A complete app for all of your league's data needs.

<br/>

## Requirements

- Python (3.8, 3.9, 3.10, 3.11, 3.12)

<br/>

## How to Use

### Setup the backend

1. Install any supported python version [here](/https://www.python.org/downloads/).
2. Download/clone the project.
3. Open a terminal or command prompt then navigate to the project's `backend` folder.

```bash
$ cd backend
```

4. Install virtualenv.

```bash
$ pip install virtualenv
```

5. Create a virtual environment with virtualenv.

```bash
$ virtualenv env
```

6. Install libraries specified in `requirements.txt`.

```bash
$ pip install -r requirements.txt
```

7. Set environment variables by creating a `.env` file from `.env.example`.
8. Create the database.

```bash
$ python manage.py makemigrations
```

9. Run the development server

```bash
$ python manage.py runserver
```

<br/>

## Dependencies

### Python

- virtualenv
- Django
- Django Rest Framework
- python-dotenv
