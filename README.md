# Basketball League App

A complete app for your league's data needs.

This project was bootstrapped with [Vite](https://vitejs.dev/).

## Requirements

- Python (3.8, 3.9, 3.10, 3.11, 3.12)
- NodeJS (>18)

<br/>

## How to Use

First step is to download/clone the project.

### Setup the Django backend

1. Download and install any supported python version from [here](https://www.python.org/downloads/).
2. Open a terminal or command prompt then navigate to the project's `backend` folder.

```bash
$ cd backend
```

3. Install virtualenv.

```bash
$ pip install virtualenv
```

4. Create a virtual environment with virtualenv.

```bash
$ virtualenv env
```

5. Install libraries specified in `requirements.txt`.

```bash
$ pip install -r requirements.txt
```

6. Find the `league` folder, create a copy of `.env.example` in the same folder, rename the copy to `.env` then set environment variables.

7. Create database tables.

```bash
$ python manage.py migrate
```

8. Create dummy data.

```bash
$ python manage.py populate_database
```

9. Run the development server.

```bash
$ python manage.py runserver
```

### Setup the React frontend

1. Download and install any supported nodejs version from [here](https://nodejs.org/en/).
2. Open a terminal or command prompt then navigate to the project's `frontend` folder.

```bash
$ cd frontend
```

3. Install dependencies.

```bash
$ npm i
```

4. Run the development server.

```bash
$ npm run dev
```

### Go to your browser

1. The React app should now be accessible on your browser at [`http://localhost:5173`](http://localhost:5173)
2. Select your preferred `role`, login and start exploring!

<br/>

## How it works

### Authentication

The backend has an endpoint exposed for creating access tokens. This endpoint requires a `role` payload which it then uses to determine the claims in the created token. The created token will have `name`, `role` and `team` claims.

For an admin role, the team will be set to `null` and the name will be set to a single hardcoded name. For the coach and player roles, a random coach or player will be selected and the token claims will be populated accordingly. This allows you to login with just the role.

Tokens are refreshed automatically upon expiry.

### Authorization

Resources are restricted to a logged in user's role:
- Admins have access to everything
- Coaches have access to their own team and players but not to other teams or players of other teams
- Players can only view the tournament brackets

Authorization is enforced on the backend but the frontend also clue in users to what they can do (eg. players do not see a cursor when hovering over team names in the tournament bracket). Users are informed if they try to access a resource they do not have access to.

<br/>

## Dependencies

### Python

- virtualenv
- Django
- Django Rest Framework
- python-dotenv
- djangorestframework-simplejwt
- django-cors-headers
- coverage

### React

- react-router
- react-router-dom
- flowbite
- flowbite-react

## Attributions

Special thanks to `mattc0m` and his awesome tournament bracket styling at [codepen](https://codepen.io/mattc0m/pen/gByvpw) where the brackets for this project has been derived from.
