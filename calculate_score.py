import json


def calculate(standard_path, answer_path, question_score):
    with open(standard_path, "r") as f:
        standard = json.loads(f.read())

    with open(answer_path, "r") as f:
        answer = json.loads(f.read())

    total_score = 0
    score_for_each_item = question_score / len(standard["questions"])
    for i, question in enumerate(standard["questions"]):
        total_score_for_each_item = 0
        for key, standard_answer in question["answer"].items():
            difference = [abs(x - y) for x, y in zip(standard_answer, answer["questions"][i]["answer"][key])]
            total_difference = sum(difference)
            score = 1 - total_difference / len(difference)
            total_score_for_each_item += score
        score_for_answer = (total_score_for_each_item / len(question["answer"])) * score_for_each_item
        total_score += score_for_answer
    return total_score


if __name__ == '__main__':
    standard_path = "/Users/damon/Desktop/10_WaveGuide_Fo17_Gain13(1).json"
    answer_path = "/Users/damon/Desktop/a.json"
    score = 10
    calculate(standard_path, answer_path, score)
