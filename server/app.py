from flask import Flask, jsonify, request
from flask_cors import CORS
from utils.questions import questions_list as QUESTIONS_LIST
from utils.conflicting_attributes import (
    conflicting_attributes_yes,
    conflicting_attributes_no,
)
from utils.attributes_weight import weights
from werkzeug.exceptions import HTTPException, NotFound, BadRequest
from db.db_methods import connect_to_db, show_table, sql_db, close_connection
import random
import asyncio
import matplotlib.pyplot as plt
import json

import pandas as pd
import numpy as np
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import (
    HillClimbSearch,
    BicScore,
    ExhaustiveSearch,
    BDeuScore,
    K2Score,
    BDsScore,
    MmhcEstimator,
    PC,
    BayesianEstimator,
    MaximumLikelihoodEstimator,
)

from pgmpy.inference import VariableElimination
from processing.pgmpy import *
from collections import deque

import seaborn as sns
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score


app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

evidences_so_far = {}
questions_so_far = []
minimum_probability = 0.92
minimum_questions = 19
db = None
model = None
attributes = []
nodes_level = {}
inverted_nodes_level = {}
exclude_attributes = []


# Test route for change data in database
@app.route("/change-db", methods=["GET", "POST"])
def change_database():
    if request.method == "GET":
        try:
            db = connect_to_db()
            data = (
                sql_db(db, "SELECT * FROM characterInfo").df().to_json(orient="records")
            )
            close_connection(db)
            return data
        except Exception as error:
            print(error)

    if request.method == "POST":
        db = connect_to_db()
        # sql = "ALTER TABLE t1 ALTER fight_with_a_sword TYPE DOUBLE;"
        # sql_db(db, sql)
        # sql_db(
        #     db,
        #     "CREATE TABLE Characters AS SELECT * FROM read_csv('data/anime_characters.csv');",
        # )
        # print(data)

        # global model
        # model = create_bayesian_model()
        # attributes = get_attributes(model)
        # estimator = create_estimator(model, data)
        # csv_path = "data/cpds.csv"
        # excel_path = "data/cpds.xlsx"
        # estimate_cpds_for_model(model, estimator, attributes)
        # export_cpds_to_excel(csv_path, excel_path, model, attributes)

        # evidence = {}
        # probabilities = query_probabilities(model, ["is_saiyan"], evidence)
        # print(probabilities)

        # temp = sql_db(db, "SELECT DISTINCT characters FROM Characters;").df()
        # print(temp)
        # for i in temp.loc[:, "characters"]:
        #     print(i)

        # entropy_table = {}
        # for attribute in attributes:
        #     if attribute not in evidence.keys() and attribute != "characters":
        #         entropy = calculate_sum_of_entropy(model, [attribute], evidence)
        #         entropy_table[attribute] = entropy
        # entropy = calculate_sum_of_entropy(
        #     model,
        #     ["have_siblings"],
        #     evidence,
        # )
        # print(entropy)
        # entropy_table = dict(sorted(entropy_table.items(), key=lambda x: x[1]))
        # for key, value in entropy_table.items():
        #     print(f"{key}: {value}")

        # print("min value is", min(entropy_table, key=entropy_table.get))

        # sql_db(
        #     db,
        #     "CREATE TABLE images (character VARCHAR PRIMARY KEY, image_address VARCHAR);",
        # )
        # request_data = request.get_json()
        # sql_db(db, "DROP TABLE images")
        # sql_db(
        #     db,
        #     "CREATE TABLE characterInfo (character VARCHAR PRIMARY KEY, anime_name VARCHAR, image_address VARCHAR);",
        # )
        # sql = "INSERT INTO characterInfo VALUES ('{}', '{}', '{}');".format(
        #     request_data["character"],
        #     request_data["anime_name"],
        #     request_data["image_address"],
        # )
        # print(sql)
        # print(request_data)
        # sql_db(db, sql)
        # data = pd.read_excel("data/anime_characters.xlsx")
        # print(data)
        # data.to_csv("data/anime_characters.csv", index=None, header=True)
        # sql = "DROP TABLE Characters;"
        # sql_db(db, sql)
        # sql = "CREATE TABLE Characters AS FROM 'data/anime_characters.csv';"
        # sql = "UPDATE characterInfo SET image_address = 'https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/a61e25a9-98cb-42ae-95a8-9e8a0ba1d67e/width=1200/a61e25a9-98cb-42ae-95a8-9e8a0ba1d67e.jpeg' WHERE character = 'Vados'"

        data = sql_db(db, "SELECT * FROM Characters;").df()

        print(data)
        result = generate_character_dicts(data)

        # In kết quả
        # for i, d in enumerate(result):
        #     print(json.dumps(d, indent=4, ensure_ascii=False))
        # sql = "SELECT * FROM Characters"
        # sql_db(db, sql)
        model = create_bayesian_model()
        attributes = get_attributes(model)
        estimator = create_estimator(model, data)
        estimate_cpds_for_model(model, estimator, attributes)

        accuracy_dict = {}
        for time in range(10):
            data_test = generate_character_dicts(data)
            # print(data_test)
            result = []
            for i, d in enumerate(data_test):
                evidence = d.copy()
                evidence.pop("characters", None)
                inference = VariableElimination(model)
                predicted = inference.map_query(["characters"], evidence=evidence)
                # print(probabilities)
                result.append(
                    {"Predicted": predicted["characters"], "Expected": d["characters"]}
                )
            # print(result)
            predict_right = 0
            for a in result:
                print(a)
                if a["Predicted"] == a["Expected"]:
                    predict_right += 1
            print("Accuracy is {}".format(predict_right / 25))
            accuracy_dict.update({"Lần " + str(time + 1): predict_right / 25})
            print(accuracy_dict)
        print(accuracy_dict)
        categories = list(accuracy_dict.keys())
        values = list(accuracy_dict.values())

        # Vẽ biểu đồ cột
        plt.bar(categories, values, color=["#363636"])

        # Thêm tiêu đề và nhãn cho các trục
        plt.title("Accuracy After 10 Tests with k = 40")
        plt.ylabel("Accuracy")

        # Xoay nhãn trục x để dễ đọc
        plt.xticks(rotation=45)

        # Hiển thị biểu đồ
        plt.tight_layout()  # Điều chỉnh bố cục
        plt.show()
        # df = pd.DataFrame(result)

        # # Lấy các giá trị dự đoán và giá trị thực tế
        # y_pred = df["Predicted"]
        # y_true = df["Expected"]

        # classes = np.unique(np.concatenate((y_pred, y_true)))

        # # Tính toán confusion matrix
        # conf_matrix = confusion_matrix(y_true, y_pred, labels=classes)

        # # Vẽ confusion matrix
        # plt.figure(figsize=(8, 6))
        # sns.heatmap(
        #     conf_matrix,
        #     annot=True,
        #     fmt="d",
        #     cmap="Blues",
        #     xticklabels=classes,
        #     yticklabels=classes,
        # )
        # plt.ylabel("Expected")
        # plt.xlabel("Predicted")
        # plt.title("Confusion Matrix")
        # plt.show()

        # # Tính toán precision, recall và F1 score cho từng lớp
        # precision = precision_score(y_true, y_pred, average=None, labels=classes)
        # recall = recall_score(y_true, y_pred, average=None, labels=classes)
        # f1 = f1_score(y_true, y_pred, average=None, labels=classes)

        # # In kết quả
        # for i, label in enumerate(classes):
        #     print(
        #         f"Class {label}: Precision = {precision[i]:.2f}, Recall = {recall[i]:.2f}, F1 Score = {f1[i]:.2f}"
        #     )

        close_connection(db)
    return {}


