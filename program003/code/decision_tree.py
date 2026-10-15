import os
import sys
import json
import csv
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')

data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "traffic_data.csv")
model_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "decision_tree.json")
tree_img_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "decision_tree.png")

headers = ['Weather', 'TimeOfWeek', 'TimeOfDay', 'TrafficJam']
dataset = []
current_tree = None

def get_default_dataset():
    result = [
        ['Clear', 'Workday', 'Morning', 'Yes'],
        ['Clear', 'Workday', 'Lunch', 'No'],
        ['Clear', 'Workday', 'Evening', 'Yes'],
        ['Clear', 'Weekend', 'Morning', 'No'],
        ['Clear', 'Weekend', 'Lunch', 'No'],
        ['Clear', 'Weekend', 'Evening', 'No'],
        ['Rainy', 'Workday', 'Morning', 'Yes'],
        ['Rainy', 'Workday', 'Lunch', 'Yes'],
        ['Rainy', 'Workday', 'Evening', 'Yes'],
        ['Rainy', 'Weekend', 'Morning', 'No'],
        ['Rainy', 'Weekend', 'Lunch', 'No'],
        ['Rainy', 'Weekend', 'Evening', 'No'],
        ['Snowy', 'Workday', 'Morning', 'Yes'],
        ['Snowy', 'Workday', 'Lunch', 'Yes'],
        ['Snowy', 'Workday', 'Evening', 'Yes'],
        ['Snowy', 'Weekend', 'Morning', 'Yes'],
        ['Snowy', 'Weekend', 'Lunch', 'No'],
        ['Snowy', 'Weekend', 'Evening', 'Yes']
    ]
    return result

