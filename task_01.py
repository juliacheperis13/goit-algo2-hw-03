from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate
from collections import defaultdict

# 1. Створюємо граф
# G = nx.DiGraph()

# # Додаємо ребра з пропускною здатністю (з таблиці)
# edges = [
#     ("Термінал 1", "Склад 1", 25),
#     ("Термінал 1", "Склад 2", 20),
#     ("Термінал 1", "Склад 3", 15),
#     ("Термінал 2", "Склад 3", 15),
#     ("Термінал 2", "Склад 4", 30),
#     ("Термінал 2", "Склад 2", 10),
#     ("Склад 1", "Магазин 1", 15),
#     ("Склад 1", "Магазин 2", 10),
#     ("Склад 1", "Магазин 3", 20),
#     ("Склад 2", "Магазин 4", 15),
#     ("Склад 2", "Магазин 5", 10),
#     ("Склад 2", "Магазин 6", 25),
#     ("Склад 3", "Магазин 7", 20),
#     ("Склад 3", "Магазин 8", 15),
#     ("Склад 3", "Магазин 9", 10),
#     ("Склад 4", "Магазин 10", 20),
#     ("Склад 4", "Магазин 11", 10),
#     ("Склад 4", "Магазин 12", 15),
#     ("Склад 4", "Магазин 13", 5),
#     ("Склад 4", "Магазин 14", 10),
# ]

# # Додаємо ребра до графа
# G.add_weighted_edges_from(edges)

# # Визначаємо позиції вузлів (згідно зі схемою)
# pos = {
#     "Термінал 1": (0, 3),
#     "Термінал 2": (0, 0),
#     "Склад 1": (2, 4),
#     "Склад 2": (2, 2),
#     "Склад 3": (4, 2),
#     "Склад 4": (4, 0),
#     "Магазин 1": (6, 4.5),
#     "Магазин 2": (6, 4),
#     "Магазин 3": (6, 3.5),
#     "Магазин 4": (6, 3),
#     "Магазин 5": (6, 2.5),
#     "Магазин 6": (6, 2),
#     "Магазин 7": (6, 1.5),
#     "Магазин 8": (6, 1),
#     "Магазин 9": (6, 0.5),
#     "Магазин 10": (6, 0),
#     "Магазин 11": (6, -0.5),
#     "Магазин 12": (6, -1),
#     "Магазин 13": (6, -1.5),
#     "Магазин 14": (6, -2),
# }

# # Малюємо граф
# plt.figure(figsize=(14, 10))
# nx.draw(
#     G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold", arrows=True
# )
# labels = nx.get_edge_attributes(G, "weight")
# nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)

# # Відображаємо граф
# plt.title("Логістична мережа", fontsize=14)
# plt.show()


# Список вузлів у графі (у порядку для матриці)
nodes = [
    "Термінал 1",
    "Термінал 2",
    "Склад 1",
    "Склад 2",
    "Склад 3",
    "Склад 4",
    "Магазин 1",
    "Магазин 2",
    "Магазин 3",
    "Магазин 4",
    "Магазин 5",
    "Магазин 6",
    "Магазин 7",
    "Магазин 8",
    "Магазин 9",
    "Магазин 10",
    "Магазин 11",
    "Магазин 12",
    "Магазин 13",
    "Магазин 14",
]

# Ініціалізація порожньої матриці (розміром кількість вузлів x кількість вузлів)
num_nodes = len(nodes)
capacity_matrix = np.zeros((num_nodes, num_nodes), dtype=int)

# Відображення вузлів на індекси
node_indices = {node: i for i, node in enumerate(nodes)}

# Додаємо пропускні здатності (з таблиці)
edges = [
    ("Термінал 1", "Склад 1", 25),
    ("Термінал 1", "Склад 2", 20),
    ("Термінал 1", "Склад 3", 15),
    ("Термінал 2", "Склад 3", 15),
    ("Термінал 2", "Склад 4", 30),
    ("Термінал 2", "Склад 2", 10),
    ("Склад 1", "Магазин 1", 15),
    ("Склад 1", "Магазин 2", 10),
    ("Склад 1", "Магазин 3", 20),
    ("Склад 2", "Магазин 4", 15),
    ("Склад 2", "Магазин 5", 10),
    ("Склад 2", "Магазин 6", 25),
    ("Склад 3", "Магазин 7", 20),
    ("Склад 3", "Магазин 8", 15),
    ("Склад 3", "Магазин 9", 10),
    ("Склад 4", "Магазин 10", 20),
    ("Склад 4", "Магазин 11", 10),
    ("Склад 4", "Магазин 12", 15),
    ("Склад 4", "Магазин 13", 5),
    ("Склад 4", "Магазин 14", 10),
]

# Заповнюємо матрицю пропускної здатності
for edge in edges:
    from_node, to_node, capacity = edge
    from_index = node_indices[from_node]
    to_index = node_indices[to_node]
    capacity_matrix[from_index][to_index] = capacity

# Вивід матриці
print("Матриця пропускної здатності:")
print(capacity_matrix)


# 2. Функція для пошуку збільшуючого шляху (BFS)