def generate_character_dicts(df):
    # Kiểm tra xem DataFrame có ít nhất 5 dòng không
    if len(df) < 5:
        raise ValueError("DataFrame cần ít nhất 5 dòng.")

    # Lấy ngẫu nhiên 5 nhân vật khác nhau
    sampled_rows = df.sample(n=5, random_state=random.randint(1, 100))
    result_dicts = []

    for index, row in sampled_rows.iterrows():
        character_name = row["characters"]  # Giả sử cột nhân vật có tên là 'nhân vật'

        for _ in range(5):
            attributes = df.columns[1:]
            selected_attributes = np.random.choice(attributes, size=40, replace=False)

            # Tạo dictionary cho thuộc tính
            attribute_dict = {attr: row[attr] for attr in selected_attributes}
            attribute_dict["characters"] = (
                character_name  # Thêm cặp key-value cho nhân vật
            )

            # Thêm dictionary vào danh sách kết quả
            result_dicts.append(attribute_dict)

    return result_dicts


@app.route("/main-game", methods=["GET", "POST"])
def main_game():
    global evidences_so_far
    global questions_so_far
    global db
    global model
    global attributes
    global nodes_level
    global inverted_nodes_level
    global exclude_attributes

    if request.method == "GET":
        if db is None:
            try:
                db = connect_to_db()

            except Exception as error:
                print(error)
        else:
            close_connection(db)
            db = connect_to_db()

        data = sql_db(db, "SELECT * FROM Characters;").df()

        model = create_bayesian_model()
        attributes = get_attributes(model)
        estimator = create_estimator(model, data)
        levels, inverted_nodes_level = set_nodes_level(model)

        for i in range(5):
            print("Bậc {}:".format(i))
            for j in inverted_nodes_level[i]:
                print("- ", j)
            print()

        csv_path = "data/cpds.csv"
        excel_path = "data/cpds.xlsx"
        estimate_cpds_for_model(model, estimator, attributes)
        export_cpds_to_excel(csv_path, excel_path, model, attributes)

        print("get method ---------------")
        questions_so_far.clear()
        evidences_so_far.clear()
        exclude_attributes = []
        first_question = generate_first_question()

        # Interact with db here.....
        # sql_db(db, "CREATE TABLE t1 AS FROM read_csv('./data/anime_characters.csv')")
        # show_table(db, "t1")

        close_connection(db)
        return {
            "status": "success",
            "description": "GET",
            "first_question": first_question,
        }
    if request.method == "POST":

        try:
            db = connect_to_db()
            request_data = request.get_json()
            response = None

            if request_data["answer"] == 0.5:
                sql = "SELECT DISTINCT {} FROM Characters".format(
                    request_data["attribute"]
                )
                enum_answer = (
                    np.array(sql_db(db, sql).df().values.tolist()).flatten().tolist()
                )
                print(enum_answer)
                if 0.5 not in enum_answer:
                    request_data["answer"] = random.choice([0, 1])

            evidence_by_player = {
                request_data["attribute"]: request_data["answer"],
            }

            evidences_so_far.update(evidence_by_player)
            questions_so_far.append(request_data["attribute"])
            questions_so_far = list(dict.fromkeys(questions_so_far))

            next_question = generate_next_question(model, attributes, evidences_so_far)

            current_probabilities = calculate_current_probabilities(evidences_so_far)

            # print(evidences_so_far)
            # print(current_probabilities)
            is_max_question = False
            if next_question is not None:
                character_result = predict_character_result(
                    current_probabilities, evidences_so_far
                )
            else:
                print("max question.....")
                character_result = max(
                    current_probabilities, key=current_probabilities.get
                )
                is_max_question = True

            if character_result is not None:
                sql = "SELECT * FROM characterInfo WHERE character = '{}'".format(
                    character_result
                )
                character_result = sql_db(db, sql).df().to_json(orient="records")

            response = {
                "questions_so_far": questions_so_far,
                "evidences_so_far": evidences_so_far,
                "next_question": next_question,
                "current_probabilites": current_probabilities,
                "predict_character_result": character_result,
                "max_question": is_max_question,
            }

            close_connection(db)

            return response

        except NotFound as e:
            return jsonify(
                {
                    "error": e.code,
                    "name": e.name,
                    "description": "Cannot found questions",
                }
            )
        except HTTPException as e:
            return jsonify(
                {"error": e.code, "name": e.name, "description": e.description}
            )
        except Exception as error:
            print("Error:", error)


