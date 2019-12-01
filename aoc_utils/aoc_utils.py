from bs4 import BeautifulSoup
import os
import requests


def fetch(year, day, content_type):
    headers = {"cookie": f"session={os.environ['SESSION_COOKIE']}",}
    if content_type == 'input':
        response = requests.get(f"https://adventofcode.com/{year}/day/{day}/input", headers=headers)
        _handle_error(response.status_code)
        message = response.text.strip()
    elif content_type == 'problem':
        response = requests.get(f"https://adventofcode.com/{year}/day/{day}", headers=headers)
        _handle_error(response.status_code)
        soup = BeautifulSoup(response.text, "html.parser")
        message = soup.article.text

    return message


def save(path_to_save, year, day, content_type):
    content = fetch(year, day, content_type)
    with open(f"{path_to_save}/{content_type}.txt", "w") as text_file:
        text_file.write(content)


def submit(year, day, level, answer):
    print(f"For Day {day}, Part {level}, we are submitting answer: {answer}")

    headers = {"cookie": f"session={os.environ['SESSION_COOKIE']}",}
    data = {
        "level": str(level),
        "answer": str(answer)
    }

    response = requests.post(f"https://adventofcode.com/{year}/day/{day}/answer", headers=headers, data=data)

    soup = BeautifulSoup(response.text, "html.parser")
    message = soup.article.text

    if "That's the right answer" in message:
        print("Correct!")
        star_path = os.getcwd()
        with open(f"{star_path}/stars.txt", "w+") as text_file:
            print("Writing '*' to star file...")
            text_file.write('*')

    elif "That's not the right answer" in message:
        print("Wrong answer!")
    elif "You gave an answer too recently" in message:
        print("Wait a bit, too recent a answer...")


def test(test_cases, answer):
    passed = True
    for test_case in test_cases:
        problem_input = test_case[1]
        submitted_answer = answer(problem_input, test_case[0])
        real_answer = test_case[2]
        if str(real_answer) == str(submitted_answer):
            print(f"Test passed! for input {real_answer}")
        else:
            passed = False
            print(f"Test failed :( for input {problem_input}, you put {submitted_answer}, correct: {real_answer}")

    if passed:
        return 'passed'


def check_stars():
    star_path = os.getcwd()
    star_file = f"{star_path}/stars.txt"
    if os.path.exists(star_file):
        with open(star_file, 'r') as file:
            stars = file.read().strip()
            return len(stars)


def test_and_submit(year, day, test_cases, problem_input, answer):
    test_results = test(test_cases, answer)

    if test_results == 'passed':
        print("\nCongratulations! All tests passed.")
        stars = check_stars()
        if stars and stars < 2:
            print('Would you like to submit this answer? y/n')
        else:
            print("It seems we've been here before and you've submitted both answers!")

        if stars == 0:
            print(f'Part 1: {answer(problem_input, 1)}')
            submit_answer = input()
            if submit_answer == 'y':
                submit(year, day, 1, answer(problem_input, 1))

        elif stars == 1:
            print(f'Part 2: {answer(problem_input, 2)}')
            submit_answer = input()
            if submit_answer == 'y':
                submit(year, day, 2, answer(problem_input, 2))


def _handle_error(code):
    if code == 404:
        raise ValueError("This day is not available yet!")
    elif code == 400:
        raise ValueError("Bad credentials!")
