# Simple Chatbot Application

This project is a simple chatbot application featuring a Next.js frontend and a Flask backend. It allows users to inquire about sushi restaurants or parking garages near Marienplatz, Munich, and get detailed information through a conversational interface.

## Getting Started

Below are the instructions to set up the frontend and backend locally on your machine.

### Backend Setup

The backend is developed with Flask. To get it up and running, follow these steps:

1. Navigate to the backend directory:

```bash
    cd chatbot-backend
```

2. Activate your virtual environment

- for Windows:

```bash
   .\venv\Scripts\activate
```

- for macOS/Linux:

```bash
    source venv/bin/activate
```

3. Start the Flask application

```bash
    flask run
```

### Frontend Setup

The frontend is built with Next.js and styled using Tailwind CSS. To start the frontend, execute the following:

1. Navigate to the frontend directory:

```bash
    cd chatbot-frontend
```

2. Install the necessary packages:

```bash
    npm install
```

3. Run the Next.js development server:

```bash
    npm run dev
```

Now, your frontend should be accessible at http://localhost:3000, and your backend should be running on http://localhost:15000.
