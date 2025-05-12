# Music Recommendation System

A modern music recommendation system built with Vue 3 and Django, featuring personalized recommendations, intelligent search, and social interactions.

## Tech Stack

### Frontend
- Vue 3 + TypeScript
- Element Plus
- Pinia
- Vue Router
- Axios
- Web Audio API
- Vite

### Backend
- Django 5.0 + Django REST framework
- PostgreSQL
- Redis
- Elasticsearch 8.x
- TensorFlow Recommenders
- BERT
- RabbitMQ
- Docker + Docker Compose

## Project Structure

```
music-recommend/
├── frontend/                 # Vue 3 frontend
├── backend/                  # Django backend
├── docker/                   # Docker configurations
└── kubernetes/              # Kubernetes configurations
```

## Getting Started

### Prerequisites
- Node.js >= 16
- Python >= 3.9
- Docker
- Docker Compose

### Development Setup

1. Clone the repository
2. Set up frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. Set up backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

4. Set up Docker (optional):
   ```bash
   docker-compose up -d
   ```

## Documentation

- [API Documentation](docs/api.md)
- [Architecture Overview](docs/architecture.md)
- [Development Guidelines](docs/development.md)

## License

MIT 