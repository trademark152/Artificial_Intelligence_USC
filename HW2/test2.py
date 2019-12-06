# variables are the applicants
# domain is { spla, lahsa, denied }
# algorithm
# 1. loop through applicants and set the possible values based on constraints.
# 2. keep track of list of candidates that will maximize the efficiency for spla
# 3. loop through list and V

import math


class SPLA:
    def __init__(self, num_spaces):
        self.num_spaces = num_spaces
        self.taken_spaces = {
            "monday": 0,
            "tuesday": 0,
            "wednesday": 0,
            "thursday": 0,
            "friday": 0,
            "saturday": 0,
            "sunday": 0}
        self.efficiency = 0
        self.first_chosen = None
        self.best_first_chosen = None

    def can_fit(self, applicant):
        for day_needed in applicant.days_needed:
            if self.taken_spaces[day_needed] >= self.num_spaces:
                return False
        return True

    def set_first_chosen(self, applicant):
        self.first_chosen = applicant.ID

    def set_best_first_chosen(self, applicant_ID):
        self.best_first_chosen = applicant_ID

    def num_spaces(self):
        return self.num_spaces

    def add_applicant(self, applicant):
        for day_needed in applicant.days_needed:
            self.taken_spaces[day_needed] += 1;
            self.efficiency += 1

    def remove_applicant(self, applicant):
        for day_needed in applicant.days_needed:
            self.taken_spaces[day_needed] -= 1;
            self.efficiency -= 1


class LAHSA:
    def __init__(self, num_beds):
        self.num_beds = num_beds
        self.taken_beds = {
            "monday": 0,
            "tuesday": 0,
            "wednesday": 0,
            "thursday": 0,
            "friday": 0,
            "saturday": 0,
            "sunday": 0}
        self.efficiency = 0

    def num_beds(self):
        return self.num_beds

    def can_fit(self, applicant):
        for day_needed in applicant.days_needed:
            if self.taken_beds[day_needed] >= self.num_beds:
                return False
        return True

    def add_applicant(self, applicant):
        for day_needed in applicant.days_needed:
            self.taken_beds[day_needed] += 1;
            self.efficiency += 1

    def remove_applicant(self, applicant):
        for day_needed in applicant.days_needed:
            self.taken_beds[day_needed] -= 1;
            self.efficiency -= 1


class BothPrograms:
    def __init__(self, spla, lahsa):
        self.spla = spla
        self.lahsa = lahsa
        self.current_best_efficiency = 0
        self.current_best_80 = 0

    def spla(self):
        return self.spla

    def lahsa(self):
        return self.lahsa

    def set_current_best_80(self, current_best_80):
        self.current_best_80 = current_best_80

    def current_best_80(self):
        return self.current_best_80

    def set_current_best_efficiency(self, current_best):
        self.current_best_efficiency = current_best

    def current_best_efficiency(self):
        return self.current_best_efficiency


def next_SPLA_applicant():
    input_file = open("input1.txt")
    content = input_file.readlines()
    content = [line.strip() for line in content]
    # get num beds, num spaces
    num_beds = int(content[0])
    num_spaces = int(content[1])

    # create programs
    spla = SPLA(num_spaces)
    lahsa = LAHSA(num_beds)

    # get already chosen ID's
    num_lahsa_chosen = int(content[2])
    lahsa_chosen = set()

    current_index = 3
    for iteration in range(0, num_lahsa_chosen):
        lahsa_chosen.add(content[current_index])
        current_index += 1

    num_spla_chosen = int(content[current_index])
    spla_chosen = set()
    current_index += 1

    for iteration in range(0, num_spla_chosen):
        spla_chosen.add(content[current_index])
        current_index += 1

    # create applicants
    applicants = []
    num_total_applicants = int(content[current_index])
    current_index += 1
    for iteration in range(0, num_total_applicants):
        applicants.append(create_applicant(spla_chosen, spla, lahsa_chosen, lahsa, content[current_index]))
        current_index += 1

    # do backtracking algorithm
    accepted_ID = find_next_accepted(applicants, spla_chosen, lahsa_chosen, spla, lahsa)
    output_file = open("output.txt", "w")
    output_file.write(accepted_ID + "\n")
    output_file.close()


def find_next_accepted(applicants, spla_chosen, lahsa_chosen, spla, lahsa):
    max_score = (lahsa.num_beds * 7) + (spla.num_spaces * 7)
    current_efficiency = spla.efficiency + lahsa.efficiency
    both_programs = BothPrograms(spla, lahsa)
    both_programs.set_current_best_efficiency(current_efficiency)
    find_next_accepted_backtrack(applicants, spla_chosen, lahsa_chosen, both_programs, max_score, 0)
    return spla.best_first_chosen