def generate_first_question():
    first_question = None
    first_question_attribute = random.choice(inverted_nodes_level[1])
    for question in QUESTIONS_LIST:
        if first_question_attribute == question["attribute"]:
            first_question = question
            break
    return first_question


def generate_next_question(model, attributes: list, evidences_so_far: dict):
    global exclude_attributes
    # visited_order = dfs(model, evidences_so_far)
    entropy_table = {}
    for attribute in attributes:
        entropy = calculate_sum_of_entropy(model, [attribute], evidences_so_far)

        entropy_table[attribute] = entropy

    entropy_table = dict(
        sorted(entropy_table.items(), key=lambda x: x[1], reverse=True),
    )
    # keys = list(entropy_table.keys())[:12]
    # values = list(entropy_table.values())[:12]
    # plt.bar(keys, values, color=["#363636"], alpha=1.0)

    # # Thêm tiêu đề và nhãn
    # plt.title("Entropy for nodes")
    # plt.xlabel("Nodes")
    # plt.ylabel("Entropy")
    # plt.rc("font", size=8)

    # # Hiện thị biểu đồ
    # plt.grid(axis="y")
    # plt.xticks(rotation=30)

    # plt.show()
    # for i in visited_order:
    #     print(i, end=" -> ")

    for attribute, answer in evidences_so_far.items():
        if attribute in conflicting_attributes_yes.keys() and answer == 1:
            exclude_attributes.extend(conflicting_attributes_yes[attribute])

        if attribute in conflicting_attributes_no.keys() and answer == 0:
            exclude_attributes.extend(conflicting_attributes_no[attribute])
    exclude_attributes = list(dict.fromkeys(exclude_attributes))
    print("exclude: ", exclude_attributes)
    # i = 1
    # while (
    #     visited_order[i] in evidences_so_far.keys()
    #     or visited_order[i] in exclude_attributes
    # ):
    #     i = i + 1
    # next_question_attribute = visited_order[i]
    i = 0
    visited_order = list(entropy_table.keys())

    while (
        visited_order[i] in evidences_so_far.keys()
        or visited_order[i] in exclude_attributes
        or visited_order[i] == "characters"
    ):

        i = i + 1
        if i == len(visited_order):
            break

    next_question_attribute = None
    if i < len(visited_order):
        next_question_attribute = visited_order[i]
        print(next_question_attribute)
    else:
        next_question_attribute = None

    # entropy_table = {}

    # for attribute in attributes:
    #     if attribute not in evidences_so_far.keys() and attribute != "characters":
    #         entropy = calculate_sum_of_entropy(model, [attribute], evidences_so_far)
    #         entropy_table[attribute] = entropy

    # entropy_table = dict(sorted(entropy_table.items(), key=lambda x: x[1]))

    # next_question_attribute = min(entropy_table, key=entropy_table.get)
    # print("min value is", next_question_attribute)
    next_question = None
    for question in QUESTIONS_LIST:
        if (
            next_question_attribute is not None
            and next_question_attribute == question["attribute"]
        ):
            next_question = question
            break
    return next_question


