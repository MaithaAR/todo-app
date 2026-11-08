# todo.py
tasks = []


def add(task):
    tasks.append(task)


def show():
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task}")

def done(number):
    tasks.pop(number - 1)

if __name__ == "__main__":
    add("Install Git")
    add("Finish the Git lab")
    show()

print("Tasks left:", count())
