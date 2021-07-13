
from session import mySession
import json
import pytest
from random import randint
session1 = mySession()


def get_workout(workoutId):
    req = session1.get("workout",workoutId)
    return mySession.show_request_details(req)

def get_workout_unexisting(workoutId):
    req = session1.get("workout",workoutId)
    return mySession.show_request_details(req)

def get_training(trainingId):
    req = session1.get("day",trainingId)
    return mySession.show_request_details(req)

def get_training_unexisting(workoutId):
    req = session1.get("day",workoutId)
    return mySession.show_request_details(req)

def get_exercise(exerciseId):
    req = session1.get("set",exerciseId)
    return mySession.show_request_details(req)

def get_exercise_unexisting(exerciseId):
    req = session1.get("exercise",exerciseId)
    return mySession.show_request_details(req)

def get_workouts():
    req = session1.get("workout")
    return mySession.show_request_details(req)

def get_exercises():
    req = session1.get("exercise")
    return mySession.show_request_details(req)

# def post_workout():
#     req = session1.post_workout()
#     id = json.loads(req[0].text).get('id')
#     response = get_workout(id)
#     return response

# def post_training(workoutId, description, days):
#     req = session1.post_training(workoutId, description, days)
#     return mySession.show_request_details(req)

def post_training_unexisting_workout(workoutId, description='tsaa', days= [6,7]):
    req = session1.post_training(workoutId, description, days)
    return mySession.show_request_details(req)

def post_exercise_unexisting_training_or_workout(workoutId,trainingId, exerciseId=345):
    req = session1.post_exercise(workoutId, trainingId, exerciseId)
    return mySession.show_request_details(req)

def post_exercise_unexisting_exercise(workoutId,trainingId, exerciseId):
    req = session1.post_exercise(workoutId, trainingId, exerciseId)
    return mySession.show_request_details(req)

def delete_workout(workoutId):
    req = session1.delete_item("workout", workoutId)
    return mySession.show_request_details(req)


@pytest.fixture()
def clear(request):
    def myteardown():
        session1.cleanUp()
    request.addfinalizer(myteardown)

def get_random_id(rand, ids):
    check = False
    while(check != True):
        random_id= rand
        if random_id not in ids:
            check = True
    return random_id
def post_many_objects(toml, type):
    session1.pass_toml(toml)
    if type == 'workout':
        id = json.loads(session1.req_toml_workout.text).get('id')
    elif type =='training':
        id = json.loads(session1.req_toml_training.text).get('id')
    elif type == 'exercise':
        id = json.loads(session1.req_toml_exercise.text).get('id')
    return id

class TestWorkout:
  
    def test_get_workout(self, clear):
        session1.pass_toml('data_workout.toml')
        id = json.loads(session1.req_toml_workout.text).get('id')
        assert get_workout(id).status_code == 200

    def test_get_workout_unexisting(self, clear):
        workout_ids = session1.get_ids("workout")
        random_id = get_random_id(randint(100000, 999999),workout_ids)

        assert get_workout(random_id).status_code == 404

    def test_get_training(self, clear):
        session1.pass_toml('data_training.toml')
        id = json.loads(session1.req_toml_training.text).get('id')
        assert get_training(id).status_code == 200
    
    def test_get_training_unexisting(self, clear):
        training_ids = session1.get_ids("day")
        random_id = get_random_id(randint(100000, 999999),training_ids)

        assert get_training(random_id).status_code == 404

    def test_get_exercise(self, clear):
        session1.pass_toml('data_exercise.toml')
        id = json.loads(session1.req_toml_exercise.text).get('id')
        assert get_exercise(id).status_code == 200

    def test_get_exercise_unexsisting(self, clear):
        exercise_ids = session1.get_ids("set")
        check = False
        random_id = get_random_id(randint(100000, 999999),exercise_ids)
        assert get_exercise(random_id).status_code == 404

    def test_get_workouts(self, clear):
        assert get_workouts().status_code == 200

    def test_get_exercises(self, clear):
        assert get_exercises().status_code == 200

    def test_post_workout(self, clear):
        session1.pass_toml('data_workout.toml')
        id = json.loads(session1.req_toml_workout.text).get('id')
        assert get_workout(id).status_code == 200

    def test_post_training(self, clear):
        session1.pass_toml('data_training.toml')
        id = json.loads(session1.req_toml_training.text).get('id')
        assert get_training(id).status_code == 200

    def test_post_training_unexisting_workout(self, clear):
        workout_ids = session1.get_ids("workout")
        random_id = get_random_id(randint(100000, 999999),workout_ids)
        assert post_training_unexisting_workout(random_id).status_code != 201
    
    def test_post_training_unexisting_days(self, clear):
        session1.pass_toml('data_training_unexisting_days.toml')
        assert session1.req_toml_training.status_code != 201

    def test_post_exercise(self, clear):
        session1.pass_toml('data_exercise.toml')
        id = json.loads(session1.req_toml_exercise.text).get('id')
        assert get_exercise(id).status_code == 200

    def test_post_exercise_unexisting_training(self, clear):
        session1.pass_toml('data_workout.toml')
        workoutId = json.loads(session1.req_toml_workout.text).get('id')
        training_ids = session1.get_ids("day")
        random_id = get_random_id(randint(100000, 999999),training_ids)
        assert post_exercise_unexisting_training_or_workout(workoutId, random_id).status_code != 201

    def test_post_exercise_unexisting_workout(self, clear):
        session1.pass_toml('data_training.toml')
        trainingId = json.loads(session1.req_toml_training.text).get('id')
        workout_ids = session1.get_ids("workout")
        random_id = get_random_id(randint(100000, 999999),workout_ids)
        assert post_exercise_unexisting_training_or_workout(random_id, trainingId).status_code != 201
    
    def test_post_exercise_unexisting_exercise(self, clear):
        session1.pass_toml('data_training.toml')
        trainingId = json.loads(session1.req_toml_training.text).get('id')
        workoutId = json.loads(session1.req_toml_training.text).get('training')
        
        exercise_ids = session1.get_ids("exercise")
        random_id = get_random_id(randint(100, 999),exercise_ids)
        
        assert post_exercise_unexisting_training_or_workout(workoutId, trainingId,random_id).status_code != 201
    
    def test_many_workout_posts(self, clear):
        for i in range (0,100):
            id = post_many_objects('data_workout.toml', 'workout')
            assert get_workout(id).status_code == 200

    def test_many_training_posts(self, clear):
        for i in range (0,100):
            id = post_many_objects('data_training.toml', 'training')
            assert get_training(id).status_code == 200
    
    def test_many_exercise_posts(self, clear):
        for i in range (0,100):
            id = post_many_objects('data_exercise.toml', 'exercise')
            assert get_exercise(id).status_code == 200
    
    def test_delete_workout(self, clear):
        session1.pass_toml('data_workout.toml')
        id = json.loads(session1.req_toml_workout.text).get('id')
        delete_workout(id)
        assert get_workout(id).status_code == 404
    

    
    