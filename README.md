# ShelfSpace

A modern bookshelf application built with Django and Tailwind CSS.

## Features

- Track your reading progress
- Search and add books from Google Books
- Organize books by status (Reading, Completed, Plan to Read, etc.)
- Add notes and track page progress
- Daily literary quotes
- Responsive design with Tailwind CSS

## Tech Stack

- Python 3.13
- Django 5.1
- Tailwind CSS 3.4
- PostgreSQL
- Google Books API

## Setup

1. Clone the repository:
```bash
git clone https://github.com/psimmons86/bookshelf.git
cd bookshelf
```

2. Create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install django django-widget-tweaks psycopg2-binary python-dotenv requests
```

4. Install Node.js dependencies:
```bash
npm install
```

5. Create a `.env` file in the project root and add your configuration:
```
DB_USER=your_db_user
DB_PW=your_db_password
DB_HOST=your_db_host
```

6. Run migrations:
```bash
python3 manage.py migrate
```

7. Build CSS:
```bash
npm run build
```

8. Run the development server:
```bash
python3 manage.py runserver
```

Visit http://127.0.0.1:8000/ to see the application.

## Development

- Build CSS (watch mode):
```bash
npm run watch
```

- Fetch quotes for the database:
```bash
python3 manage.py fetch_quotes
```

## License

MIT License
