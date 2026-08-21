# Task Tracker CLI

A lightweight, robust command-line task management utility written in Python. It enables users to track, organize, and manage daily tasks efficiently using a local JSON persistence layer.

---

## 🌟 Key Features

* **Full CRUD Support**: Add, view, update, and delete tasks directly from the terminal.
* **Status Tracking**: Categorize tasks into three distinct states: `todo`, `in-progress`, or `done`.
* **Automatic Data Persistence**: Automatically creates and updates a local `tasks.json` file.
* **Smart Sequential ID Management**: Automatically re-indexes task IDs upon deletion to maintain continuous `1..N` ordering.
* **Robust Input Validation**: Safely handles invalid numerical options, empty text descriptions, and non-existent task IDs.
* **Zero Runtime Dependencies**: Core application is built entirely with Python standard libraries (`datetime`, `json`, `sys`).

---

## 🛠️ Prerequisites

* **Python 3.10** or higher (required for `match-case` syntax support).

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Omid-Zamzami/Task-tracker.git
cd Task-tracker
```

### 2. Install Dependencies (Optional for testing)

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python task_tracker.py
```

## 📋 JSON Data Structure

Tasks are saved in `tasks.json` using the following format:

```json
{
  "tasks": [
    {
      "id": 1,
      "description": "Complete project documentation",
      "status": "in-progress",
      "created_at": "2026-08-15 14:30:00",
      "updated_status_at": "2026-08-15 15:00:00"
    }
  ]
}
```

## 💻 Menu Options Overview

1. **Add task**: Prompt for description and status to create a new task.
2. **Update task**: Modify the description of an existing task by ID.
3. **Delete task**: Confirm and remove a task by ID while re-indexing remaining IDs.
4. **Mark task**: Update task status (`todo`, `in-progress`, `done`).
5. **Observe tasks**: Display all tasks or filter by status.
6. **Quit**: Safely exit the CLI program.

## 🧪 Running Tests

This project includes automated unit tests written with `pytest` covering CRUD operations, user input validation, data persistence, and ID re-indexing.

To execute the test suite:

```bash
pytest -v
```

## 📁 Repository Structure

```text
Task-tracker/
├── .gitignore          # Ignores cache directories and local JSON storage
├── README.md           # Project documentation
├── requirements.txt    # Testing dependencies
├── task_tracker.py     # Main application source code
└── test_task_tracker.py# Automated unit test suite
```

## License

This project is open-source and available under the [MIT License](LICENSE).