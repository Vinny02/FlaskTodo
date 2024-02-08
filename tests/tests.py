from app import app, create_task, Task

def test_Task():
    testTask = Task("a test task")
    assert(testTask.text == "a test task")