# will return true if the max efficiency was found. else false.
def find_next_accepted_backtrack(applicants,
                                 spla_chosen,
                                 lahsa_chosen,
                                 both_programs,
                                 max_efficiency,
                                 current_index):
    spla = both_programs.spla
    lahsa = both_programs.lahsa
    efficiency = spla.efficiency + lahsa.efficiency
    # if we are at max efficiency
    if efficiency == max_efficiency and spla.first_chosen != None:
        spla.set_best_first_chosen(spla.first_chosen)
        return True

    # set best first chosen if the all variables set and efficiency is greater than current best efficiency
    if current_index == len(applicants):
        if efficiency > both_programs.current_best_efficiency:
            spla.set_best_first_chosen(spla.first_chosen)
            both_programs.set_current_best_efficiency(efficiency)
        elif spla.best_first_chosen == None:
            spla.set_best_first_chosen(spla.first_chosen)
        return False

    applicant = applicants[current_index]

    # if the applicant has already been chosen, just move on to the next applicant.
    if (applicant.ID in spla_chosen) or (applicant.ID in lahsa_chosen):
        return find_next_accepted_backtrack(applicants,
                                            spla_chosen,
                                            lahsa_chosen,
                                            both_programs,
                                            max_efficiency,
                                            current_index + 1)

    for program in applicant.possible_programs:
        added_to_spla = False
        added_to_lahsa = False
        if program == "spla" and spla.can_fit(applicant):
            if spla.first_chosen == None:
                spla.set_first_chosen(applicant)
            spla.add_applicant(applicant)
            added_to_spla = True
        elif program == "lahsa" and lahsa.can_fit(applicant):
            lahsa.add_applicant(applicant)
            added_to_lahsa = True
        found_max_score = find_next_accepted_backtrack(applicants,
                                                       spla_chosen,
                                                       lahsa_chosen,
                                                       both_programs,
                                                       max_efficiency,
                                                       current_index + 1)

        # if we found the max score, then return
        if found_max_score:
            return True
        # reset values and remove applicant from chosen program.
        if added_to_spla:
            spla.remove_applicant(applicant)
        elif added_to_lahsa:
            lahsa.remove_applicant(applicant)
        if spla.first_chosen == applicant.ID:
            spla.first_chosen = None
    return False


class Applicant:
    def __init__(self,
                 ID,
                 gender,
                 age,
                 has_pet,
                 has_medical_condition,
                 has_car,
                 has_drivers_license,
                 days_needing_shelter):
        self.ID = ID
        self.gender = gender
        self.has_pet = has_pet
        self.age = age
        self.has_medical_condition = has_medical_condition
        self.has_car = has_car
        self.has_drivers_license = has_drivers_license
        self.days_needed = []
        self.set_days_needing_shelter(days_needing_shelter)
        self.possible_programs = []
        self.set_possible_programs()

    def ID(self):
        return self.ID

    def set_possible_programs(self):
        self.possible_programs.append("None")
        if self.has_car == "Y" and self.has_drivers_license == "Y" and self.has_medical_condition == "N":
            self.possible_programs.append("spla")
        if self.gender == "F" and self.age > 17 and self.has_pet == "N":
            self.possible_programs.append("lahsa")

    def possible_programs(self):
        return self.possible_programs

    def set_days_needing_shelter(self, days_string):
        if int(days_string[0]) == 1:
            self.days_needed.append("monday")
        if int(days_string[1]) == 1:
            self.days_needed.append("tuesday")
        if int(days_string[2]) == 1:
            self.days_needed.append("wednesday")
        if int(days_string[3]) == 1:
            self.days_needed.append("thursday")
        if int(days_string[4]) == 1:
            self.days_needed.append("friday")
        if int(days_string[5]) == 1:
            self.days_needed.append("saturday")
        if int(days_string[6]) == 1:
            self.days_needed.append("sunday")


def create_applicant(spla_chosen, spla, lahsa_chosen, lahsa, applicant_string):
    ID = applicant_string[0:5]
    gender = applicant_string[5]
    age = int(applicant_string[6:9])
    has_pet = applicant_string[9]
    has_medical_condition = applicant_string[10]
    has_car = applicant_string[11]
    has_drivers_license = applicant_string[12]
    days_needing_shelter = applicant_string[13:]

    applicant = Applicant(
        ID,
        gender,
        age,
        has_pet,
        has_medical_condition,
        has_car,
        has_drivers_license,
        days_needing_shelter)
    # if the applicant has been chosen, add them to the correct program.
    if applicant.ID in spla_chosen:
        spla.add_applicant(applicant)
    elif applicant.ID in lahsa_chosen:
        lahsa.add_applicant(applicant)

    return applicant


if __name__ == "__main__":
    applicant = next_SPLA_applicant()
    print applicant
