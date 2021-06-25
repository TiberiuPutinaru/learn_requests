import requests

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
         mySession.s.get(self.loginURL)
         csrftoken = mySession.s.cookies['csrftoken']
         sessionId = mySession.s.cookies['sessionid']
         self.payload = {
            'username': 'tiberiu1213',
            'password' : 'THeoTHEo2013&',
            'submit' : 'Login',
            'csrfmiddlewaretoken':csrftoken
            }
         self.loginResponse = mySession.s.post(self.loginURL,data = self.payload, headers=dict(Referer=self.loginURL))
         return [csrftoken,sessionId]

    #requests

    def get_workout(self, workoutId = None):
        get_workoutURL = self.base_URL + "workout/"
        if workoutId is not None:
            get_workoutURL += str(workoutId)
        response_get_workout = mySession.s.get(get_workoutURL, headers = self.headers)
        return [response_get_workout, mySession.check_get(response_get_workout)]
    
    def get_exercise(self, exerciseId = None):
        get_exerciseURL = self.base_URL + "exercise/"
        if exerciseId is not None:
            get_exerciseURL += str(exerciseId)
        response_get_exercise = mySession.s.get(get_exerciseURL, headers= self.headers)
        return [response_get_exercise, mySession.check_get(response_get_exercise)]
    
    def get_nutritionplan(self, nutritionplanId = None):
        get_nutritionplanURL = self.base_URL + "nutritionplan/"
        if nutritionplanId is not None:
            get_nutritionplanURL += str(nutritionplanId)
        response_get_nutritionplan = mySession.s.get(get_nutritionplanURL, headers= self.headers)
        return [response_get_nutritionplan, mySession.check_get(response_get_nutritionplan)]

    def get_meal(self, mealId = None):
        get_mealURL = self.base_URL + "meal/"
        if mealId is not None:
            get_mealURL += str(mealId)
        response_get_meal = mySession.s.get(get_mealURL, headers= self.headers)
        return [response_get_meal, mySession.check_get(response_get_meal)]

    def post_workout(self):
        post_workoutURL = self.base_URL + "workout/"
        workout_post_headers = self.headers
        post_workoutReferer = self.base_workoutReferer + "overview/"
        workout_post_headers['Referer'] = post_workoutReferer
        
        response_post_workout = mySession.s.post(post_workoutURL, headers= workout_post_headers)
        return [response_post_workout, mySession.check_post(response_post_workout)]
    
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

        response_post_training = mySession.s.post(post_trainingURL, json= payload_training ,headers = training_post_headers)
        return [response_post_training, mySession.check_post(response_post_training)]
    
    def post_exercise(self, workoutId, exerciseday, exercises):
        post_exerciseURL = self.base_URL + "set/"
        exercise_post_headers = self.headers
        post_exerciseReferer = self.base_workoutReferer + str(workoutId) + "/view/"
        exercise_post_headers['Referer'] = post_exerciseReferer

        payload_exercise = {
            "exerciseday":exerciseday,
            "exercises":exercises
          }

        response_post_exercise = mySession.s.post(post_exerciseURL, json= payload_exercise ,headers= exercise_post_headers)
        return [response_post_exercise, mySession.check_post(response_post_exercise)]

    def post_nutritionplan(self):
        post_nutritionplanURL = self.base_URL + "nutritionplan/"
        nutritionplan_post_headers = self.headers
        post_nutritionplanReferer = self.base_nutritionReferer + "overview/"
        nutritionplan_post_headers['Referer'] = post_nutritionplanReferer

        response_post_nutritionplan = mySession.s.post(post_nutritionplanURL,headers= nutritionplan_post_headers)
        return [response_post_nutritionplan, mySession.check_post(response_post_nutritionplan)]

    def post_meal(self, nutritionplanId):
        post_mealURL = self.base_URL + "meal/"
        meal_post_headers = self.headers
        post_mealReferer = self.base_nutritionReferer + str(nutritionplanId) + "/view/"
        meal_post_headers['Referer'] = post_mealReferer

        payload_meal = {
        "plan":nutritionplanId
        }

        response_post_meal = mySession.s.post(post_mealURL, json = payload_meal , headers= meal_post_headers)
        return [response_post_meal,mySession.check_post(response_post_meal)]
    
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

        response_post_mealitem = mySession.s.post(post_mealitemURL, json = payload_mealitem , headers=mealitem_post_headers )
        return [response_post_mealitem , mySession.check_post(response_post_mealitem)]
    
    @staticmethod
    def check_get(response):
        if (response.status_code == 200):
            return "Successful get request !"
        else:
            return "Erorr, something went wrong."
    @staticmethod
    def check_post(response):
        if (response.status_code == 201):
            return "Successful post request !"
        else:
            return "Erorr, something went wrong."



session1 = mySession()

req1 = session1.get_workout()
req3 = session1.post_workout()
req4 = session1.post_training(280895, 'mamamama', [6, 7])
req5 = session1.post_exercise(280895, 142834, 279)
req6 = session1.post_nutritionplan()
req7 = session1.post_meal(75496)
req8 = session1.post_mealitem(280895, 188455, 9842, 400)
req9 = session1.get_workout(279811)
req11 = session1.get_exercise()
req12 = session1.get_exercise(345)
req13 = session1.get_nutritionplan()
req14 = session1.get_nutritionplan(75157)
req15 = session1.get_meal()
req16 = session1.get_meal(187530)
reqs = [req1 , req3 ,req4 ,req5, req6, req7, req8, req9, req11, req12,req13, req14, req15, req16]

for req in reqs:
    mySession.show_request_details(req)



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