def bfs(capacity_matrix, flow_matrix, source, sink, parent):
    visited = [False] * len(capacity_matrix)
    queue = deque([source])
    visited[source] = True

    while queue:
        current_node = queue.popleft()

        for neighbor in range(len(capacity_matrix)):
            # Перевірка, чи є залишкова пропускна здатність у каналі
            if (
                not visited[neighbor]
                and capacity_matrix[current_node][neighbor]
                - flow_matrix[current_node][neighbor]
                > 0
            ):
                parent[neighbor] = current_node
                visited[neighbor] = True
                if neighbor == sink:
                    return True
                queue.append(neighbor)

    return False


# Основна функція для обчислення максимального потоку


def edmonds_karp(capacity_matrix, source, sink):
    num_nodes = len(capacity_matrix)
    # Ініціалізуємо матрицю потоку нулем
    flow_matrix = [[0] * num_nodes for _ in range(num_nodes)]
    parent = [-1] * num_nodes
    max_flow = 0

    # Поки є збільшуючий шлях, додаємо потік
    while bfs(capacity_matrix, flow_matrix, source, sink, parent):
        # Знаходимо мінімальну пропускну здатність уздовж знайденого шляху (вузьке місце)
        path_flow = float("Inf")
        current_node = sink

        while current_node != source:
            previous_node = parent[current_node]
            path_flow = min(
                path_flow,
                capacity_matrix[previous_node][current_node]
                - flow_matrix[previous_node][current_node],
            )
            current_node = previous_node

        # Оновлюємо потік уздовж шляху, враховуючи зворотний потік
        current_node = sink
        while current_node != source:
            previous_node = parent[current_node]
            flow_matrix[previous_node][current_node] += path_flow
            flow_matrix[current_node][previous_node] -= path_flow
            current_node = previous_node

        # Збільшуємо максимальний потік
        max_flow += path_flow

    return max_flow


data = [
    ["Термінал 1", "Магазин 1", edmonds_karp(capacity_matrix, 0, 6)],
    ["Термінал 1", "Магазин 2", edmonds_karp(capacity_matrix, 0, 7)],
    ["Термінал 1", "Магазин 3", edmonds_karp(capacity_matrix, 0, 8)],
    ["Термінал 1", "Магазин 4", edmonds_karp(capacity_matrix, 0, 9)],
    ["Термінал 1", "Магазин 5", edmonds_karp(capacity_matrix, 0, 10)],
    ["Термінал 1", "Магазин 6", edmonds_karp(capacity_matrix, 0, 11)],
    ["Термінал 1", "Магазин 7", edmonds_karp(capacity_matrix, 0, 12)],
    ["Термінал 1", "Магазин 8", edmonds_karp(capacity_matrix, 0, 13)],
    ["Термінал 1", "Магазин 9", edmonds_karp(capacity_matrix, 0, 14)],
    ["Термінал 2", "Магазин 4", edmonds_karp(capacity_matrix, 1, 9)],
    ["Термінал 2", "Магазин 5", edmonds_karp(capacity_matrix, 1, 10)],
    ["Термінал 2", "Магазин 6", edmonds_karp(capacity_matrix, 1, 11)],
    ["Термінал 2", "Магазин 7", edmonds_karp(capacity_matrix, 1, 12)],
    ["Термінал 2", "Магазин 8", edmonds_karp(capacity_matrix, 1, 13)],
    ["Термінал 2", "Магазин 9", edmonds_karp(capacity_matrix, 1, 14)],
    ["Термінал 2", "Магазин 10", edmonds_karp(capacity_matrix, 1, 15)],
    ["Термінал 2", "Магазин 11", edmonds_karp(capacity_matrix, 1, 16)],
    ["Термінал 2", "Магазин 12", edmonds_karp(capacity_matrix, 1, 17)],
    ["Термінал 2", "Магазин 13", edmonds_karp(capacity_matrix, 1, 18)],
    ["Термінал 2", "Магазин 14", edmonds_karp(capacity_matrix, 1, 19)],
]

# Заголовки таблиці
headers = ["Термінал", "Магазин", "Фактичний Потік (одиниць)"]

# Формування таблиці
table = tabulate(data, headers=headers, tablefmt="grid", stralign="center")

# Вивід таблиці
print(table)


sum_terminal_1 = 0
sum_terminal_2 = 0

for row in data:
    if row[0] == "Термінал 1":
        sum_terminal_1 += row[2]
    elif row[0] == "Термінал 2":
        sum_terminal_2 += row[2]

# Виводимо результати
print(f"Сума для Термінал 1: {sum_terminal_1}")
print(f"Сума для Термінал 2: {sum_terminal_2}")


# Створення словника для зберігання сум по кожному магазину
store_sums = defaultdict(int)

# Додавання значень до відповідних магазинів
for entry in data:
    store_name = entry[1]  # Назва магазину
    flow_value = entry[2]  # Значення, яке повертає edmonds_karp
    store_sums[store_name] += flow_value

# Виведення результатів
for store, total_flow in store_sums.items():
    print(f"Сума для магазину {store}: {total_flow}")


# Згідно з розрахунків обидва термінали мають однаковий потік - 130
# Маршрут термінал 2 - склад 4 - магазин 13 має найменшу пропускну здатність
# Магазин 13 отримав 5, магазини 1 - 15, магазин 2 - 10, магазин 11 - 10, магаин 14 - 10
# Термінал 2	- Склад 2 має пропускну властивість всього в 10, збільшивши пропускну здатність цього вузла можна збільшити обсяг до магазинів