def set_nodes_level(model):
    levels = {node: -1 for node in model.nodes()}
    root_node = "characters"
    levels[root_node] = 0

    queue = deque([root_node])

    while queue:
        current_node = queue.popleft()
        current_level = levels[current_node]

        for child in model.get_children(current_node):
            if levels[child] == -1:
                levels[child] = current_level + 1
                queue.append(child)

    inverted_levels = {}

    for node, level in levels.items():
        if level not in inverted_levels:
            inverted_levels[level] = []
        inverted_levels[level].append(node)

    return levels, inverted_levels


def dfs(model, evidences_so_far):
    visited = set()
    root_node = "characters"
    stack = [root_node]
    visited_order = []  # Lưu trữ thứ tự duyệt

    while stack:
        current = stack.pop()
        if current not in visited:
            visited.add(current)
            visited_order.append(current)  # Thêm nút hiện tại vào thứ tự duyệt
            children = model.get_children(current)
            entropy_table = {}
            for child in children:
                if child != "characters":
                    entropy = calculate_sum_of_entropy(model, [child], evidences_so_far)
                    entropy += weights[child]
                    entropy_table[child] = entropy

            entropy_table = dict(
                sorted(entropy_table.items(), key=lambda x: x[1], reverse=True),
            )
            # print(entropy_table)
            for child in entropy_table.keys():
                stack.append(child)

            # for child in children:
            #     stack.append(child)

            # print("after entropy", len(entropy_table.keys()))
            # for child in entropy_table.keys():
            #     stack.append(child)

    return visited_order


def calculate_current_probabilities(evidences_so_far: dict):
    try:
        current_probabilities: dict[str, float] = {}

        probabilities = query_probabilities(model, ["characters"], evidences_so_far)
        print(probabilities)

        characters_list = sql_db(db, "SELECT DISTINCT characters FROM Characters;").df()
        characters_list = characters_list.loc[:, "characters"]
        # print(probabilities)
        for character in characters_list:
            attr = {"characters": character}
            current_probabilities[character] = probabilities.get_value(**attr)
    except Exception as error:
        print(error)
    return current_probabilities


def predict_character_result(
    current_probabilities: dict[str, float], evidence_so_far: dict
):
    global minimum_probability
    global minimum_questions
    num_of_evidences = len(evidence_so_far)
    max_probability = minimum_probability
    result = None

    for character, probability in current_probabilities.items():
        if (
            probability >= minimum_probability
            and probability >= max_probability
            and num_of_evidences >= minimum_questions
        ):
            result = character
            max_probability = probability

    return result


if __name__ == "__main__":
    app.run()