def load_training_data():
    global dataset
    result = "Failed to load data"
    data_list = []
    if not os.path.exists(data_file):
        dataset = get_default_dataset()
        save_training_data()
        result = "Created default traffic_data.csv and loaded successfully"
    else:
        with open(data_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            if rows:
                if rows[0] == headers:
                    rows = rows[1:]
                for r in rows:
                    if len(r) == 4:
                        data_list.append([r[0].strip(), r[1].strip(), r[2].strip(), r[3].strip()])
        dataset = data_list
        result = f"Loaded {len(dataset)} records from {data_file} successfully"
    return result

def save_training_data():
    global dataset
    result = "No data to save"
    if dataset:
        with open(data_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for row in dataset:
                writer.writerow(row)
        result = f"Saved {len(dataset)} records to {data_file} successfully"
    return result

def show_training_data():
    global dataset
    result = "No training data available"
    if dataset:
        lines = []
        lines.append(f"{'No.':<5} {'Weather':<12} {'TimeOfWeek':<14} {'TimeOfDay':<12} {'TrafficJam':<10}")
        lines.append("-" * 55)
        for idx, row in enumerate(dataset, start=1):
            lines.append(f"{idx:<5} {row[0]:<12} {row[1]:<14} {row[2]:<12} {row[3]:<10}")
        lines.append("-" * 55)
        lines.append(f"Total: {len(dataset)} records")
        result = "\n".join(lines)
    return result

def add_training_data():
    global dataset
    result = "Invalid input. Record not added."
    weather = input("Enter Weather (Clear/Rainy/Snowy): ").strip().capitalize()
    time_of_week = input("Enter TimeOfWeek (Workday/Weekend): ").strip().capitalize()
    time_of_day = input("Enter TimeOfDay (Morning/Lunch/Evening): ").strip().capitalize()
    traffic_jam = input("Enter TrafficJam (Yes/No): ").strip().capitalize()
    if weather in ['Clear', 'Rainy', 'Snowy'] and time_of_week in ['Workday', 'Weekend'] and time_of_day in ['Morning', 'Lunch', 'Evening'] and traffic_jam in ['Yes', 'No']:
        dataset.append([weather, time_of_week, time_of_day, traffic_jam])
        save_training_data()
        result = f"Added record [{weather}, {time_of_week}, {time_of_day}, {traffic_jam}] successfully"
    return result

def edit_training_data():
    global dataset
    result = "No training data to edit"
    if dataset:
        print(show_training_data())
        val = input("Enter record number to edit: ").strip()
        if val.isdigit():
            idx = int(val) - 1
            if 0 <= idx < len(dataset):
                curr = dataset[idx]
                w = input(f"Enter Weather [{curr[0]}]: ").strip().capitalize()
                tow = input(f"Enter TimeOfWeek [{curr[1]}]: ").strip().capitalize()
                tod = input(f"Enter TimeOfDay [{curr[2]}]: ").strip().capitalize()
                tj = input(f"Enter TrafficJam [{curr[3]}]: ").strip().capitalize()
                if w in ['Clear', 'Rainy', 'Snowy']:
                    curr[0] = w
                if tow in ['Workday', 'Weekend']:
                    curr[1] = tow
                if tod in ['Morning', 'Lunch', 'Evening']:
                    curr[2] = tod
                if tj in ['Yes', 'No']:
                    curr[3] = tj
                dataset[idx] = curr
                save_training_data()
                result = f"Record #{val} updated to {curr} successfully"
            else:
                result = "Record number out of range"
        else:
            result = "Invalid record number"
    return result

def search_training_data():
    global dataset
    result = "No training data available"
    if dataset:
        keyword = input("Enter keyword to search (e.g. Clear, Workday, Yes): ").strip().lower()
        if keyword:
            matches = []
            for idx, row in enumerate(dataset, start=1):
                if any(keyword in str(item).lower() for item in row):
                    matches.append(f"{idx:<5} {row[0]:<12} {row[1]:<14} {row[2]:<12} {row[3]:<10}")
            if matches:
                lines = [f"Search results for '{keyword}':", f"{'No.':<5} {'Weather':<12} {'TimeOfWeek':<14} {'TimeOfDay':<12} {'TrafficJam':<10}", "-" * 55]
                lines.extend(matches)
                lines.append(f"Found {len(matches)} matching records")
                result = "\n".join(lines)
            else:
                result = f"No records matching '{keyword}' found"
        else:
            result = "Search keyword cannot be empty"
    return result

def delete_training_data():
    global dataset
    result = "No training data to delete"
    if dataset:
        print(show_training_data())
        val = input("Enter record number to delete: ").strip()
        if val.isdigit():
            idx = int(val) - 1
            if 0 <= idx < len(dataset):
                removed = dataset.pop(idx)
                save_training_data()
                result = f"Deleted record #{val} {removed} successfully"
            else:
                result = "Record number out of range"
        else:
            result = "Invalid record number"
    return result

def gini_index(groups, classes):
    result = 0.0
    n_instances = float(sum([len(group) for group in groups]))
    if n_instances > 0:
        gini = 0.0
        for group in groups:
            size = float(len(group))
            if size > 0:
                score = 0.0
                for class_val in classes:
                    p = [row[-1] for row in group].count(class_val) / size
                    score += p * p
                gini += (1.0 - score) * (size / n_instances)
        result = gini
    return result

def test_split(index, value, data):
    result = ([], [])
    left = []
    right = []
    for row in data:
        if row[index] == value:
            left.append(row)
        else:
            right.append(row)
    result = (left, right)
    return result

def get_split(data):
    result = {}
    class_values = list(set(row[-1] for row in data))
    b_index = 999
    b_value = 999
    b_score = 999.0
    b_groups = None
    for index in range(len(data[0]) - 1):
        for row in data:
            groups = test_split(index, row[index], data)
            gini = gini_index(groups, class_values)
            if gini < b_score:
                b_index = index
                b_value = row[index]
                b_score = gini
                b_groups = groups
    result = {'index': b_index, 'value': b_value, 'groups': b_groups}
    return result

def to_terminal(group):
    result = "No"
    if group:
        outcomes = [row[-1] for row in group]
        result = max(set(outcomes), key=outcomes.count)
    return result

def split_node(node, max_depth, min_size, depth):
    result = None
    left, right = node['groups']
    del(node['groups'])
    if not left or not right:
        node['left'] = node['right'] = to_terminal(left + right)
        result = node
    elif depth >= max_depth:
        node['left'] = to_terminal(left)
        node['right'] = to_terminal(right)
        result = node
    else:
        if len(set(r[-1] for r in left)) == 1 or len(left) <= min_size:
            node['left'] = to_terminal(left)
        else:
            node['left'] = get_split(left)
            split_node(node['left'], max_depth, min_size, depth + 1)
        if len(set(r[-1] for r in right)) == 1 or len(right) <= min_size:
            node['right'] = to_terminal(right)
        else:
            node['right'] = get_split(right)
            split_node(node['right'], max_depth, min_size, depth + 1)
        result = node
    return result

def build_tree(train, max_depth=5, min_size=1):
    result = None
    if train:
        root = get_split(train)
        split_node(root, max_depth, min_size, 1)
        result = root
    return result

def predict(node, row):
    result = "No"
    if not isinstance(node, dict):
        result = node
    else:
        if row[node['index']] == node['value']:
            result = predict(node['left'], row)
        else:
            result = predict(node['right'], row)
    return result

def format_tree_text(node, depth=0, branch='Root'):
    result = ""
    indent = "  " * depth
    if isinstance(node, dict):
        attr = headers[node['index']]
        val = node['value']
        left_str = format_tree_text(node['left'], depth + 1, 'YES')
        right_str = format_tree_text(node['right'], depth + 1, 'NO')
        result = f"{indent}[{branch}] IF {attr} == '{val}':\n{left_str}\n{right_str}"
    else:
        result = f"{indent}[{branch}] -> PREDICT TrafficJam = {node}"
    return result

def get_tree_layout(node, depth=0, x_left=0.0, x_right=1.0, positions=None, edges=None):
    if positions is None:
        positions = {}
    if edges is None:
        edges = []
    x = (x_left + x_right) / 2.0
    y = 1.0 - depth * 0.22
    node_id = len(positions)
    positions[node_id] = (x, y, node)
    if isinstance(node, dict):
        attr = headers[node['index']]
        val = node['value']
        label = f"{attr} == '{val}'"
        positions[node_id] = (x, y, label, False)
        left_id, _, _ = get_tree_layout(node['left'], depth + 1, x_left, x, positions, edges)
        edges.append((node_id, left_id, 'Yes'))
        right_id, _, _ = get_tree_layout(node['right'], depth + 1, x, x_right, positions, edges)
        edges.append((node_id, right_id, 'No'))
    else:
        positions[node_id] = (x, y, f"TrafficJam: {node}", True)
    result = (node_id, positions, edges)
    return result

def generate_tree_image(tree, filename='decision_tree.png'):
    result = "Failed to generate image"
    if tree:
        _, positions, edges = get_tree_layout(tree)
        fig, ax = plt.subplots(figsize=(12, 7), dpi=150)
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.05, 1.1)
        ax.axis('off')
        for p1_id, p2_id, elabel in edges:
            x1, y1 = positions[p1_id][0], positions[p1_id][1]
            x2, y2 = positions[p2_id][0], positions[p2_id][1]
            ax.plot([x1, x2], [y1, y2], color='#334155', linewidth=1.5, zorder=1)
            mx = (x1 + x2) / 2.0
            my = (y1 + y2) / 2.0
            ax.text(mx, my, elabel, fontsize=9, color='#1e293b', ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='#ffffff', edgecolor='#cbd5e1'), zorder=3)
        for nid, (x, y, text, is_leaf) in positions.items():
            if is_leaf:
                fcolor = '#dcfce7' if 'Yes' in text else '#fee2e2'
                ecolor = '#16a34a' if 'Yes' in text else '#dc2626'
                ax.text(x, y, text, fontsize=9, fontweight='bold', ha='center', va='center',
                        bbox=dict(boxstyle='round,pad=0.4', facecolor=fcolor, edgecolor=ecolor, linewidth=1.5), zorder=4)
            else:
                ax.text(x, y, text, fontsize=9, ha='center', va='center',
                        bbox=dict(boxstyle='square,pad=0.4', facecolor='#f8fafc', edgecolor='#0f172a', linewidth=1.5), zorder=4)
        plt.title("Decision Tree Model - Traffic Jam Prediction", fontsize=13, fontweight='bold', pad=15)
        plt.savefig(filename, bbox_inches='tight', facecolor='#ffffff')
        plt.close()
        result = f"Generated decision tree image: {filename}"
    return result

