# Project: bortelid-web

## Technical Stack
- **Language:** Python 3.12 (managed by `uv`)
- **Framework:** py4web (Bottle-based)
- **Database:** MySQL (via `pymysql`)
- **Dependency Manager:** `uv`

## Project Structure & Routing
- **Core App:** Located in `apps/_scaffold/`
- **Controller Pattern:** 
    - Individual controller logic must be developed in the `apps/_scaffold/controllers/` directory.
    - To make a controller visible to py4web, it **must** be imported into `apps/_scaffold/controllers.py`.
- **Views/Templates:** Located in `apps/_scaffold/templates/`
- **Static Assets:** Located in `apps/_scaffold/static/`

## Database Management
- **Connection:** Configured via `DB_URI` in `apps/_scaffold/settings.py`.
- **Schema Definitions:** All table definitions and database structures must be stored as files within `apps/_scaffold/databases/`.
- **Workflow:** When adding new tables or modifying existing ones, update the corresponding file in `_scaffold/databases/` to maintain a source of truth for the schema.
- **Library:** Use `pymysql` for underlying connectivity.

## Development Commands
- **Install Dependencies:** `uv sync`
- **Run Server:** `python run.py`
- **Run Tests:** `uv run pytest`
- **Add Package:** `uv add <package_name>`

## Coding Standards
- **MVC Separation:** Strictly maintain the separation between `controllers/` (logic), `templates/` (UI), and `databases/` (schema).
- **Imports:** When creating a new feature, always check if the controller is exported in `controllers.py`.
- **Typing:** Use Python type hints for all function signatures to ensure stability.

## AI Permissions & Tool Use
- **Read Access:** The AI has standing permission to read any file within the project root and the `.venv` directory for the purpose of understanding library implementations.
- **Write Access:** The AI must still ask for permission before modifying files in `apps/` or `config/`.
- **Execution:** The AI is permitted to run `uv run` commands for read-only tasks (like `ls` or `cat`) without explicit confirmation.

- **CRITICAL:** `apps/_scaffold/controllers.py` is the application's dispatcher. NEVER empty this file. Whenever a new controller file is created in `controllers/`, it MUST be imported into `controllers.py` using `from .controllers.filename import *`.

