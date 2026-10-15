import os
import sys
import math
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')

file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tables.csv")
map_img_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "restaurant_map.png")

def generate_map(data):
    result = "สร้างแผนที่สำเร็จ"
    if data:
        fig, ax = plt.subplots(figsize=(8, 6), dpi=100)
        drawn_edges = set()
        for k, v in data.items():
            x1, y1 = v['x'], v['y']
            for n, d in v['neighbors'].items():
                if n in data:
                    edge = tuple(sorted([k, n]))
                    if edge not in drawn_edges:
                        drawn_edges.add(edge)
                        x2, y2 = data[n]['x'], data[n]['y']
                        ax.plot([x1, x2], [y1, y2], color='#94a3b8', linestyle='--', linewidth=1.5, zorder=1)
                        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                        ax.text(mx, my, f"{d}m", color='#475569', fontsize=9, fontweight='bold', ha='center', va='center',
                                bbox=dict(boxstyle='round,pad=0.2', facecolor='#ffffff', edgecolor='#cbd5e1', alpha=0.9), zorder=2)
        for k, v in data.items():
            x, y = v['x'], v['y']
            circle = plt.Circle((x, y), 0.45, facecolor='#3b82f6', edgecolor='#1d4ed8', linewidth=2, zorder=3)
            ax.add_patch(circle)
            ax.text(x, y, k, color='#ffffff', fontsize=11, fontweight='bold', ha='center', va='center', zorder=4)
            ax.text(x, y - 0.7, f"SLD:{v['sld']}", color='#0f172a', fontsize=8.5, fontweight='bold', ha='center', va='top', zorder=4)
        ax.set_title("Robot Food Delivery Map (Tables, Distances & SLD)", fontsize=13, fontweight='bold')
        ax.set_aspect('equal')
        ax.grid(True, linestyle=':', alpha=0.5)
        plt.tight_layout()
        plt.savefig(map_img_name)
        plt.close()
    return result

def save_file(data):
    with open(file_name, "w", encoding="utf-8") as f:
        f.write("table,x,y,neighbors,sld\n")
        for k, v in data.items():
            neigh_str = ";".join([f"{n}:{d}" for n, d in v['neighbors'].items()])
            f.write(f"{k},{v['x']},{v['y']},{neigh_str},{v['sld']}\n")
    generate_map(data)
    return None

def load_file():
    data = {}
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines[1:]:
                line = line.strip()
                if line:
                    parts = line.split(",")
                    k = parts[0].strip()
                    x = float(parts[1].strip())
                    y = float(parts[2].strip())
                    neigh_raw = parts[3].strip()
                    sld = float(parts[4].strip())
                    neighbors = {}
                    if neigh_raw:
                        for item in neigh_raw.split(";"):
                            if ":" in item:
                                n_k, n_d = item.split(":", 1)
                                neighbors[n_k.strip()] = float(n_d.strip())
                    data[k] = {'x': x, 'y': y, 'neighbors': neighbors, 'sld': sld}
    if not data:
        data = {
            'T1': {'x': 1.0, 'y': 1.0, 'neighbors': {'T2': 4.0, 'T3': 6.0}, 'sld': 12.0},
            'T2': {'x': 4.0, 'y': 2.0, 'neighbors': {'T1': 4.0, 'T4': 5.0, 'T5': 7.0}, 'sld': 9.0},
            'T3': {'x': 2.0, 'y': 6.0, 'neighbors': {'T1': 6.0, 'T5': 4.0, 'T6': 8.0}, 'sld': 8.0},
            'T4': {'x': 8.0, 'y': 1.0, 'neighbors': {'T2': 5.0, 'T7': 6.0}, 'sld': 5.0},
            'T5': {'x': 6.0, 'y': 5.0, 'neighbors': {'T2': 7.0, 'T3': 4.0, 'T7': 4.0}, 'sld': 4.0},
            'T6': {'x': 5.0, 'y': 9.0, 'neighbors': {'T3': 8.0, 'T7': 5.0}, 'sld': 5.0},
            'T7': {'x': 10.0, 'y': 6.0, 'neighbors': {'T4': 6.0, 'T5': 4.0, 'T6': 5.0}, 'sld': 0.0}
        }
        save_file(data)
    return data

