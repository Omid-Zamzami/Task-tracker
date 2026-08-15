import json
import pytest
import task_tracker


@pytest.fixture(autouse=True)
def setup_and_teardown(tmp_path, monkeypatch):
    """
    Fixture to isolate test environment:
    - Redirects JSON persistence to a temporary file.
    - Resets global state (tasks_list, next_id) before each test.
    """
    test_file = tmp_path / "test_tasks.json"
    monkeypatch.setattr(task_tracker, "FILENAME", str(test_file))
    
    # Reset in-memory global state
    task_tracker.tasks_list.clear()
    task_tracker.tasks_dict["tasks"] = task_tracker.tasks_list
    task_tracker.next_id = 1

    yield


# CREATE (ADD TASK) TESTS

def test_add_task_success(monkeypatch, capsys):
    """Test adding a task with valid description and status."""
    inputs = iter(["Write unit tests", "todo"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    task_tracker.add_task()

    assert len(task_tracker.tasks_list) == 1
    added_task = task_tracker.tasks_list[0]
    assert added_task["id"] == 1
    assert added_task["description"] == "Write unit tests"
    assert added_task["status"] == "todo"
    assert "created_at" in added_task

    captured = capsys.readouterr()
    assert "Task 'Write unit tests' created successfully!" in captured.out


def test_add_task_invalid_then_valid_input(monkeypatch):
    """Test retry prompts for empty description and invalid status."""
    # First empty description, then valid; first invalid status, then valid
    inputs = iter(["", "Buy milk", "invalid_status", "in-progress"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    task_tracker.add_task()

    assert len(task_tracker.tasks_list) == 1
    assert task_tracker.tasks_list[0]["description"] == "Buy milk"
    assert task_tracker.tasks_list[0]["status"] == "in-progress"


# READ (OBSERVE TASK) TESTS

def test_observe_task_all(monkeypatch, capsys):
    """Test displaying all tasks regardless of status."""
    task_tracker.tasks_list.extend([
        {"id": 1, "description": "Task 1", "status": "todo", "created_at": "2026-08-15 10:00:00"},
        {"id": 2, "description": "Task 2", "status": "done", "created_at": "2026-08-15 11:00:00"},
    ])

    monkeypatch.setattr("builtins.input", lambda _: "all")
    task_tracker.observe_task()

    captured = capsys.readouterr()
    assert "Task 1" in captured.out
    assert "Task 2" in captured.out


def test_observe_task_filter_by_status(monkeypatch, capsys):
    """Test filtering tasks by specific status."""
    task_tracker.tasks_list.extend([
        {"id": 1, "description": "Task 1", "status": "todo", "created_at": "2026-08-15 10:00:00"},
        {"id": 2, "description": "Task 2", "status": "done", "created_at": "2026-08-15 11:00:00"},
    ])

    monkeypatch.setattr("builtins.input", lambda _: "done")
    task_tracker.observe_task()

    captured = capsys.readouterr()
    assert "Task 2" in captured.out
    assert "Task 1" not in captured.out


# UPDATE TESTS

def test_update_task_description(monkeypatch):
    """Test updating the description of an existing task."""
    task_tracker.tasks_list.append({
        "id": 1,
        "description": "Old description",
        "status": "todo",
        "created_at": "2026-08-15 10:00:00"
    })

    inputs = iter(["1", "Updated description"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    task_tracker.update_task()

    assert task_tracker.tasks_list[0]["description"] == "Updated description"
    assert "updated_description_at" in task_tracker.tasks_list[0]


def test_mark_task_status(monkeypatch):
    """Test updating the execution status of a task."""
    task_tracker.tasks_list.append({
        "id": 1,
        "description": "Study Python",
        "status": "todo",
        "created_at": "2026-08-15 10:00:00"
    })

    inputs = iter(["1", "done"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    task_tracker.mark_task()

    assert task_tracker.tasks_list[0]["status"] == "done"
    assert "updated_status_at" in task_tracker.tasks_list[0]


# DELETE TESTS & RE-INDEXING

def test_delete_task_with_reindexing(monkeypatch):
    """Test deleting a task and ensuring continuous 1..N ID re-indexing."""
    task_tracker.tasks_list.extend([
        {"id": 1, "description": "Task A", "status": "todo", "created_at": "2026-08-15 10:00:00"},
        {"id": 2, "description": "Task B", "status": "in-progress", "created_at": "2026-08-15 10:05:00"},
        {"id": 3, "description": "Task C", "status": "done", "created_at": "2026-08-15 10:10:00"},
    ])
    task_tracker.next_id = 4

    # Delete ID 2, confirm with 'yes'
    inputs = iter(["2", "yes"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    task_tracker.delete_task()

    assert len(task_tracker.tasks_list) == 2
    assert task_tracker.tasks_list[0]["id"] == 1
    assert task_tracker.tasks_list[0]["description"] == "Task A"
    
    # Task C should be re-indexed from ID 3 to ID 2
    assert task_tracker.tasks_list[1]["id"] == 2
    assert task_tracker.tasks_list[1]["description"] == "Task C"
    assert task_tracker.next_id == 3


def test_delete_task_cancelled(monkeypatch):
    """Test cancelling deletion prompt when choice is 'no'."""
    task_tracker.tasks_list.append({
        "id": 1,
        "description": "Important task",
        "status": "todo",
        "created_at": "2026-08-15 10:00:00"
    })

    inputs = iter(["1", "n"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    task_tracker.delete_task()

    assert len(task_tracker.tasks_list) == 1
    assert task_tracker.tasks_list[0]["description"] == "Important task"


# SYSTEM & PERSISTENCE TESTS

def test_save_tasks_writes_json():
    """Test that save_tasks writes valid JSON data to disk."""
    task_tracker.tasks_list.append({
        "id": 1,
        "description": "Persist data",
        "status": "todo",
        "created_at": "2026-08-15 10:00:00"
    })

    task_tracker.save_tasks()

    with open(task_tracker.FILENAME, "r") as f:
        data = json.load(f)

    assert "tasks" in data
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["description"] == "Persist data"


def test_quit_task_tracker(monkeypatch):
    """Test application termination prompt on exit."""
    monkeypatch.setattr("builtins.input", lambda _: "y")

    with pytest.raises(SystemExit):
        task_tracker.quit_task_tracker()