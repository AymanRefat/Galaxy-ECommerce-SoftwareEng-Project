# E-Commerce Project

Full-stack E-commerce application with Django (Backend), Next.js (Frontend), PostgreSQL (Database), and Nginx (Reverse Proxy).

## Project Structure

- `backend/`: Django application
- `frontend/`: Next.js application
- `nginx/`: Nginx configuration
- `docker-compose.yml`: Docker orchestration

## Requirements

- Docker
- Docker Compose

## Getting Started

1.  Clone the repository.
2.  Run the application:
    ```bash
    docker-compose up --build
    ```
3.  Access the application:
    - Frontend: http://localhost
    - Backend API: http://localhost/api
    - Django Admin: http://localhost/admin (You need to create a superuser first)

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
