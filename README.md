# Habij Backend

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/gethabij/habij-backend.git
cd habij
```

### 2. Install Dependencies

Ensure you have Poetry installed. Then run:

```bash
poetry install
```

Activate the virtual environment:

```bash
poetry shell
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Run the Development Server

```bash
python manage.py runserver
```

Open your browser at `http://127.0.0.1:8000`.

---

## Tools and Configuration

### Pre-commit Hooks

Pre-commit is configured to run linting and formatting checks before every commit. To set it up:

```bash
pre-commit install
```

Run all hooks manually:

```bash
pre-commit run --all-files
```

### Ruff Configuration

Run Ruff manually:

```bash
ruff check .
```

---

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).

