# Flowchart - Binary Tree Program

Documentation and flowcharts for the Binary Tree Search and Management Program with Breadth-First Search (BFS) and Cascade Delete.
All functions follow structured single-exit design (a single `return result` per function).

---

## 1. Main Program Flowchart (`main()`)

```mermaid
flowchart TD
    Start([Start main()]) --> Loop{while True}
    Loop --> ReadKey[/num = readKey()/]
    ReadKey --> Process[result = process(num)]
    Process --> Output[output(result)]
    Output --> Loop
```

---

## 2. Menu Input (`readKey()`) - Single Return

```mermaid
flowchart TD
    Start([Start readKey()]) --> Init[result = 0]
    Init --> PrintMenu[/print menu:\n1. Show  2. Add  3. Edit\n4. Search  5. Delete  6. Exit/]
    PrintMenu --> InputVal[/val = input('choice')/]
    InputVal --> Clean[val = val.strip().replace('.', '')]
    Clean --> CheckDigit{val.isdigit() ?}
    CheckDigit -- Yes --> SetResult[result = int(val)] --> Ret
    CheckDigit -- No --> Ret[/return result/]
    Ret --> End([End readKey()])
```

---

## 3. Menu Dispatcher (`process(num)`) - Single Return

```mermaid
flowchart TD
    Start([Start process(num)]) --> Init[result = 'Invalid choice']
    Init --> CheckNum{Check num}
    CheckNum -- 1 --> F1[result = show_data()] --> Ret
    CheckNum -- 2 --> F2[result = add_data()] --> Ret
    CheckNum -- 3 --> F3[result = edit_data()] --> Ret
    CheckNum -- 4 --> F4[result = search_data()] --> Ret
    CheckNum -- 5 --> F5[result = delete_data()] --> Ret
    CheckNum -- 6 --> F6[result = 'Exit'] --> Ret
    CheckNum -- Other --> Ret[/return result/]
    Ret --> End([End process(num)])
```

---

## 4. Show Data (`show_data()`) - Single Return

```mermaid
flowchart TD
    Start([Start show_data()]) --> Init[result = 'No data']
    Init --> CheckGraph{if graph :}
    CheckGraph -- Yes --> BuildLines[lines = []\nfor k, v in graph.items():\nlines.append(f'{k} : {v}')\nresult = '\n'.join(lines)] --> Ret
    CheckGraph -- No --> Ret[/return result/]
    Ret --> End([End show_data()])
```

---

## 5. Add Data (`add_data()`) - Single Return

```mermaid
flowchart TD
    Start([Start add_data()]) --> Init[result = 'Invalid input']
    Init --> InputData[/node_name = input('node')\nleft = input('left')\nright = input('right')/]
    InputData --> CheckName{if node_name :}
    CheckName -- Yes --> BuildChildren[children = []\nif left: children.append(left)\nif right: children.append(right)\ngraph[node_name] = children\nsave_file(graph)\nresult = 'Add success'] --> Ret
    CheckName -- No --> Ret[/return result/]
    Ret --> End([End add_data()])
```

---

## 6. Edit Data (`edit_data()`) - Single Return

```mermaid
flowchart TD
    Start([Start edit_data()]) --> Init[result = 'Node not found']
    Init --> InputNode[/node_name = input('node to edit')/]
    InputNode --> CheckInGraph{node_name in graph ?}
    CheckInGraph -- Yes --> EditProc[left = input('new left')\nright = input('new right')\nchildren = []\nif left: children.append(left)\nif right: children.append(right)\ngraph[node_name] = children\nsave_file(graph)\nresult = 'Edit success'] --> Ret
    CheckInGraph -- No --> Ret[/return result/]
    Ret --> End([End edit_data()])
```

---

## 7. Breadth-First Search (`BFS(graph, start, dest)`) - Single Return

```mermaid
flowchart TD
    Start([Start BFS(graph, start, dest)]) --> Init[queue = [start], visited = []\nresult = ['Not reachable', []]]
    Init --> LoopQueue{while queue}
    LoopQueue -- Yes --> PopNode[node = queue.pop(0)\nvisited.append(node)]
    PopNode --> CheckDest{node == dest ?}
    CheckDest -- Yes --> PrintFound[print(f'{node} : {queue}')\nresult[0] = 'Reachable'\nbreak] --> SetRet
    CheckDest -- No --> ExpandChildren[for child in graph.get(node, []):\nif child not in visited and child not in queue:\nqueue.append(child)\nprint(f'{node} : {queue}')] --> LoopQueue
    LoopQueue -- No --> SetRet[result[1] = visited] --> Ret[/return result/]
    Ret --> End([End BFS()])
```

---

## 8. Search Data (`search_data()`) - Single Return

```mermaid
flowchart TD
    Start([Start search_data()]) --> Init[result = ['Tree is empty', []]]
    Init --> InputTarget[/target = input('Enter target node: ')/]
    InputTarget --> GetRoot[start = 'A' if 'A' in graph else list(keys)[0]]
    GetRoot --> CheckRoot{if start :}
    CheckRoot -- Yes --> CallBFS[result = BFS(graph, start, target)] --> Ret
    CheckRoot -- No --> Ret[/return result/]
    Ret --> End([End search_data()])
```

---

## 9. Delete Data with Cascade Subtree (`delete_data()`) - Single Return

```mermaid
flowchart TD
    Start([Start delete_data()]) --> Init[result = 'Node not found']
    Init --> InputNode[/node_name = input('Enter node to delete: ')/]
    InputNode --> CheckInGraph{node_name in graph ?}
    CheckInGraph -- Yes --> CascadeDel[to_delete = [node_name]\nBFS collect all descendants in subtree\nfor n in to_delete: del graph[n]\nremove node_name from parents\nsave_file(graph)\nresult = 'Delete success'] --> Ret
    CheckInGraph -- No --> Ret[/return result/]
    Ret --> End([End delete_data()])
```

---

## 10. Output Handler (`output(result)`)

```mermaid
flowchart TD
    Start([Start output(result)]) --> CheckNone{result is None ?}
    CheckNone -- Yes --> Ret[return] --> End([End output()])
    CheckNone -- No --> CheckList{isinstance(result, list) and len == 2 ?}
    CheckList -- Yes --> PrintBFS[/print(result[0])\nprint('Path used to traverse :', path)/] --> End
    CheckList -- No --> PrintResult[/print(result)/]
    PrintResult --> CheckExit{result == 'Exit' ?}
    CheckExit -- Yes --> SysExit[sys.exit()]
    CheckExit -- No --> End
```

---

## 11. File I/O (`load_file()` & `save_file(data)`)

```mermaid
flowchart TD
    subgraph load_file
        L_Start([Start load_file()]) --> L_Check{tree.csv exists ?}
        L_Check -- Yes --> L_Read[Read lines & parse CSV\ndata[k] = children] --> L_Ret
        L_Check -- No --> L_Init[Init default A - O\nsave_file(data)] --> L_Ret
        L_Ret[/return data/] --> L_End([End load_file()])
    end

    subgraph save_file
        S_Start([Start save_file(data)]) --> S_Open[open('tree.csv', 'w')\nwrite header 'node,left,right']
        S_Open --> S_Loop[for k, children in data.items():\nf.write(f'{k},{left},{right}\n')]
        S_Loop --> S_Close[close file] --> S_End([End save_file()])
    end
```
