# E-Commerce Project

Full-stack E-commerce application with Django (Backend), Angular (Frontend), PostgreSQL (Database), and Nginx (Reverse Proxy).

## Project Structure

- `backend/`: Django application (REST API)
- `frontend/`: Angular application (Storefront)
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

#### Frontend Setup (Angular):
1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Angular development server:
   ```bash
   npm start
   ```
    The frontend will be available at `http://localhost:3000`. 
    *(Note: Although port 4200 is the Angular default, this project is configured to use port 3000 to maintain compatibility with existing Docker and Nginx configurations).*

## Quality Assurance & Testing

### Backend Testing
The project uses `pytest` for backend testing. To run the tests:
```bash
cd backend
.venv/bin/pytest
```

### Frontend Testing
The project uses Karma/Jasmine for frontend unit testing. To run the tests:
```bash
cd frontend
npm test
```

### Authentication & Security
- **Registration Verification**: The registration feature has been verified to prevent duplicate emails and usernames using database-level unique constraints and API validation.
- **Role-Based Access**: The application supports different roles (`CONSUMER`, `VENDOR`, `ADMIN`) with corresponding dashboard redirections.

## Vendor Dashboard (Django Admin Integration)

The backend features a fully integrated **Vendor Dashboard** built directly into the Django Admin interface. 

### Features:
- **Role-Based Security:** Vendors can securely log into `/admin/` and will *only* see data belonging to their store. They cannot see other vendors' products or general administrative settings.
- **Auto-Population:** When a vendor adds products or requests store extensions, their `vendor_profile` is automatically assigned in the background.
- **Analytics:** A custom dashboard index shows real-time analytics for the logged-in vendor, including **Total Earnings**, **Items Sold**, and **Active Subscriptions**.
- **Admin Management:** Admins can securely review and approve vendor profiles and store extension requests via the same admin interface.

### Test Credentials
To test the vendor dashboard, you can use the pre-configured approved vendor account:
- **URL:** `http://127.0.0.1:8000/admin/`
- **Username:** `vendor`
- **Password:** `vendor123`

*(Note: Ensure you have run migrations and the database has been seeded using the provided methods before logging in).*

## Development

### Code Scaffolding

This project uses the Angular CLI for code generation. You can use the following commands inside the `frontend` directory:

```bash
# Generate a new component
ng generate component components/my-component

# Generate a new service
ng generate service services/my-service

# Generate a new module
ng generate module pages/my-page
```

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
