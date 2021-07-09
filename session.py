import requests
import json
import toml
from requests.sessions import session

class mySession:
    """
    Creates an instance of an user login session on https://wger.de/en/user/login

    """

    s = requests.session()

    #baseURL
    
    base_URL = "https://wger.de/api/v2/"


    #loginURL

    loginURL="https://wger.de/en/user/login"


    #baseReferers

    base_workoutReferer = "https://wger.de/en/workout/"
    base_nutritionReferer = "https://wger.de/en/nutrition/"

    #workout and nutritionplan created ids
    workout_ids = []
    nutritionplan_ids = []


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
        """ 
        Print the status_code and the content of a request and
            whether the request was made with success

        :param response_list: ([request, mySession.check(request)])

        returns:
            json with status_code and content of the response

        """
        print(response_list[1])
        print(f"status code: {response_list[0].status_code}")
        print(f"response : {response_list[0].content}")
        print("\n")
        return response_list[0]
    
    def login_and_cookies(self):
        """ 
        Returns the csrftoken and sessionId of a session
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
        """ 
        Makes any get request
            
        :param type: object of the request
        :param id: id of the request

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
        """ 
        Makes a post request for a workout

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

        #add id to created ids list
        mySession.add_post_id(response_post_workout,self.workout_ids)
        return [response_post_workout, mySession.check(response_post_workout)]
    
    def post_training(self, workoutId, description, days):
        """ 
        Makes a post request for a training

        :param workoutId: workout id where you want to add the training
        :param description: description of the training
        :param days: the days of the week to make the training

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
        """ 
        Makes a post request for an exercise

        :param workoutId: workout id of the training where you want to add the exercise
        :param exerciseday: training id where you want to add the exercise
        :param exercises: the specific id of the exercise

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
        """ 
        Makes a post request for a nutritionplan

        returns:
            list: [response of the request, check(response)]
        """
        # create the URL
        post_nutritionplanURL = self.base_URL + "nutritionplan/"

        # create referer and headers
        nutritionplan_post_headers = self.headers
        post_nutritionplanReferer = self.base_nutritionReferer + "overview/"
        nutritionplan_post_headers['Referer'] = post_nutritionplanReferer

        # make the request
        response_post_nutritionplan = self.s.post(post_nutritionplanURL,headers= nutritionplan_post_headers)

        #add id to created ids list
        mySession.add_post_id(response_post_nutritionplan, self.nutritionplan_ids)
        return [response_post_nutritionplan, mySession.check(response_post_nutritionplan)]

    def post_meal(self, nutritionplanId):
        """ 
        Makes a post request for a meal

        :param nutritionplanId: nutritionplan id  where you want to add the meal

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
        """ 
        Makes a post request for a meal item

        :param nutritionplanId: nutritionplan id of the meal where you want to add the meal item
        :param mealId: meal id where you want to add the meal item
        :param amount: the amount of the meal item

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
    
    def delete_item(self, type, id):
        """ 
        Delete a specific workout or nutritionplan

        :param id: the id of the workout or nutritionplan to delete

        returns:
            list: [response of the request, check(response)]
        """
        # create the URL
        delete_URL = self.base_URL + type +'/' + str(id) 

        # create referer and headers
        delete_headers = self.headers
        if(type == 'workout'):
            delete_Referer = self.base_workoutReferer + str(id) +  "/view/"
        else:
            delete_Referer = self.base_nutritionReferer + str(id) +  "/view/"
        delete_headers['Referer'] = delete_Referer

        # make the request
        response_delete = self.s.delete(delete_URL, headers= delete_headers)
        return [response_delete, mySession.check(response_delete)]
    
    #get requests for certain ids

    def get_trainings(self, workoutId):
        """ 
        Get the trainings of a specific workout

        :param workoutId: workout id of the trainings you want to get
            
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
        """ 
        Get the sets of a specific training

        :param trainingId: training id of the sets you want to get
            
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
        """ 
        Get the meals of a specific nutritionplan ( plan )

        :param planId: plan id of the meals you want to get
            
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
        """ 
        Get the mealitems of a specific meal

        :param mealId: meal id of the mealitems you want to get
            
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
        """ 
        Check a request with .ok method

        :param <response>: the response of a request
            
        returns:
            str: whether the request was successful or not
        """
        if (response.ok):
            return "Successful request !"
        else:
            return "Erorr, something went wrong."

    #parsing toml

    def parse_workouts(self, workouts_dict):
        """ 
        Parse the workouts information from a toml

        :param workouts_dict: the workouts dictionary resulted from the toml
            
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
        """ 
        Parse the trainings information from a toml

        :param trainings_dict: the trainings dictionary resulted from the toml
        :param workout_id: the workout id of the trainings
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
        """ 
        Parse the exercises information from a toml

        :param exercises_dict: the exercises dictionary resulted from the toml
        :param workout_id: the workout id of the exercises
        :param training_id: the workout id of the exercises
        """
        # make a post request for every exercise
        for exercise_value in exercises_dict.values():
            req_exercise = self.post_exercise(workout_id,training_id,exercise_value.get('exerciseid'))
            mySession.show_request_details(req_exercise)
    
    def parse_nutritionplans(self, nutritionplans_dict):
        """ 
        Parse the nutritionplans information from a toml

        :param nutritionplans_dict: the nutritionplans dictionary resulted from the toml
            
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
        """ 
        Parse the meals information from a toml

        :param meals_dict: the meals dictionary resulted from the toml
        :param nutritionplan_id: the nutritionplan id of the meals
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
         """ 
         Parse the mealitems information from a toml

        :param mealitems_dict: the mealitems dictionary resulted from the toml
        :param nutritionplan_id: the nutritionplan id of the mealitems
        :param meal_id: the meal id of the mealitems
        """
        # make a post request for every mealitem
         for mealitem_value in mealitems_dict.values():
            req_mealitem = self.post_mealitem(nutritionplan_id,meal_id,mealitem_value.get('ingredientid'),mealitem_value.get('amount'))
            mySession.show_request_details(req_mealitem)
    

    def pass_toml(self,path):
        """
        Get input requests from a toml

        :param path: path of the toml
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
    

    @classmethod
    def add_post_id(cls, response, ids):
        """ 
        Add an id of a created request object to a list with all created request objects
        
        """

        id = json.loads(response.text).get('id')
        ids.append(id)
    
        
    def cleanUp(self):
        """ 
        Delete all the workouts and nutritionplans created in an object

        """

        for workout_id in self.workout_ids:
            self.delete_item('workout', workout_id)

        for nutritionplan_id in self.nutritionplan_ids:
            self.delete_item('nutritionplan', nutritionplan_id)