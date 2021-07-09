import main


def test_get_workout():
    assert main.get_workout(279811).status_code == 200

def test_get_workout_unexisting():
    assert main.get_workout_unexisting(279811222222).status_code == 404

def test_get_exercise():
    assert main.get_exercise(345).status_code == 200

def test_get_exercise_unexsisting():
    assert main.get_exercise(55555555).status_code == 404

def test_get_workouts():
    assert main.get_workouts().status_code == 200

def test_get_exercises():
    assert main.get_exercises().status_code == 200