def train_decision_tree():
    global current_tree, dataset
    result = "No training data available to train"
    if dataset:
        current_tree = build_tree(dataset)
        save_tree_file()
        generate_tree_image(current_tree, tree_img_name)
        result = "Decision Tree trained successfully and saved to decision_tree.json & decision_tree.png"
    return result

def show_tree_structure():
    global current_tree
    result = "Decision Tree has not been trained or loaded yet."
    if current_tree:
        lines = ["=== Decision Tree Structure ===", format_tree_text(current_tree)]
        result = "\n".join(lines)
    return result

def load_tree_file():
    global current_tree
    result = "Failed to load decision tree file"
    if os.path.exists(model_file):
        with open(model_file, 'r', encoding='utf-8') as f:
            current_tree = json.load(f)
        generate_tree_image(current_tree, tree_img_name)
        result = f"Loaded Decision Tree from {model_file} successfully"
    else:
        result = f"File {model_file} does not exist. Please train the tree first."
    return result

def save_tree_file():
    global current_tree
    result = "No decision tree to save"
    if current_tree:
        with open(model_file, 'w', encoding='utf-8') as f:
            json.dump(current_tree, f, indent=2)
        result = f"Saved Decision Tree to {model_file} successfully"
    return result

def test_decision_tree():
    global current_tree
    result = "Decision Tree has not been trained or loaded yet. Please run option 8 or 10 first."
    if current_tree:
        weather = input("Enter Weather (Clear/Rainy/Snowy): ").strip().capitalize()
        time_of_week = input("Enter TimeOfWeek (Workday/Weekend): ").strip().capitalize()
        time_of_day = input("Enter TimeOfDay (Morning/Lunch/Evening): ").strip().capitalize()
        if weather in ['Clear', 'Rainy', 'Snowy'] and time_of_week in ['Workday', 'Weekend'] and time_of_day in ['Morning', 'Lunch', 'Evening']:
            sample = [weather, time_of_week, time_of_day]
            pred = predict(current_tree, sample)
            lines = [
                "=== Test Result ===",
                f"Input: Weather={weather}, TimeOfWeek={time_of_week}, TimeOfDay={time_of_day}",
                f"Predicted TrafficJam: {pred}"
            ]
            result = "\n".join(lines)
        else:
            result = "Invalid input values. Please use valid categories."
    return result

