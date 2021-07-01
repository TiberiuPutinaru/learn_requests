import requests

import json

import toml

from requests.sessions import session

class mySession:

    s = requests.session()

    #baseURL
    
    base_URL = "https://wger.de/api/v2/"


    #loginURL

    loginURL="https://wger.de/en/user/login"


    #baseReferers

    base_workoutReferer = "https://wger.de/en/workout/"
    base_nutritionReferer = "https://wger.de/en/nutrition/"


    def __init__(self):
        cookies = self.login_and_cookies()
        self.csrftoken = cookies[0]
        self.sessionId = cookies[1]

        self.headers = {
        'Content-Type': 'application/json',
        'Referer': '',
        'X-CSRFToken' : self.csrftoken,
        'Authorization' : 'Token bd9ecc45b397f0e22bd0a8bd3304010ab4b586d8',
        'Cookie':f'csrftoken={self.csrftoken}; sessionid={self.sessionId}'
    }

    @classmethod
    def show_request_details(cls, response_list):
        print(response_list[1])
        print(f"status code: {response_list[0].status_code}")
        print(f"response : {response_list[0].content}")
        print("\n")
    
    def login_and_cookies(self):
         self.s.get(self.loginURL)
         csrftoken = self.s.cookies['csrftoken']
         sessionId = self.s.cookies['sessionid']
         self.payload = {
            'username': 'tiberiu1213',
            'password' : 'THeoTHEo2013&',
            'submit' : 'Login',
            'csrfmiddlewaretoken':csrftoken
            }
         self.loginResponse = self.s.post(self.loginURL,data = self.payload, headers=dict(Referer=self.loginURL))
         return [csrftoken,sessionId]

    #requests

    def get(self, type, id = None):
        
        get_URL = self.base_URL + type + "/"
        if id:
            get_URL += str(id)

        response_get = self.s.get(get_URL, headers = self.headers)

        return [response_get, mySession.check(response_get)]

    def post_workout(self):
        post_workoutURL = self.base_URL + "workout/"
        workout_post_headers = self.headers
        post_workoutReferer = self.base_workoutReferer + "overview/"
        workout_post_headers['Referer'] = post_workoutReferer
        
        response_post_workout = self.s.post(post_workoutURL, headers= workout_post_headers)
        return [response_post_workout, mySession.check(response_post_workout)]
    
    def post_training(self, workoutId, description, days):
        post_trainingURL = self.base_URL + "day/"
        training_post_headers = self.headers
        post_trainingReferer = self.base_workoutReferer + str(workoutId) + "/view/"
        training_post_headers['Referer'] = post_trainingReferer

        payload_training = {
            'training':workoutId,
            'description':f'{description}',
            'day':days
            }

        response_post_training = self.s.post(post_trainingURL, json= payload_training ,headers = training_post_headers)
        return [response_post_training, mySession.check(response_post_training)]
    
    def post_exercise(self, workoutId, exerciseday, exercises):
        post_exerciseURL = self.base_URL + "set/"
        exercise_post_headers = self.headers
        post_exerciseReferer = self.base_workoutReferer + str(workoutId) + "/view/"
        exercise_post_headers['Referer'] = post_exerciseReferer

        payload_exercise = {
            "exerciseday":exerciseday,
            "exercises":exercises
          }

        response_post_exercise = self.s.post(post_exerciseURL, json= payload_exercise ,headers= exercise_post_headers)
        return [response_post_exercise, mySession.check(response_post_exercise)]

    def post_nutritionplan(self):
        post_nutritionplanURL = self.base_URL + "nutritionplan/"
        nutritionplan_post_headers = self.headers
        post_nutritionplanReferer = self.base_nutritionReferer + "overview/"
        nutritionplan_post_headers['Referer'] = post_nutritionplanReferer

        response_post_nutritionplan = self.s.post(post_nutritionplanURL,headers= nutritionplan_post_headers)
        return [response_post_nutritionplan, mySession.check(response_post_nutritionplan)]

    def post_meal(self, nutritionplanId):
        post_mealURL = self.base_URL + "meal/"
        meal_post_headers = self.headers
        post_mealReferer = self.base_nutritionReferer + str(nutritionplanId) + "/view/"
        meal_post_headers['Referer'] = post_mealReferer

        payload_meal = {
        "plan":nutritionplanId
        }

        response_post_meal = self.s.post(post_mealURL, json = payload_meal , headers= meal_post_headers)
        return [response_post_meal,mySession.check(response_post_meal)]
    
    def post_mealitem(self, nutritionplanId, mealId, ingredientId, amount):
        post_mealitemURL = self.base_URL + "mealitem/"
        mealitem_post_headers = self.headers
        post_mealitemReferer = self.base_nutritionReferer + str(nutritionplanId) + "/view/"
        mealitem_post_headers['Referer'] = post_mealitemReferer

        payload_mealitem = {
        "meal":mealId,
        "ingredient":ingredientId,
        "amount":amount
        }

        response_post_mealitem = self.s.post(post_mealitemURL, json = payload_mealitem , headers=mealitem_post_headers )
        return [response_post_mealitem , mySession.check(response_post_mealitem)]
    
    #special requests

    def get_trainings(self, workoutId):
        get_trainingURL = self.base_URL + "day/"

        response_get_training = self.s.get(get_trainingURL, headers= self.headers)

        match_trainings =  []
        next_trainingURL = 0
        
        while  next_trainingURL != None:
            results = json.loads(response_get_training.text)['results']
            for result in results:
                if result['training'] == workoutId:
                    match_trainings.append(result)
            next_trainingURL = json.loads(response_get_training.text)['next']
            if next_trainingURL != None:
                response_get_training = self.s.get(next_trainingURL, headers= self.headers)

        return match_trainings

    def get_sets(self, trainingId):
        get_setURL = self.base_URL + "set/"

        response_get_set = self.s.get(get_setURL, headers= self.headers)

        match_sets =  []
        next_setURL = 0
        
        while  next_setURL != None:
            results = json.loads(response_get_set.text)['results']
            for result in results:
                if result['exerciseday'] == trainingId:
                    match_sets.append(result)
            next_setURL = json.loads(response_get_set.text)['next']
            if next_setURL != None:
                response_get_set = self.s.get(next_setURL, headers= self.headers)

        return match_sets
    
    def get_meals(self, planId):
        get_mealURL = self.base_URL + "meal/"

        response_get_meal = self.s.get(get_mealURL, headers= self.headers)

        match_meals =  []
        next_mealURL = 0
        
        while  next_mealURL != None:
            results = json.loads(response_get_meal.text)['results']
            for result in results:
                if result['plan'] == planId:
                    match_meals.append(result)
            next_mealURL = json.loads(response_get_meal.text)['next']
            if next_mealURL != None:
                response_get_meal = self.s.get(next_mealURL, headers= self.headers)

        return match_meals
    
    def get_mealitems(self, mealId):
        get_mealitemURL = self.base_URL + "mealitem/"

        response_get_mealitem = self.s.get(get_mealitemURL, headers= self.headers)

        match_mealitems =  []
        next_mealitemURL = 0
        
        while  next_mealitemURL != None:
            results = json.loads(response_get_mealitem.text)['results']
            for result in results:
                if result['meal'] == mealId:
                    match_mealitems.append(result)
            next_mealitemURL = json.loads(response_get_mealitem.text)['next']
            if next_mealitemURL != None:
                response_get_mealitem = self.s.get(next_mealitemURL, headers= self.headers)

        return match_mealitems

    
    def check(response):
        if (response.status_code == 200):
            return "Successful get request !"
        elif (response.status_code == 201):
            return "Successful post request !"
        else:
            return "Erorr, something went wrong."
    # @staticmethod
    # def dict_toml(req, dict, dict_el,dict_key):
    #         #if dict is not emtpy
    #         sub_dict = dict[dict_el]
    #         if bool(sub_dict):
    #             id = json.loads(req[0].text)['id']
    #             rez_dict = sub_dict[dict_key]
    #             return rez_dict
    
    def pass_toml(self,path):
        with open(path) as file:
            toml_data_dict = toml.load(file)

        workouts_dict = toml_data_dict.get('workouts')
        nutritionplans_dict = toml_data_dict.get('nutritionplans')

        if workouts_dict:
            for workout_value in workouts_dict.values():
                req_workout = self.post_workout()
                mySession.show_request_details(req_workout)
                if bool(workout_value):
                    workout_id = json.loads(req_workout[0].text)['id']
                    trainings_dict = workout_value.get('trainings')

                    for training_value in trainings_dict.values():
                        req_training = self.post_training(workout_id,training_value.get('description'),training_value.get('days'))
                        
                        mySession.show_request_details(req_training)
                        if(training_value.get('exercises')):
                            training_id = json.loads(req_training[0].text)['id']
                            exercises_dict = training_value.get('exercises')

                            for exercise_value in exercises_dict.values():
                                req_exercise = self.post_exercise(workout_id,training_id,exercise_value.get('exerciseid'))
                                mySession.show_request_details(req_exercise)

        if nutritionplans_dict:
            for nutritionplan_value in nutritionplans_dict.values():
                req_nutritionplan = self.post_nutritionplan()
                mySession.show_request_details(req_nutritionplan)
                if bool(nutritionplan_value):
                    nutritionplan_id = json.loads(req_nutritionplan[0].text)['id']
                    meals_dict = nutritionplan_value.get('meals')

                    for meal_value in meals_dict.values():
                        req_meal = self.post_meal(nutritionplan_id)
                        
                        mySession.show_request_details(req_meal)
                        if(meal_value.get('mealitems')):
                            meal_id = json.loads(req_meal[0].text)['id']
                            mealitems_dict = meal_value.get('mealitems')

                            for mealitem_value in mealitems_dict.values():
                                req_mealitem = self.post_mealitem(nutritionplan_id,meal_id,mealitem_value.get('ingredientid'),mealitem_value.get('amount'))
                                mySession.show_request_details(req_mealitem)
            




