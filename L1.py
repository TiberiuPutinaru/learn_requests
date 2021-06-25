import requests

from requests.sessions import session

s = requests.session()

class mySession:
    
    #get Urls

    loginURL="https://wger.de/en/user/login"
    get_workoutURL = "https://wger.de/api/v2/workout"
    get_exerciseURL = "https://wger.de/api/v2/exercise"
    get_spworkoutURL = "https://wger.de/api/v2/workout/279811"
    get_spexerciseURL = "https://wger.de/api/v2/exercise/345"
    get_nutritionplanURL = "https://wger.de/api/v2/nutritionplan/"
    get_mealURL = "https://wger.de/api/v2/meal"
    get_spnutritionplanURL = "https://wger.de/api/v2/nutritionplan/75157"
    get_spmealURL = "https://wger.de/api/v2/meal/187530"

    #post Urls

    post_workoutURL = "https://wger.de/api/v2/workout/"
    post_trainingURL = "https://wger.de/api/v2/day/"
    post_exerciseURL ="https://wger.de/api/v2/set/"
    post_nutritionplanURL = "https://wger.de/api/v2/nutritionplan/"
    post_mealURL = "https://wger.de/api/v2/meal/"
    post_mealitemURL = "https://wger.de/api/v2/mealitem/"

    #Referers

    post_workoutReferer = "https://wger.de/en/workout/overview"
    post_trainingReferer = "https://wger.de/en/workout/280895/view/"
    post_exerciseReferer = "https://wger.de/en/workout/280895/view"
    post_nutritionplanReferer = "https://wger.de/en/nutrition/overview/"
    post_mealReferer = "https://wger.de/en/nutrition/75441/view/"
    post_mealitemReferer = "https://wger.de/en/nutrition/75441/view/"

    #Headers

    def func_post_workout_headers(self):
        self.post_workout_headers = {
        'Content-Type': 'application/json',
        'Referer': self.post_workoutReferer,
        'X-CSRFToken' : self.csrftoken,
        'Authorization' : 'Token bd9ecc45b397f0e22bd0a8bd3304010ab4b586d8',
        'Cookie':f'csrftoken={self.csrftoken}; sessionid={self.sessionId}'
    }
        return self.post_workout_headers

    def func_post_training_headers(self):
        self.post_training_headers = {
        'Content-Type': 'application/json',
        'Referer': self.post_trainingReferer,
        'X-CSRFToken' : self.csrftoken,
        'Authorization' : 'Token bd9ecc45b397f0e22bd0a8bd3304010ab4b586d8',
        'Cookie':f'csrftoken={self.csrftoken}; sessionid={self.sessionId}'
    }
        return self.post_training_headers
    
    def func_post_exercise_headers(self):
        self.post_exercise_headers = {
        'Content-Type': 'application/json',
        'Referer': self.post_exerciseReferer,
        'X-CSRFToken' : self.csrftoken,
        'Authorization' : 'Token bd9ecc45b397f0e22bd0a8bd3304010ab4b586d8',
        'Cookie':f'csrftoken={self.csrftoken}; sessionid={self.sessionId}'
    }
        return self.post_exercise_headers
    
    def func_post_nutritionplan_headers(self):
        self.post_nutritionplan_headers = {
        'Content-Type': 'application/json',
        'Referer': self.post_nutritionplanReferer,
        'X-CSRFToken' : self.csrftoken,
        'Authorization' : 'Token bd9ecc45b397f0e22bd0a8bd3304010ab4b586d8',
        'Cookie':f'csrftoken={self.csrftoken}; sessionid={self.sessionId}'
    }
        return self.post_nutritionplan_headers
    
    def func_post_meal_headers(self):
        self.post_meal_headers = {
        'Content-Type': 'application/json',
        'Referer': self.post_mealReferer,
        'X-CSRFToken' : self.csrftoken,
        'Authorization' : 'Token bd9ecc45b397f0e22bd0a8bd3304010ab4b586d8',
        'Cookie':f'csrftoken={self.csrftoken}; sessionid={self.sessionId}'
    }
        return self.post_meal_headers
    
    def func_post_mealitem_headers(self):
        self.post_mealitem_headers = {
        'Content-Type': 'application/json',
        'Referer': self.post_mealitemReferer,
        'X-CSRFToken' : self.csrftoken,
        'Authorization' : 'Token bd9ecc45b397f0e22bd0a8bd3304010ab4b586d8',
        'Cookie':f'csrftoken={self.csrftoken}; sessionid={self.sessionId}'
    }
        return self.post_mealitem_headers

    #payloads

    payload_training = {
    'training':280895,
    'description':'ssssssssssss',
    'day':[6,7]
}
    payload_exercise = {
    "exerciseday":142728,
    "exercises":279
}

    payload_meal = {
        "plan":75441
}

    payload_mealitem = {
    "meal":188373,
    "ingredient":9842,
    "amount":200
}

    def __init__(self):
        s.get(self.loginURL)
        self.csrftoken = s.cookies['csrftoken']
        self.sessionId = s.cookies['sessionid']

        self.payload = {
            'username': 'tiberiu1213',
            'password' : 'THeoTHEo2013&',
            'submit' : 'Login',
            'csrfmiddlewaretoken':self.csrftoken
            }

        self.loginResponse = s.post(self.loginURL,data = self.payload, headers=dict(Referer=self.loginURL))
        
    @classmethod
    def show_request_details(cls,response):
        print(response.status_code)
        print(response.content)
        print("\n")
    
    #requests

    def get_workout(self):
        self.response_get_workout = s.get(self.get_workoutURL)
        return self.response_get_workout
    
    def get_exercise(self):
        self.response_get_exercise = s.get(self.get_exerciseURL)
        return self.response_get_exercise

    def get_spworkout(self):
        self.response_get_spworkout = s.get(self.get_spworkoutURL)
        return self.response_get_spworkout
    
    def get_spexercise(self):
        self.response_get_spexercise = s.get(self.get_spexerciseURL)
        return self.response_get_spexercise
    
    def get_nutritionplan(self):
        self.response_get_nutritionplan = s.get(self.get_nutritionplanURL)
        return self.response_get_nutritionplan

    def get_meal(self):
        self.response_get_meal = s.get(self.get_mealURL)
        return self.response_get_meal

    def get_spnutritionplan(self):
        self.response_get_spnutritionplan = s.get(self.get_spnutritionplanURL)
        return self.response_get_spnutritionplan
    
    def get_spmeal(self):
        self.response_get_spmeal = s.get(self.get_spmealURL)
        return self.response_get_spmeal

    def post_workout(self):
        self.response_post_workout = s.post(self.post_workoutURL, headers= self.func_post_workout_headers())
        return self.response_post_workout
    
    def post_training(self):
        self.response_post_training = s.post(self.post_trainingURL, json= self.payload_training ,headers= self.func_post_training_headers())
        return self.response_post_training
    
    def post_exercise(self):
        self.response_post_exercise = s.post(self.post_exerciseURL, json= self.payload_exercise ,headers= self.func_post_exercise_headers())
        return self.response_post_exercise

    def post_nutritionplan(self):
        self.response_post_nutritionplan = s.post(self.post_nutritionplanURL,headers= self.func_post_nutritionplan_headers())
        return self.response_post_nutritionplan

    def post_meal(self):
        self.response_post_meal = s.post(self.post_mealURL, json = self.payload_meal , headers= self.func_post_meal_headers())
        return self.response_post_meal
    
    def post_mealitem(self):
        self.response_post_mealitem = s.post(self.post_mealitemURL, json = self.payload_mealitem , headers= self.func_post_mealitem_headers())
        return self.response_post_mealitem


session1 = mySession()

req1 = session1.get_workout()
req2 = session1.get_spmeal()
req3 = session1.post_workout()
req4 = session1.post_training()
req5 = session1.post_exercise()
req6 = session1.post_nutritionplan()
req7 = session1.post_meal()
req8 = session1.post_mealitem()

reqs = [req1 , req2, req3 ,req4 ,req5, req6, req7, req8]

for req in reqs:
    mySession.show_request_details(req)



#login
# loginURL = "https://wger.de/en/user/login"

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
#print(response.content)

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
# # print(response3.status_code)
# # print(response3.content)

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