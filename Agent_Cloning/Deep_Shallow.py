import copy
Shallow_active_students = ["Naveed","Waqas","Asif"]

Shallow_new_active_participants = Shallow_active_students

Shallow_new_active_participants.append("saheer")
Shallow_new_active_participants.append("hajra")
print("Orignal List : ", Shallow_active_students)
print("Shallow_Copy Newly active Student of the list:",Shallow_new_active_participants)


Deep_active_students = ["Waqas","Ahmad","Hafiz"]

Deep_new_active_participants = copy.copy(Deep_active_students)

Deep_new_active_participants.append("kamran")
Deep_new_active_participants.append("Mujahid")
print("Orignal List : ", Deep_active_students)
print("Deep_Copy Newly active student of the list:",Deep_new_active_participants)