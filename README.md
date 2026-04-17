# E-Commerce Project

Full-stack E-commerce application with Django (Backend), Next.js (Frontend), PostgreSQL (Database), and Nginx (Reverse Proxy).

## Project Structure

- `backend/`: Django application
- `frontend/`: Next.js application
- `nginx/`: Nginx configuration
- `docker-compose.yml`: Docker orchestration

## Getting Started

You can run the project either using Docker (recommended for a quick full-stack setup) or locally without Docker (recommended for active backend/frontend development).

### Option A: With Docker (Recommended)

**Prerequisites:**
- Docker
- Docker Compose

1. Clone the repository.
2. Run the application:
   ```bash
   docker-compose up --build
   ```
3. Access the application:
   - Frontend: `http://localhost`
   - Backend API: `http://localhost/api`
   - API Docs: `http://localhost/api/docs/`
   - Django Admin: `http://localhost/admin`

4. To create a superuser inside the container (though one is created automatically on startup):
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

> [!NOTE]
> The application automatically runs migrations and generates dummy data (including a superuser: `admin@admin.com` / `admin`) every time the backend container starts.

### Option B: Without Docker (Local Development)

**Prerequisites:**
- Python 3.10+
- Node.js 18+ (for frontend)
- PostgreSQL (or SQLite will be used by default)

#### Backend Setup (Django):
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. **(Optional)** Generate dummy initial data and a superuser (`admin@admin.com` / `admin`):
   ```bash
   python manage.py generate_random_products
   ```
6. Start the server:
   ```bash
   python manage.py runserver
   ```
   The backend API will run on `http://127.0.0.1:8000/api/` and Docs at `http://127.0.0.1:8000/api/docs/`.

#### Frontend Setup (Next.js):
1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Next.js development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:3000`.

## Development

### Commit Messages

This project uses [Commitizen](https://commitizen-tools.github.io/commitizen/) to enforce conventional commits.
Please use `cz commit` or ensure your commit messages follow the conventional commit format:

```
feat: add new feature
fix: bug fix
docs: documentation changes
style: formatting, missing semi colons, etc
refactor: refactoring production code
test: adding missing tests, refactoring tests
chore: updating grunt tasks etc
```

### Versioning

Version bumping is handled automatically by GitHub Actions on push to `main` branch.
