# variables are the applicants
# domain is { spla, lahsa, denied }
# algorithm
# 1. loop through applicants and set the possible values based on constraints.
# 2. keep track of list of candidates that will maximize the efficiency for spla
# 3. loop through list and V

import math
# classes
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
        self.possible_applicants = set()

    def can_fit(self, applicant):
        for day_needed in applicant.days_needed:
            if self.taken_spaces[day_needed] >= self.num_spaces:
                return False
        return True

    def num_spaces(self):
        return self.num_spaces

    def add_applicant(self, applicant):
        for day_needed in applicant.days_needed:
            self.taken_spaces[day_needed] += 1
            self.efficiency += 1

    def remove_applicant(self, applicant):
        for day_needed in applicant.days_needed:
            self.taken_spaces[day_needed] -= 1
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
        self.possible_applicants = set()

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

    # print applicant
    def __repr__(self):
        return self.ID

    # See which program this applicant qualifies
    def set_possible_programs(self):
        self.possible_programs.append("None")
        if self.has_car == "Y" and self.has_drivers_license == "Y" and self.has_medical_condition == "N":
            self.possible_programs.append("spla")
        if self.gender == "F" and self.age > 17 and self.has_pet == "N":
            self.possible_programs.append("lahsa")

    # specify which days this applicant need shelter
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

# methods
# function to find the next optimal SPLA applicant to choose from
def next_SPLA_applicant():
    input_file = open("input1.txt")
    content = input_file.readlines()
    content = [line.strip() for line in content]

    # print content
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
    print lahsa_chosen

    num_spla_chosen = int(content[current_index])
    spla_chosen = set()
    current_index += 1

    for iteration in range(0, num_spla_chosen):
        spla_chosen.add(content[current_index])
        current_index += 1
    print spla_chosen

    # create applicants
    applicants = []
    num_total_applicants = int(content[current_index])
    current_index += 1
    for iteration in range(0, num_total_applicants):
        applicants.append(create_applicant(spla_chosen, spla, lahsa_chosen, lahsa, content[current_index]))
        current_index += 1
    print applicants

    # do minimax algorithm
    accepted_ID = find_next_accepted(spla, lahsa, spla_chosen, lahsa_chosen)
    print (accepted_ID)
    output_file = open("output.txt", "w")
    output_file.write(accepted_ID.ID + "\n")
    output_file.close()

def find_next_accepted(spla, lahsa, spla_chosen, lahsa_chosen):
    # If there is more spla chosen then we need to have lahsa choose to catch up.
    # while len(spla_chosen) < len(lahsa_chosen) and len(lahsa.possible_applicants) > 0:
        # applicant = find_next_lahsa_accepted(spla, lahsa)
        # # add that applicant to the chosen pool of lahsa
        # lahsa_chosen.add(applicant.ID)
        # # add that applicant to the lahsa schedule
        # lahsa.add_applicant(applicant)
        # # remove that applicant out of both possible pools
        # lahsa.possible_applicants.remove(applicant)
        # spla.possible_applicants.remove(applicant)
    return find_next_spla_accepted(spla, lahsa)

# Choose the next lahsa candidate
def find_next_lahsa_accepted(spla, lahsa):
    max_efficiency = -1
    best_applicant = None
    for applicant in lahsa.possible_applicants.copy():
        # remove this applicant from lahsa and maybe from spla
        lahsa.possible_applicants.remove(applicant)
        removed_from_spla = False
        added_to_lahsa = False
        # if hsa can fit that applicant in its schedule
        if lahsa.can_fit(applicant):
            # add to lahsa
            lahsa.add_applicant(applicant)
            added_to_lahsa = True
            # if that applicant in the pool of spla
            if applicant in spla.possible_applicants:
                spla.possible_applicants.remove(applicant)
                removed_from_spla = True

        spla_efficiency, lahsa_efficiency = spla_turn_max(spla, lahsa)

        # choose the best efficiency for lahsa or break ties by smaller applicant id
        if (lahsa_efficiency > max_efficiency or
                (lahsa_efficiency == max_efficiency and applicant.ID < best_applicant.ID)):
            max_efficiency = lahsa_efficiency
            best_applicant = applicant

        # revert the changes to test other applicants
        lahsa.possible_applicants.add(applicant)
        if added_to_lahsa:
            lahsa.remove_applicant(applicant)
        if removed_from_spla:
            spla.possible_applicants.add(applicant)

    return best_applicant