# session1 = mySession()

# req1 = session1.get("workout")
# req3 = session1.post_workout()
# req4 = session1.post_training(280895, 'mamamama', [6, 7])
# req5 = session1.post_exercise(280895, 142834, 279)
# req6 = session1.post_nutritionplan()
# req7 = session1.post_meal(75496)
# req8 = session1.post_mealitem(280895, 188455, 9842, 400)
# req9 = session1.get("workout",279811)
# req11 = session1.get("exercise")
# req12 = session1.get("exercise", 345)
# req13 = session1.get("nutritionplan")
# req14 = session1.get("nutritionplan",75157)
# req15 = session1.get("meal")
# req16 = session1.get("meal",187530)

# reqs = [req1 , req3 ,req4 ,req5, req6, req7, req8, req9, req11, req12,req13, req14, req15, req16]

# for req in reqs:
#     mySession.show_request_details(req)

# req17 = session1.get_trainings(281244)
# req18 = session1.get_meals(75256)
# req19 = session1.get_mealitems(188373)
# req20 = session1.get_sets(142338)
# print(req17)
# print(req18)
# print(req19)
# print(req20)


#login
# loginURL = "https://wger.de/en/user/login"

# s=mySession.s
# a = s.get(loginURL)
# csrftoken = s.cookies['csrftoken']
# sessionId = s.cookies['sessionid']
# print(csrftoken)
# print('\n')


