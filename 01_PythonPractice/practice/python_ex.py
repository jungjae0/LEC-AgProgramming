from collections import Counter


def ex_list():
    names = [
        "전혜진", "강다영", "김희진",
        "장희원", "정재영", "윤예진"
    ]

    reverse_name = []
    for i, name in enumerate(names):
        sorted_names = sorted(names)
        reverse_name.append(sorted_names[-(i+1)])
    print(reverse_name)

    print(sorted(names, reverse=True))
    print(sorted(names)[::-1])
    print(names.sort(),"/", names)


def ex_for():
    for i in range(10000):
        print(i)

    print(list(range(10000)))
    print([x for x in range(10000)])


def ex_dict():
    scores = {"전혜진": 10, "최수영": 20, "장희원": 30, "김희진": 40}
    for name in scores:
        score = scores[name]
        print(name, ":", score)

    for k, v in scores.items():
        print("key:", k, "value:", v)

    for score in scores.values():
        print(score)

    print(len(scores))

def ex_set():
    names = ["전혜진", "강다영", "김희진", "장희원", "정재영", "윤예진",
             "전혜진", "강다영", "김희진", "장희원", "정재영", "윤예진",]

    del_duplicate = list(set(names))
    print(del_duplicate)

    visited = []
    for name in names:
        if name not in visited:
            visited.append(name)
    print(visited)

    counter = Counter(names)
    rank = counter.most_common(3)
    print(rank[0][1] + rank[1][1] + rank[2][1])
    print(sum([rank[i][1] for i, r in enumerate(rank)]))
    print(sum([v for k, v in rank]))


    complex_list = [
        ("전혜진", 15, 20, 30),
        ("강다영", 20, 11, 29)
    ]

    for name, *info in complex_list:
        print(name, info)

def main():
    ex_set()
    ex_dict()
    ex_for()
    ex_list()

if __name__ == "__main__":
    main()
