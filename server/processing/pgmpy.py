import pgmpy
import pandas as pd
import numpy as np
import math
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import BayesianEstimator
from pgmpy.inference import VariableElimination
from utils.answers import answers_list
from utils.attributes_weight import weights


def create_bayesian_model():
    model = BayesianNetwork(
        [
            ("wear_clothes", "wear_shoes"),
            ("wear_clothes", "wear_green_jacket"),
            ("wear_clothes", "have_bow_tie"),
            ("wear_clothes", "wear_hat"),
            ("wear_clothes", "wear_orange_suits"),
            ("wear_clothes", "wear_glasses"),
            ("characters", "wear_clothes"),
            ("special_powers", "from_jujutsu_kaisen"),
            ("special_powers", "from_one_piece"),
            ("special_powers", "from_seven_deadly_sins"),
            ("special_powers", "from_attack_on_titan"),
            ("special_powers", "from_dragon_ball"),
            ("special_powers", "from_naruto"),
            ("special_powers", "from_one_punch_man"),
            ("special_powers", "can_fly"),
            ("special_powers", "can_transform"),
            ("special_powers", "is_demon_slayer"),
            ("special_powers", "turn_into_a_fox"),
            ("special_powers", "hunt_demons"),
            ("from_attack_on_titan", "use_a_hook"),
            ("characters", "special_powers"),
            ("is_bad", "is_demon"),
            ("characters", "is_bad"),
            ("from_dragon_ball", "is_saiyan"),
            ("from_dragon_ball", "ultra_instinct"),
            ("from_dragon_ball", "is_angel"),
            ("from_dragon_ball", "weakness_is_tail"),
            ("from_dragon_ball", "look_like_cat"),
            ("look_like_cat", "is_god_of_destruction"),
            ("from_one_piece", "is_sailor_or_pirate"),
            ("from_jujutsu_kaisen", "wear_blindfold"),
            ("can_transform", "evolve_more_than_once"),
            ("characters", "is_animal"),
            ("is_animal", "have_tail"),
            ("is_animal", "is_cat"),
            ("is_animal", "is_dragon"),
            ("is_cat", "from_tom_and_jerry"),
            ("characters", "in_detective_story"),
            ("in_detective_story", "is_detective"),
            ("in_detective_story", "wear_clothes"),
            ("in_detective_story", "own_skateboard"),
            ("is_detective", "go_to_school"),
            ("characters", "fight_with_a_sword"),
            ("characters", "have_hair"),
            ("have_hair", "special_hair_color"),
            ("have_hair", "long_hair"),
            ("special_hair_color", "multi_colored_hair"),
            ("special_hair_color", "dark_hair"),
            ("special_hair_color", "white_hair"),
            ("special_hair_color", "blue_hair"),
            ("special_hair_color", "blond_hair"),
            ("blond_hair", "ever_had_blond_hair"),
            ("linked_with_magic", "have_magical_staff"),
            ("characters", "linked_with_magic"),
            ("characters", "play_cards_game"),
            ("characters", "is_robot"),
            ("characters", "yellow_skin"),
            ("yellow_skin", "is_pokemon"),
            ("characters", "have_children"),
            ("characters", "big"),
            ("characters", "is_girl"),
            ("characters", "have_violet_eyes"),
            ("characters", "have_siblings"),
            ("characters", "green_skin"),
            ("characters", "is_a_captain"),
            ("characters", "pink_skin"),
            ("characters", "blue_skin"),
            ("characters", "small"),
            ("characters", "fat"),
            ("characters", "go_to_school"),
            ("characters", "have_legs"),
            ("have_legs", "walk_on_two_legs"),
            ("characters", "have_scars_on_head"),
            ("characters", "small"),
            ("characters", "have_sad_backstory"),
            ("characters", "son_of_leader"),
            ("have_sad_backstory", "orphan"),
            ("from_dragon_ball", "have_magical_staff"),
            ("from_dragon_ball", "wear_orange_suits"),
        ]
    )

    return model


def create_estimator(model, data):
    estimator = BayesianEstimator(model, data)
    return estimator


def estimate_cpds_for_model(model, estimator, attributes: list):
    for attribute in attributes:
        cpd = estimator.estimate_cpd(attribute, prior_type="BDeu")
        # print(attribute)
        # print(cpd)
        model.add_cpds(cpd)


def export_cpds_to_excel(csv_path, excel_path, model, attributes: list):
    with pd.ExcelWriter(excel_path) as writer:
        for attribute in attributes:
            cpd = model.get_cpds(attribute)
            cpd.to_csv(filename=csv_path)
            df = pd.read_csv(csv_path)
            df.to_excel(writer, sheet_name=attribute, index=False)


def get_attributes(model):
    attributes = []
    for node in model.nodes():
        attributes.append(node)

    return attributes


def query_probabilities(model, attribute, evidence):
    try:
        inference = VariableElimination(model)
        probabilities = inference.query(attribute, evidence=evidence)
        return probabilities
    except Exception as error:
        pass


def calculate_sum_of_entropy(model, attribute_coming, evidence):
    sum_of_entropy = 0

    # print("evidence_so_far:", evidence)
    # print("Attribute Coming: ", attribute_coming)
    query_discrete_factor = query_probabilities(model, attribute_coming, evidence)
    # print(query_discrete_factor)
    for answer in answers_list:
        attr = {attribute_coming[0]: answer["value"]}
        try:
            pr = query_discrete_factor.get_value(**attr)
            sum_of_entropy = sum_of_entropy + (pr * (-1) * math.log2(pr))

        except Exception as error:
            # print(error)
            pass
    return sum_of_entropy
