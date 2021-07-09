from session import mySession
import toml


session1 = mySession()

#req1 = session1.get("workout")
# req3 = session1.post_workout(), 
#req4 = session1.post_training(280895, 'mamamama', [6, 7])
# req5 = session1.post_exercise(28089544444444, 142834, 279)
# req6 = session1.post_nutritionplan()
# req7 = session1.post_meal(75496)
# req8 = session1.post_mealitem(280895, 188455, 9842, 400)
#req9 = session1.get("workout",279811)
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

# mySession.show_request_details(req9)

# cum sa imi dau seama sa fac toml
# test_dict = {
#     "workouts": {
#         "workout1" : {
#             "trainings" : {
#                 "training1" : {
#                     "description":"ce frum e",
#                     "days": [6,7],
#                     "exercises" : {
#                         "exercise1": {
#                             "exerciseid":279
#                             },
#                         "exercise2": {
#                             "exerciseid":279
#                             },
#                         "exercise3": {
#                             "exerciseid":279
#                             }
#                         }
#                 },
#                 "training2" : {
#                     "description":"ce frum e",
#                     "days": [6,7]
#                     }
#             }
#         },
#         "workout2" : {}
#     }
# }


# test_dict2 = {
#     "nutritionplans": {
#         "nutritionplan1" : {
#             "meals" : {
#                 "meal1" : {
#                     "mealitems" : {
#                         "mealitem1": {
#                             "ingredientid":9842,
#                             "amount":400
#                             },
#                         "mealitem2": {
#                             "ingredientid":9842,
#                             "amount":400
#                             },
#                         "mealitem3": {
#                             "ingredientid":9842,
#                             "amount":400
#                             }
#                         }
#                 },
#                 "meal2" : {}
#             }
#         },
#         "nutritionplan2" : {}
#     }
# }

# test_toml = toml.dumps(test_dict2)


session1.pass_toml('.\data.toml')
# req_del = session1.delete_workout(283311)
# mySession.show_request_details(req_del)

# req_del = session1.delete_nutritionplan(76819)
#mySession.show_request_details(req1)
session1.cleanUp()