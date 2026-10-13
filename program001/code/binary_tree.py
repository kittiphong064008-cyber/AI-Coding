import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')

file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tree.csv")

def load_file():
    data = {}
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines[1:]:
                line = line.strip()
                if line:
                    parts = [p.strip() for p in line.split(",")]
                    k = parts[0]
                    children = [p for p in parts[1:] if p]
                    data[k] = children
    if not data:
        data = {
            'A': ['B', 'C'],
            'B': ['D', 'E'],
            'C': ['F', 'G'],
            'D': ['H', 'I'],
            'E': ['J', 'K'],
            'F': ['L', 'M'],
            'G': ['N', 'O'],
            'H': [],
            'I': [],
            'J': [],
            'K': [],
            'L': [],
            'M': [],
            'N': [],
            'O': []
        }
        save_file(data)
    return data

def save_file(data):
    with open(file_name, "w", encoding="utf-8") as f:
        f.write("node,left,right\n")
        for k, children in data.items():
            left = children[0] if len(children) > 0 else ""
            right = children[1] if len(children) > 1 else ""
            f.write(f"{k},{left},{right}\n")

graph = load_file()

def show_data():
    result = "ไม่มีข้อมูล"
    if graph:
        lines = []
        for k, v in graph.items():
            lines.append(f"{k} : {v}")
        result = "\n".join(lines)
    return result

def add_data():
    result = "ข้อมูลไม่ถูกต้อง"
    node_name = input("ป้อนโหนด: ").strip().upper()
    left = input("ป้อนโหนดซ้าย (เว้นว่างได้): ").strip().upper()
    right = input("ป้อนโหนดขวา (เว้นว่างได้): ").strip().upper()
    if node_name:
        children = []
        if left:
            children.append(left)
        if right:
            children.append(right)
        graph[node_name] = children
        save_file(graph)
        result = "เพิ่มข้อมูลสำเร็จ"
    return result

def edit_data():
    result = "ไม่พบโหนด"
    node_name = input("ป้อนโหนดที่ต้องการแก้ไข: ").strip().upper()
    if node_name in graph:
        left = input("ป้อนโหนดซ้ายใหม่ (เว้นว่างได้): ").strip().upper()
        right = input("ป้อนโหนดขวาใหม่ (เว้นว่างได้): ").strip().upper()
        children = []
        if left:
            children.append(left)
        if right:
            children.append(right)
        graph[node_name] = children
        save_file(graph)
        result = "แก้ไขข้อมูลสำเร็จ"
    return result

def BFS(graph, start, dest):
    queue = [start]
    visited = []
    result = ["Not reachable", []]
    while queue:
        node = queue.pop(0)
        visited.append(node)
        if node == dest:
            print(f"{node} : {queue}")
            result[0] = "Reachable"
            break
        for child in graph.get(node, []):
            if child not in visited and child not in queue:
                queue.append(child)
        print(f"{node} : {queue}")
    result[1] = visited
    return result

def search_data():
    result = ["Tree is empty", []]
    target = input("Enter target node: ").strip().upper()
    start = "A" if "A" in graph else (list(graph.keys())[0] if graph else "")
    if start:
        result = BFS(graph, start, target)
    return result

def delete_data():
    result = "ไม่พบโหนด"
    node_name = input("ป้อนโหนดที่ต้องการลบ: ").strip().upper()
    if node_name in graph:
        to_delete = []
        queue = [node_name]
        while queue:
            curr = queue.pop(0)
            to_delete.append(curr)
            for child in graph.get(curr, []):
                if child not in to_delete and child not in queue:
                    queue.append(child)
        for n in to_delete:
            if n in graph:
                del graph[n]
        for k in graph:
            if node_name in graph[k]:
                graph[k].remove(node_name)
        save_file(graph)
        result = "ลบข้อมูลสำเร็จ"
    return result

def readKey():
    result = 0
    print("1. แสดง")
    print("2. เพิ่ม")
    print("3. แก้ไข")
    print("4. ค้นหา")
    print("5. ลบ")
    print("6. ออกจากโปรแกรม")
    val = input("ป้อนตัวเลือก: ").strip().replace(".", "")
    if val.isdigit():
        result = int(val)
    return result

def process(num):
    result = "เลือกตัวเลือกไม่ถูกต้อง"
    if num == 1:
        result = show_data()
    elif num == 2:
        result = add_data()
    elif num == 3:
        result = edit_data()
    elif num == 4:
        result = search_data()
    elif num == 5:
        result = delete_data()
    elif num == 6:
        result = "ออกจากโปรแกรม"
    return result

def output(result):
    if result is None:
        return
    if isinstance(result, list) and len(result) == 2 and isinstance(result[1], list):
        print(result[0])
        print("Path used to traverse :", end=" ")
        for x in result[1]:
            print(x, end=" ")
        print()
    else:
        print(result)
        if result == "ออกจากโปรแกรม":
            sys.exit()

def main():
    while True:
        num = readKey()
        result = process(num)
        output(result)

if __name__ == "__main__":
    main()
