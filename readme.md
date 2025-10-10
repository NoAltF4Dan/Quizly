# Quizly Backend

![Logo](/media/logoheader.png)

Quizly is an innovative, AI API-based backend for an interactive quiz application, leveraging Django and Django REST Framework. Powered by advanced AI, it enables users to create, take, and manage quizzes with a standout feature: automatic quiz generation from YouTube videos using AI-driven content analysis. The API supports seamless question creation, user answer submission, and result tracking, making it perfect for educational platforms, trivia apps, or personalized learning tools.

Find the frontend here: [Quizly Frontend Repository](https://github.com/NoAltF4Dan/Quizly_Frontend.git)

## Features

The Quizly backend provides the following core features:

- **AI-Powered Quiz Generation**: Automatically creates quizzes from YouTube videos using the Gemini API for content analysis.
- **Question Answering**: Users can answer questions generated from Gemini API.
- **Result Storage**: Save quiz results for later reference.

## Getting Started

Follow this guide to set up a local development environment for the project.

### Prerequisites

Make sure you have Python 3.13.3 (or newer) and pip installed on your system.

### Installation

1. Clone the repository:

```bash
git clone https://github.com/NoAltF4Dan/Quizly-Backend.git
cd Quizly-Backend
```

2. Create a virtual environment and activate it:

```bash
python -m venv env
```
```bash
source env/bin/activate   # macOS/Linux
```

On Windows:

```bash
env\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Create a Gemini API key and configure environment

Generate a Gemini API Key: Visit Google AI Studio to create your Gemini API key.
https://aistudio.google.com/api-keys


```bash
cp -n .env.template .env
```

change:
GEMINI_API_KEY=YOUR_GOOGLE_GEMINI_API_KEY

4. Run the database migrations:

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
- **Backend**: Built by Daniel K.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
