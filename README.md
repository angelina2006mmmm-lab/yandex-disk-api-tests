# Yandex Disk API autotests

Test project for the Yandex Fintech QA Automation internship assignment.

The project checks Yandex Disk REST API using the required stack:

- Python 3
- Pytest
- requests

Additional tool:

- Allure Pytest for test reporting

## What is covered

The suite contains integration tests for all required HTTP methods:

| Method | Scenario |
| --- | --- |
| GET | Get disk information and resource metadata |
| POST | Copy a folder |
| PUT | Create a folder |
| DELETE | Delete a folder |

Negative checks are also included:

- GET for a missing resource returns `404`
- PUT for an already existing folder returns `409`

API base URL:

```text
https://cloud-api.yandex.net/v1/disk
```

## Important security note

Do not use a personal Yandex account for this assignment.

Create or use a separate test account and obtain an OAuth token for that test account. Never commit the real token to GitHub.

The project reads the token from the `YANDEX_DISK_TOKEN` environment variable.

## Project structure

```text
yandex-disk-api-tests/
├── yandex_disk/
│   ├── __init__.py
│   └── client.py
├── tests/
│   ├── conftest.py
│   ├── test_delete.py
│   ├── test_get.py
│   ├── test_post.py
│   └── test_put.py
├── .env.example
├── .gitignore
├── pytest.ini
├── README.md
└── requirements.txt
```

## Local installation

Python 3.10+ is recommended.

Clone the repository and open the project directory:

```bash
git clone <your-public-github-repository-url>
cd yandex-disk-api-tests
```

Create a virtual environment:

### Linux / macOS / WSL

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Configure the token

Copy the example environment file:

### Linux / macOS / WSL

```bash
cp .env.example .env
```

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

Edit `.env`:

```text
YANDEX_DISK_TOKEN=your_test_account_oauth_token
```

The `.env` file is ignored by Git.

## Run tests

```bash
pytest
```

Verbose run:

```bash
pytest -v
```

If the token is not configured, the integration tests are skipped with an explanatory message.

## Allure report

Generate Allure results:

```bash
pytest --alluredir=allure-results
```

If the Allure CLI is installed, open the report:

```bash
allure serve allure-results
```

## Test design notes

- Every test uses a unique resource name to reduce collisions between runs.
- Test data is cleaned up after scenarios where possible.
- OAuth credentials are not stored in source code.
- Assertions cover both HTTP status codes and important response fields.
- The API client is separated from the tests so the suite is easier to maintain.

## Official documentation

Yandex Disk REST API:

```text
https://yandex.ru/dev/disk/rest/
```

Yandex Disk Polygon:

```text
https://yandex.ru/dev/disk/poligon/
```

API host:

```text
https://cloud-api.yandex.net
```