# payload = {
#     'username': 'tiberiu1213',
#     'password' : 'THeoTHEo2013&',
#     'submit' : 'Login',
#     'csrfmiddlewaretoken':csrftoken
# }



# response = s.post(loginURL,data = payload, headers=dict(Referer=loginURL))
# #print(response.status_code)
# print(response.content)

#getworkout

# get_workoutURL = "https://wger.de/api/v2/workout"
# response1 = s.get(get_workoutURL)
# # print(response1.status_code)
# # print(response1.content)
# # print("\n")


# #getexercise

# get_exerciseURL = "https://wger.de/api/v2/exercise"
# response2 = s.get(get_exerciseURL)
# # print(response2.status_code)
# # print(response2.content)

# #getaspecificworkout

# get_spworkoutURL = "https://wger.de/api/v2/workout/279811"
# response3 = s.get(get_spworkoutURL)
# print(response3.status_code)
# print(response3.content)

# #getaspecificexercise

# get_spexerciseURL = "https://wger.de/api/v2/exercise/345"
# response4 = s.get(get_spexerciseURL)
# # print(response4.status_code)
# # print(response4.content)

# #getnutritionplan

# get_nutritionplanURL = "https://wger.de/api/v2/nutritionplan/"
# response5 = s.get(get_nutritionplanURL)
# # print(response5.status_code)
# # print(response5.content)
# # print("\n")

# #getmeal

# get_mealURL = "https://wger.de/api/v2/meal"
# response6 = s.get(get_mealURL)
# # print(response6.status_code)
# # print(response6.content)
# # print("\n")

# #getspecific nutrition plan

# get_spnutritionplanURL = "https://wger.de/api/v2/nutritionplan/75157"
# response7 = s.get(get_spnutritionplanURL)
# # print(response7.status_code)
# # print(response7.content)
# # print("\n")

# #getspecific meal

# get_spmealURL = "https://wger.de/api/v2/meal/187530"
# response8 = s.get(get_spmealURL)
# print(response8.status_code)
# print(response8.content)
# print("\n")

#post workout

# post_workoutURL = "https://wger.de/api/v2/workout/"
# post_workoutReferer = "https://wger.de/en/workout/overview"
# post_workout_headers = {
#     'Content-Type': 'application/json',
#     'Referer': post_workoutReferer,
#     'X-CSRFToken' : csrftoken,
#     'Authorization' : 'Token bd9ecc45b397f0e22bd0a8bd3304010ab4b586d8',
#     'Cookie':f'csrftoken={csrftoken}; sessionid={sessionId}'
# }
# response9 = s.post(post_workoutURL, headers=post_workout_headers)
# print(response9.status_code)
# print(response9.content)
# #print(response9.cookies)
# print("\n")

#post add training to workout

# payload_training = {
#     'training':280895,
#     'description':'ssssssssssss',
#     'day':[6,7]
# }

# post_trainingURL = "https://wger.de/api/v2/day/"
# post_trainingReferer = "https://wger.de/en/workout/280895/view/"
# post_training_headers = {
#     'Content-Type': 'application/json',
#     'Referer': post_trainingReferer,
#     'X-CSRFToken' : csrftoken,
#     'Authorization' : 'Token bd9ecc45b397f0e22bd0a8bd3304010ab4b586d8',
#     'Cookie':f'csrftoken={csrftoken}; sessionid={sessionId}'
# }
# response10 = s.post(post_trainingURL, json = payload_training, headers=post_training_headers)
# print(response10.status_code)
# print(response10.content)
# print("\n")