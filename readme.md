# Quizly Backend

![Logo](/media/logoheader.png)

Quizly is an interactive quiz application that allows users to create, take, and manage quizzes. The backend for this application enables quiz generation from YouTube videos, question answering, and storing results. This project is developed using Django and Django REST Framework.

Find the frontend here: [Quizly Frontend Repository](https://github.com/NoAltF4Dan/Quizly-Frontend.git)

## Features

The Quizly backend provides the following core features:

- **Quiz Generation**: Create quizzes based on YouTube video URLs.
- **Question Answering**: Users can answer questions generated from a video.
- **Result Storage**: Save quiz results for later reference.

## Getting Started

Follow this guide to set up a local development environment for the project.

### Prerequisites

Make sure you have Python 3.13.3 (or newer) and pip installed on your system.

### Installation

Clone the repository:

```bash
git clone https://github.com/HPetersen2/Quizly-Backend.git
cd Quizly-Backend
```

Create a virtual environment and activate it:

```bash
python -m venv env
```

On macOS/Linux:

```bash
source env/bin/activate
```

On Windows:

```bash
env\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a .env file in the project root and add your Gemini API Key:

```bash
SECRET_KEY=your_django_secret_key_here
DEBUG=True
GEMINI_API_KEY=your_gemini_api_key_here
```

Run the database migrations:

```bash
python manage.py migrate
```

Create a superuser for admin access:

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

The backend should now be accessible at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## API Endpoints

### Authentication
- **POST** `/api/register/`
- **POST** `/api/login/`
- **POST** `/api/logout/`
- **POST** `/api/token/refresh/`

### Quiz Management
- **POST** `/api/createQuiz/`
- **GET** `/api/quizzes/`
- **GET** `/api/quizzes/{id}/`
- **PATCH** `/api/quizzes/{id}/`
- **DELETE** `/api/quizzes/{id}/`

The exact routes and functionality are defined in the corresponding views and serializers.

## Built With

- **Python 3.13.3** - The programming language used.
- **Django** - The web framework for perfectionists with deadlines.
- **Django REST Framework** - A powerful and flexible toolkit for building Web APIs.
- **JWT (JSON Web Token)** - For secure authentication and authorization in the backend.
- **Whisper AI** - For speech-to-text functionality on YouTube video content.
- **Gemini API** - For video-related data processing.
- **yt-dlp** - A command-line tool to download videos and extract data from YouTube.

## Credits

- **Frontend**: Developer Akademie for providing the frontend.
- **Backend**: Built by Henrik Petersen.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