def find_next_spla_accepted(spla, lahsa):
    max_efficiency = -1
    best_applicant = None
    for applicant in spla.possible_applicants.copy():
        # remove this applicant from SPLA and maybe from LAHSA
        spla.possible_applicants.remove(applicant)
        removed_from_lahsa = False
        added_to_spla = False
        if spla.can_fit(applicant):
            spla.add_applicant(applicant)
            added_to_spla = True
            if applicant in lahsa.possible_applicants:
                lahsa.possible_applicants.remove(applicant)
                removed_from_lahsa = True
        spla_efficiency, lahsa_efficiency = lahsa_turn_max(spla, lahsa)
        if (spla_efficiency > max_efficiency or
                (spla_efficiency == max_efficiency and applicant.ID < best_applicant.ID)):
            max_efficiency = spla_efficiency
            best_applicant = applicant
        spla.possible_applicants.add(applicant)
        if added_to_spla:
            spla.remove_applicant(applicant)
        if removed_from_lahsa:
            lahsa.possible_applicants.add(applicant)
    return best_applicant

def lahsa_turn_max(spla, lahsa):
    # if both possible applicant pools are empty:
    if len(lahsa.possible_applicants) == 0 and len(spla.possible_applicants) == 0:
        return spla.efficiency, lahsa.efficiency
    # if only lahsa possible pool is empty
    elif len(lahsa.possible_applicants) == 0:
        return spla_turn_max(spla, lahsa)

    best_lahsa_efficiency = -1
    associated_spla_efficiency = -1

    for applicant in lahsa.possible_applicants.copy():
        lahsa.possible_applicants.remove(applicant)
        removed_from_spla = False
        added_to_lahsa = False

        if lahsa.can_fit(applicant):
            lahsa.add_applicant(applicant)
            added_to_lahsa = True

            if applicant in spla.possible_applicants:
                spla.possible_applicants.remove(applicant)
                removed_from_spla = True

        spla_efficiency, lahsa_efficiency = spla_turn_max(spla, lahsa)

        if best_lahsa_efficiency < lahsa_efficiency:
            best_lahsa_efficiency = lahsa_efficiency
            associated_spla_efficiency = spla_efficiency
        lahsa.possible_applicants.add(applicant)
        if added_to_lahsa:
            lahsa.remove_applicant(applicant)
        if removed_from_spla:
            spla.possible_applicants.add(applicant)
    return associated_spla_efficiency, best_lahsa_efficiency

def spla_turn_max(spla, lahsa):
    if len(spla.possible_applicants) == 0 and len(lahsa.possible_applicants) == 0:
        return spla.efficiency, lahsa.efficiency
    elif len(spla.possible_applicants) == 0:
        return lahsa_turn_max(spla, lahsa)

    best_spla_efficiency = -1
    associated_lahsa_efficiency = -1
    for applicant in spla.possible_applicants.copy():
        spla.possible_applicants.remove(applicant)
        removed_from_lahsa = False
        added_to_spla = False
        if spla.can_fit(applicant):
            spla.add_applicant(applicant)
            added_to_spla = True
            if applicant in lahsa.possible_applicants:
                lahsa.possible_applicants.remove(applicant)
                removed_from_lahsa = True
        spla_efficiency, lahsa_efficiency = lahsa_turn_max(spla, lahsa)
        if best_spla_efficiency < spla_efficiency:
            best_spla_efficiency = spla_efficiency
            associated_lahsa_efficiency = lahsa_efficiency
        spla.possible_applicants.add(applicant)
        if added_to_spla:
            spla.remove_applicant(applicant)
        if removed_from_lahsa:
            lahsa.possible_applicants.add(applicant)
    return best_spla_efficiency, associated_lahsa_efficiency

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
        return applicant
    elif applicant.ID in lahsa_chosen:
        lahsa.add_applicant(applicant)
        return applicant

    if "spla" in applicant.possible_programs:
        spla.possible_applicants.add(applicant)
    if "lahsa" in applicant.possible_programs:
        lahsa.possible_applicants.add(applicant)
    return applicant

if __name__ == "__main__":
    next_SPLA_applicant()