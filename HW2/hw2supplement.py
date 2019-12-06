# FIND THE BEST PICKING
print
selectApp = {}
utilScore = 9999
idInit = -99
if sharedPool:
    for applicant in sharedPool:
        calendar = splaCalendar
        # hypothetically update the calendar with this applicant to calculate utility score
        # updateCalendar(calendar, applicant)
        score = calUtility(calendar, applicant)
        print("The highest score of all shared applicants is: " + str(score))

        # update the min Score utility
        if score == utilScore:
            if int(applicant["ID"]) < int(idInit):
                utilScore = score
                selectApp = applicant
                idInit = applicant["ID"]
        if score < utilScore:
            utilScore = score
            selectApp = applicant
            idInit = applicant["ID"]

elif not sharedPool:
    for applicant in splaPool:
        calendar = splaCalendar
        # hypothetically update the calendar with this applicant to calculate utility score
        # updateCalendar(calendar, applicant)
        score = calUtility(calendar, applicant)
        print(score)

        # update the min Score utility
        if score < utilScore:
            utilScore = score
            selectApp = applicant

print
print("The FIRST chosen applicant's ID for SPLA is " + selectApp["ID"])

# FIRST STEP: pick an applicant in the shared pool with highest util score
selectList = []
allCalendar = [splaCalendar, hsaCalendar]
turnToChoose = 0

# looping until sharedPool is empty
# while sharedPool:
#     selectApp = {}
#     utilScore = -9999
#     for applicant in sharedPool:
#         if turnToChoose % 2 == 0:
#             calendar = allCalendar[0]
#         elif turnToChoose % 2 == 1:
#             calendar = allCalendar[1]
#
#         # hypothetically update the calendar with this applicant to calculate utility score
#         # updateCalendar(calendar, applicant)
#         score = calUtility(calendar, applicant)
#
#         # update the max Score utility
#         if score > utilScore:
#             utilScore = score
#             selectApp = applicant
#
#     # Store the selection in a list
#     selectList.append(selectApp)
#
#     # Update the calendars:
#     # updateCalendar(splaCalendar, applicant)
#
#     # Update the application pool
#     removeApp(sharedPool, selectApp["ID"])
#
#     # Finish turn and update counter
#     turnToChoose += 1
#