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
        
        #extract csrftoken and sessionId
        self.csrftoken = cookies[0]
        self.sessionId = cookies[1]

        #create login header
        self.headers = {
        'Content-Type': 'application/json',
        'Referer': '',
        'X-CSRFToken' : self.csrftoken,
        'Authorization' : 'Token bd9ecc45b397f0e22bd0a8bd3304010ab4b586d8',
        'Cookie':f'csrftoken={self.csrftoken}; sessionid={self.sessionId}'
    }

    @classmethod
    def show_request_details(cls, response_list):
        """ Print the status_code and the content of a request and
            whether the request was made with success

            response_list ([request, mySession.check(request)])

        """
        print(response_list[1])
        print(f"status code: {response_list[0].status_code}")
        print(f"response : {response_list[0].content}")
        print("\n")
    
    def login_and_cookies(self):
        """ Returns the csrftoken and sessionId of a session
        """
        self.s.get(self.loginURL)
        csrftoken = self.s.cookies.get('csrftoken')
        sessionId = self.s.cookies.get('sessionid')
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
        """ Makes any get request
            
            args:
                type ( str ): object of the request
                id ( int, optional): id of the request

            returns:
                list: [response of the request, check(response)]
        """
        # create the URL by adding type and id
        get_URL = self.base_URL + type + "/"
        if id:
            get_URL += str(id)

        # make the request
        response_get = self.s.get(get_URL, headers = self.headers)

        return [response_get, mySession.check(response_get)]

    def post_workout(self):
        """ Makes a post request for a workout

            returns:
                list: [response of the request, check(response)]
        """
        # create the URL
        post_workoutURL = self.base_URL + "workout/"

        # create referer and headers
        workout_post_headers = self.headers
        post_workoutReferer = self.base_workoutReferer + "overview/"
        workout_post_headers['Referer'] = post_workoutReferer
        
        # make the request
        response_post_workout = self.s.post(post_workoutURL, headers= workout_post_headers)
        return [response_post_workout, mySession.check(response_post_workout)]
    
    def post_training(self, workoutId, description, days):
        """ Makes a post request for a training

            args:
                workoutId( int ): workout id where you want to add the training
                description( str ): description of the training
                days( list of int): the days of the week to make the training

            returns:
                list: [response of the request, check(response)]
        """
        # create the URL
        post_trainingURL = self.base_URL + "day/"

        # create referer and headers
        training_post_headers = self.headers
        post_trainingReferer = self.base_workoutReferer + str(workoutId) + "/view/"
        training_post_headers['Referer'] = post_trainingReferer

        # create the payload
        payload_training = {
            'training':workoutId,
            'description':f'{description}',
            'day':days
            }

        # make the request
        response_post_training = self.s.post(post_trainingURL, json= payload_training ,headers = training_post_headers)
        return [response_post_training, mySession.check(response_post_training)]
    
    def post_exercise(self, workoutId, exerciseday, exercises):
        """ Makes a post request for an exercise

            args:
                workoutId( int ): workout id where you want to add the exercise
                exerciseday( int ): training id where you want to add the exercise
                exercises( int ): the specific id of the exercise

            returns:
                list: [response of the request, check(response)]
        """
        # create the URL
        post_exerciseURL = self.base_URL + "set/"

        # create referer and headers
        exercise_post_headers = self.headers
        post_exerciseReferer = self.base_workoutReferer + str(workoutId) + "/view/"
        exercise_post_headers['Referer'] = post_exerciseReferer

        # create the payload
        payload_exercise = {
            "exerciseday":exerciseday,
            "exercises":exercises
          }

        # make the request
        response_post_exercise = self.s.post(post_exerciseURL, json= payload_exercise ,headers= exercise_post_headers)
        return [response_post_exercise, mySession.check(response_post_exercise)]

    def post_nutritionplan(self):
        """ Makes a post request for a nutritionplan

            returns:
                list: [response of the request, check(response)]
        """

        post_nutritionplanURL = self.base_URL + "nutritionplan/"
        nutritionplan_post_headers = self.headers
        post_nutritionplanReferer = self.base_nutritionReferer + "overview/"
        nutritionplan_post_headers['Referer'] = post_nutritionplanReferer

        response_post_nutritionplan = self.s.post(post_nutritionplanURL,headers= nutritionplan_post_headers)
        return [response_post_nutritionplan, mySession.check(response_post_nutritionplan)]

    def post_meal(self, nutritionplanId):
        """ Makes a post request for a meal

            args:
                nutritionplanId( int ): nutritionplan id where you want to add the meal

            returns:
                list: [response of the request, check(response)]
        """
        # create the URL
        post_mealURL = self.base_URL + "meal/"

        # create referer and headers
        meal_post_headers = self.headers
        post_mealReferer = self.base_nutritionReferer + str(nutritionplanId) + "/view/"
        meal_post_headers['Referer'] = post_mealReferer

        # create the payload
        payload_meal = {
        "plan":nutritionplanId
        }

        # make the request
        response_post_meal = self.s.post(post_mealURL, json = payload_meal , headers= meal_post_headers)
        return [response_post_meal,mySession.check(response_post_meal)]
    
    def post_mealitem(self, nutritionplanId, mealId, ingredientId, amount):
        """ Makes a post request for a meal item

            args:
                nutritionplanId( int ): nutritionplan id where you want to add the meal item
                mealId( int ): meal id where you want to add the meal item
                amount( int ): the amount of the meal item

            returns:
                list: [response of the request, check(response)]
        """
        # create the URL
        post_mealitemURL = self.base_URL + "mealitem/"

        # create referer and headers
        mealitem_post_headers = self.headers
        post_mealitemReferer = self.base_nutritionReferer + str(nutritionplanId) + "/view/"
        mealitem_post_headers['Referer'] = post_mealitemReferer

        # create the payload
        payload_mealitem = {
        "meal":mealId,
        "ingredient":ingredientId,
        "amount":amount
        }

        # make the request
        response_post_mealitem = self.s.post(post_mealitemURL, json = payload_mealitem , headers=mealitem_post_headers )
        return [response_post_mealitem , mySession.check(response_post_mealitem)]
    
    #special requests

    def get_trainings(self, workoutId):
        """ Get the trainings of a specific workout

            args:
                workoutId ( int ): workout id of the trainings you want to get
            
            returns:
                list: the trainings of the workout
        """
        # create the URL
        get_trainingURL = self.base_URL + "day/"

        # make the request
        response_get_training = self.s.get(get_trainingURL, headers= self.headers)

        match_trainings =  []
        next_trainingURL = 0
        
        # search for the match trainings
        while  next_trainingURL != None:
            results = json.loads(response_get_training.text).get('results')
            for result in results:
                if result.get('training') == workoutId:
                    match_trainings.append(result)
            next_trainingURL = json.loads(response_get_training.text).get('next')
            if next_trainingURL != None:
                response_get_training = self.s.get(next_trainingURL, headers= self.headers)

        return match_trainings

    def get_sets(self, trainingId):
        """ Get the sets of a specific training

            args:
                trainingId ( int ): training id of the sets you want to get
            
            returns:
                list: the sets of the workout
        """

        # create the URL
        get_setURL = self.base_URL + "set/"

        # make the request
        response_get_set = self.s.get(get_setURL, headers= self.headers)

        match_sets =  []
        next_setURL = 0
        
        # search for the match sets
        while  next_setURL != None:
            results = json.loads(response_get_set.text).get('results')
            for result in results:
                if result.get('exerciseday') == trainingId:
                    match_sets.append(result)
            next_setURL = json.loads(response_get_set.text).get('next')
            if next_setURL != None:
                response_get_set = self.s.get(next_setURL, headers= self.headers)

        return match_sets
    
    def get_meals(self, planId):
        """ Get the meals of a specific nutritionplan ( plan )

            args:
                planId ( int ): plan id of the meals you want to get
            
            returns:
                list: the meals of the workout
        """
        # create the URL
        get_mealURL = self.base_URL + "meal/"

        # make the request
        response_get_meal = self.s.get(get_mealURL, headers= self.headers)

        match_meals =  []
        next_mealURL = 0
        
        # search for the match meals
        while  next_mealURL != None:
            results = json.loads(response_get_meal.text).get('results')
            for result in results:
                if result.get('plan') == planId:
                    match_meals.append(result)
            next_mealURL = json.loads(response_get_meal.text).get('next')
            if next_mealURL != None:
                response_get_meal = self.s.get(next_mealURL, headers= self.headers)

        return match_meals
    
    def get_mealitems(self, mealId):
        """ Get the mealitems of a specific meal

            args:
                mealId ( int ): meal id of the mealitems you want to get
            
            returns:
                list: the mealitems of the meal
        """
        # create the URL
        get_mealitemURL = self.base_URL + "mealitem/"

        # make the request
        response_get_mealitem = self.s.get(get_mealitemURL, headers= self.headers)

        match_mealitems =  []
        next_mealitemURL = 0

        # search for the match mealitems 
        while  next_mealitemURL != None:
            results = json.loads(response_get_mealitem.text).get('results')
            for result in results:
                if result.get('meal') == mealId:
                    match_mealitems.append(result)
            next_mealitemURL = json.loads(response_get_mealitem.text).get('next')
            if next_mealitemURL != None:
                response_get_mealitem = self.s.get(next_mealitemURL, headers= self.headers)

        return match_mealitems

    
    def check(response):
        """ Check a request

            args:
                response: the response of a request
            
            returns:
                str: whether the request was successful or not
        """
        if (response.status_code == 200):
            return "Successful get request !"
        elif (response.status_code == 201):
            return "Successful post request !"
        else:
            return "Erorr, something went wrong."

    #parsing toml

    def parse_workouts(self, workouts_dict):
        """ Parse the workouts information from a toml

            args:
                workouts_dict ( dict ): the workouts dictionary resulted from the toml
            
        """

        # make a post request for every workout
        for workout_value in workouts_dict.values():
                req_workout = self.post_workout()

                mySession.show_request_details(req_workout)
                # if workout has values get the id of the workout created and the trainings values
                if workout_value:
                    workout_id = json.loads(req_workout[0].text).get('id')
                    trainings_dict = workout_value.get('trainings')

                    self.parse_trainings(trainings_dict, workout_id)

   
    def parse_trainings(self, trainings_dict, workout_id):
        """ Parse the trainings information from a toml

            args:
                trainings_dict ( dict ): the trainings dictionary resulted from the toml
                workout_id ( int ): the workout id of the trainings
        """

        # make a post request for every training
        for training_value in trainings_dict.values():
            req_training = self.post_training(workout_id,training_value.get('description'),training_value.get('days'))
                        
            mySession.show_request_details(req_training)
            # if training has values get the id of the training created and the exercises values
            if(training_value.get('exercises')):
                training_id = json.loads(req_training[0].text).get('id')
                exercises_dict = training_value.get('exercises')

                self.parse_exercises(exercises_dict, workout_id, training_id)

    def parse_exercises(self, exercises_dict, workout_id, training_id):
        """ Parse the exercises information from a toml

            args:
                exercises_dict ( dict ): the exercises dictionary resulted from the toml
                workout_id ( int ): the workout id of the exercises
                training_id ( int ): the workout id of the exercises
        """
        # make a post request for every exercise
        for exercise_value in exercises_dict.values():
            req_exercise = self.post_exercise(workout_id,training_id,exercise_value.get('exerciseid'))
            mySession.show_request_details(req_exercise)
    
    def parse_nutritionplans(self, nutritionplans_dict):
        """ Parse the nutritionplans information from a toml

            args:
                nutritionplans_dict ( dict ): the nutritionplans dictionary resulted from the toml
            
        """
        # make a post request for every nutritionplan
        for nutritionplan_value in nutritionplans_dict.values():
                req_nutritionplan = self.post_nutritionplan()

                mySession.show_request_details(req_nutritionplan)
                # if nutritionplan has values get the id of the nutritionplan created and the meals values
                if nutritionplan_value:
                    nutritionplan_id = json.loads(req_nutritionplan[0].text).get('id')
                    meals_dict = nutritionplan_value.get('meals')

                    self.parse_meals(meals_dict, nutritionplan_id)
    
    def parse_meals(self, meals_dict, nutritionplan_id):
        """ Parse the meals information from a toml

            args:
                meals_dict ( dict ): the meals dictionary resulted from the toml
                nutritionplan_id ( int ): the nutritionplan id of the meals
        """

        # make a post request for every meal
        for meal_value in meals_dict.values():
            req_meal = self.post_meal(nutritionplan_id)
                        
            mySession.show_request_details(req_meal)
            # if meal has values get the id of the meal created and the mealitems values
            if(meal_value.get('mealitems')):
                meal_id = json.loads(req_meal[0].text).get('id')
                mealitems_dict = meal_value.get('mealitems')

                self.parse_mealitems(mealitems_dict, nutritionplan_id, meal_id)

    def parse_mealitems(self,mealitems_dict, nutritionplan_id, meal_id):
         """ Parse the mealitems information from a toml

            args:
                mealitems_dict ( dict ): the mealitems dictionary resulted from the toml
                nutritionplan_id ( int ): the nutritionplan id of the mealitems
                meal_id ( int ): the meal id of the mealitems
        """
        # make a post request for every mealitem
         for mealitem_value in mealitems_dict.values():
            req_mealitem = self.post_mealitem(nutritionplan_id,meal_id,mealitem_value.get('ingredientid'),mealitem_value.get('amount'))
            mySession.show_request_details(req_mealitem)
    

    def pass_toml(self,path):
        """Get input requests from a toml

            args:
                path( str ): path of the toml
        """
        # convert TOML into dict
        with open(path) as file:
            toml_data_dict = toml.load(file)

        # get workouts and nutritionplans value
        workouts_dict = toml_data_dict.get('workouts')
        nutritionplans_dict = toml_data_dict.get('nutritionplans')

        # begin the parsing
        if workouts_dict:
            self.parse_workouts(workouts_dict)

        if nutritionplans_dict:
            self.parse_nutritionplans(nutritionplans_dict)




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