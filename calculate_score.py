import json


def calculate(standard, answer):
    for i, question in enumerate(standard["questions"]):
        total_score = 0
        for key, standard_answer in question["answer"].items():
            difference = [abs(x - y) for x, y in zip(standard_answer, answer["questions"][i]["answer"][key])]
            total_difference = sum(difference)
            score = 1 - total_difference / len(difference)
            total_score += score
        total_score = total_score / len(question["answer"])
        print(total_score)


if __name__ == '__main__':
    with open(r"C:\Users\star\Desktop\10_WaveGuide_Fo17_Gain13(1).json", "r") as f:
        standard = json.loads(f.read())

    with open(r"C:\Users\star\Desktop\a.json", "r") as f:
        answer = json.loads(f.read())

    calculate(standard, answer)