graph = load_file()

def show_data():
    result = "ไม่มีข้อมูล"
    if graph:
        lines = ["\n--- รายชื่อโต๊ะอาหารและระยะทาง (Robot Delivery Map) ---"]
        lines.append(f"{'โต๊ะ':<8} {'พิกัด (X,Y)':<14} {'ระยะทางตรง (SLD)':<18} {'โต๊ะข้างเคียง (ระยะทาง)'}")
        lines.append("-" * 65)
        for k, v in graph.items():
            pos = f"({v['x']}, {v['y']})"
            neighs = ", ".join([f"{n} ({d}m)" for n, d in v['neighbors'].items()]) if v['neighbors'] else "ไม่มี"
            lines.append(f"{k:<8} {pos:<14} {v['sld']:<18} {neighs}")
        lines.append("-" * 65)
        lines.append(f"รูปแผนที่ถูกสร้างไว้ที่: {map_img_name}")
        result = "\n".join(lines)
    return result

def add_data():
    result = "ข้อมูลไม่ถูกต้อง"
    table_name = input("ป้อนชื่อโต๊ะ: ").strip().upper()
    if table_name:
        x_str = input("ป้อนพิกัด X (ตัวเลข): ").strip()
        y_str = input("ป้อนพิกัด Y (ตัวเลข): ").strip()
        sld_str = input("ป้อนระยะทางตรง SLD (ตัวเลข): ").strip()
        neigh_str = input("ป้อนโต๊ะข้างเคียงและระยะทาง เช่น T2:4, T3:6 (เว้นว่างได้): ").strip().upper()
        x = float(x_str) if x_str.replace('.', '', 1).isdigit() else 0.0
        y = float(y_str) if y_str.replace('.', '', 1).isdigit() else 0.0
        sld = float(sld_str) if sld_str.replace('.', '', 1).isdigit() else 0.0
        neighbors = {}
        if neigh_str:
            parts = [p.strip() for p in neigh_str.split(",") if p.strip()]
            for p in parts:
                if ":" in p:
                    n_name, dist = p.split(":", 1)
                    n_name = n_name.strip()
                    dist_val = float(dist.strip()) if dist.strip().replace('.', '', 1).isdigit() else 1.0
                    neighbors[n_name] = dist_val
        graph[table_name] = {'x': x, 'y': y, 'neighbors': neighbors, 'sld': sld}
        save_file(graph)
        result = "เพิ่มข้อมูลสำเร็จ"
    return result

def edit_data():
    result = "ไม่พบโต๊ะอาหาร"
    table_name = input("ป้อนชื่อโต๊ะที่ต้องการแก้ไข: ").strip().upper()
    if table_name in graph:
        curr = graph[table_name]
        x_str = input(f"ป้อนพิกัด X ใหม่ (เดิม {curr['x']}): ").strip()
        y_str = input(f"ป้อนพิกัด Y ใหม่ (เดิม {curr['y']}): ").strip()
        sld_str = input(f"ป้อนระยะทางตรง SLD ใหม่ (เดิม {curr['sld']}): ").strip()
        neigh_str = input("ป้อนโต๊ะข้างเคียงและระยะทางใหม่ เช่น T2:4, T3:6: ").strip().upper()
        x = float(x_str) if x_str.replace('.', '', 1).isdigit() else curr['x']
        y = float(y_str) if y_str.replace('.', '', 1).isdigit() else curr['y']
        sld = float(sld_str) if sld_str.replace('.', '', 1).isdigit() else curr['sld']
        neighbors = {}
        if neigh_str:
            parts = [p.strip() for p in neigh_str.split(",") if p.strip()]
            for p in parts:
                if ":" in p:
                    n_name, dist = p.split(":", 1)
                    n_name = n_name.strip()
                    dist_val = float(dist.strip()) if dist.strip().replace('.', '', 1).isdigit() else 1.0
                    neighbors[n_name] = dist_val
        graph[table_name] = {'x': x, 'y': y, 'neighbors': neighbors, 'sld': sld}
        save_file(graph)
        result = "แก้ไขข้อมูลสำเร็จ"
    return result