def readKey():
    result = 0
    print("\n" + "=" * 45)
    print("      TRAFFIC JAM PREDICTION SYSTEM")
    print("=" * 45)
    print("1. โหลดข้อมูลสอน (Load Training Data)")
    print("2. บันทึกข้อมูลสอน (Save Training Data)")
    print("3. แสดงข้อมูลสอน (Show Training Data)")
    print("4. เพิ่มข้อมูลสอน (Add Training Data)")
    print("5. แก้ไขข้อมูลสอน (Edit Training Data)")
    print("6. ค้นหาข้อมูลสอน (Search Training Data)")
    print("7. ลบข้อมูลสอน (Delete Training Data)")
    print("8. สอน (Train Decision Tree)")
    print("9. แสดงโครงสร้าง Decision Tree (Show Tree)")
    print("10. โหลด Decision Tree (Load Tree)")
    print("11. บันทึก Decision Tree (Save Tree)")
    print("12. ทดสอบ (Test / Predict)")
    print("13. ออกจากโปรแกรม (Exit)")
    print("=" * 45)
    val = input("Select choice (1-13): ").strip().replace(".", "")
    if val.isdigit():
        result = int(val)
    return result

def process(num):
    result = "Invalid choice"
    if num == 1:
        result = load_training_data()
    elif num == 2:
        result = save_training_data()
    elif num == 3:
        result = show_training_data()
    elif num == 4:
        result = add_training_data()
    elif num == 5:
        result = edit_training_data()
    elif num == 6:
        result = search_training_data()
    elif num == 7:
        result = delete_training_data()
    elif num == 8:
        result = train_decision_tree()
    elif num == 9:
        result = show_tree_structure()
    elif num == 10:
        result = load_tree_file()
    elif num == 11:
        result = save_tree_file()
    elif num == 12:
        result = test_decision_tree()
    elif num == 13:
        result = "Exit"
    return result

def output(result):
    if result:
        print("\n" + str(result))
        if result == "Exit":
            sys.exit(0)
    return None

def main():
    load_training_data()
    train_decision_tree()
    while True:
        num = readKey()
        result = process(num)
        output(result)

if __name__ == '__main__':
    main()