def delete_data():
    result = "ไม่พบโต๊ะอาหาร"
    table_name = input("ป้อนชื่อโต๊ะที่ต้องการลบ: ").strip().upper()
    if table_name in graph:
        del graph[table_name]
        for k in graph:
            if table_name in graph[k]['neighbors']:
                del graph[k]['neighbors'][table_name]
        save_file(graph)
        result = "ลบข้อมูลสำเร็จ"
    return result

def a_star_search(data, start, dest):
    result = ["Not reachable", [], 0, []]
    if start in data and dest in data:
        start_h = data[start]['sld']
        open_list = [(start_h, 0.0, start, [start])]
        visited = []
        step = 0
        found = False
        final_path = []
        final_cost = 0.0
        while open_list and not found:
            step += 1
            open_list.sort(key=lambda item: item[0])
            curr_f, curr_g, curr_node, curr_path = open_list.pop(0)
            visited.append(curr_node)
            curr_h = curr_f - curr_g
            print(f"Step {step} >> Node {curr_node} : g={curr_g}, h={curr_h}, f={curr_f}")
            if curr_node == dest:
                found = True
                final_path = curr_path
                final_cost = curr_g
            else:
                for neighbor, dist in data[curr_node]['neighbors'].items():
                    if neighbor in data and neighbor not in visited:
                        new_g = curr_g + dist
                        h_val = data[neighbor]['sld']
                        new_f = new_g + h_val
                        new_path = curr_path + [neighbor]
                        open_list.append((new_f, new_g, neighbor, new_path))
            open_display = [f"('{item[2]}', f={item[0]})" for item in open_list]
            print(f"  Open list : [{', '.join(open_display)}]")
        if found:
            result = ["Reachable", final_path, final_cost, visited]
    return result

def search_data():
    result = ["ไม่มีข้อมูลโต๊ะอาหาร", []]
    start = input("ป้อนตำแหน่งโต๊ะเริ่มต้น: ").strip().upper()
    dest = input("ป้อนตำแหน่งโต๊ะเป้าหมาย: ").strip().upper()
    if start and dest:
        result = a_star_search(graph, start, dest)
    return result

def readKey():
    result = 0
    print("\n========== ระบบค้นหาเส้นทางเสิร์ฟอาหาร (A* Search) ==========")
    print("1. แสดง")
    print("2. เพิ่ม")
    print("3. แก้ไข")
    print("4. ลบ")
    print("5. ค้นหา")
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
        result = delete_data()
    elif num == 5:
        result = search_data()
    elif num == 6:
        result = "ออกจากโปรแกรม"
    return result

def output(result):
    if result is not None:
        if isinstance(result, list) and len(result) >= 3:
            print("\n" + "=" * 55)
            print(f"ผลการค้นหา: {result[0]}")
            if result[0] == "Reachable":
                print(f"เส้นทางการเสิร์ฟอาหาร: {' -> '.join(result[1])}")
                print(f"ระยะทางรวม: {result[2]} เมตร")
                print(f"ลำดับการสำรวจโหนด (Visited): {' -> '.join(result[3])}")
            print("=" * 55)
        else:
            print(result)
            if result == "ออกจากโปรแกรม":
                sys.exit()
    return None

def main():
    while True:
        num = readKey()
        result = process(num)
        output(result)

if __name__ == "__main__":
    main()
