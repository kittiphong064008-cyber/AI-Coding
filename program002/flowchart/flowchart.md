# Flowchart - A* Search Program (Robot Food Delivery)

Documentation and flowcharts for the A* Search Robot Food Delivery System (`program002`).
All functions follow structured single-exit design (exactly 1 `return result` per function, zero comments in code, English-only labels in flowcharts).

---

## Overview of Files

| Filename | Function | Description |
|---|---|---|
| [`01_main.png`](./01_main.png) / [`.drawio`](./01_main.drawio) | `main()` | Continuous event loop (`readKey` -> `process` -> `output`) |
| [`02_readKey.png`](./02_readKey.png) / [`.drawio`](./02_readKey.drawio) | `readKey()` | Display 6 options menu, sanitise input and parse choice |
| [`03_process.png`](./03_process.png) / [`.drawio`](./03_process.drawio) | `process(num)` | Menu dispatcher mapping numbers 1-6 to function calls |
| [`04_show_data.png`](./04_show_data.png) / [`.drawio`](./04_show_data.drawio) | `show_data()` | Formats and displays table coords, neighbors, and SLD |
| [`05_add_data.png`](./05_add_data.png) / [`.drawio`](./05_add_data.drawio) | `add_data()` | Adds a new table with coordinates, neighbors and SLD heuristic |
| [`06_edit_data.png`](./06_edit_data.png) / [`.drawio`](./06_edit_data.drawio) | `edit_data()` | Modifies existing table coordinates, neighbors and SLD |
| [`07_delete_data.png`](./07_delete_data.png) / [`.drawio`](./07_delete_data.drawio) | `delete_data()` | Removes a table and cleans up references from all neighbors |
| [`08_search_data.png`](./08_search_data.png) / [`.drawio`](./08_search_data.drawio) | `search_data()` | Prompts start & destination and executes A* search |
| [`09_a_star_search.png`](./09_a_star_search.png) / [`.drawio`](./09_a_star_search.drawio) | `a_star_search(...)` | Core A* Search algorithm evaluating $f(n) = g(n) + h(n)$ |
| [`10_output.png`](./10_output.png) / [`.drawio`](./10_output.drawio) | `output(result)` | Prints formatted results or handles program exit |
| [`11_file_io.png`](./11_file_io.png) / [`.drawio`](./11_file_io.drawio) | `load_file()`, `save_file()` | Reads from and writes to `tables.csv` |
| [`12_generate_map.png`](./12_generate_map.png) / [`.drawio`](./12_generate_map.drawio) | `generate_map(data)` | Plots restaurant floor plan map with tables and distances |
| [`flowchart.png`](./flowchart.png) / [`.drawio`](./flowchart.drawio) | Unified Canvas | Complete master diagram containing all 12 functions |

---

## 1. Main Loop (`main()`)

```mermaid
flowchart TD
    Start([main()]) --> Loop(( ))
    Loop --> ReadKey[num = readKey()]
    ReadKey --> Process[result = process(num)]
    Process --> Output[output(result)]
    Output --> Loop
```

---

## 2. Menu Input (`readKey()`) - Single Return

```mermaid
flowchart TD
    Start([readKey()]) --> Init[result = 0]
    Init --> PrintMenu[Print menu (1 to 6)]
    PrintMenu --> InputVal[val = input('choice')]
    InputVal --> Clean[val = val.strip().replace('.', '')]
    Clean --> CheckDigit{val.isdigit()}
    CheckDigit -- yes --> SetResult[result = int(val)] --> Join(( ))
    CheckDigit -- no --> Join
    Join --> Ret[return result]
    Ret --> End([Return])
```

---

## 3. Dispatcher (`process(num)`) - Single Return

```mermaid
flowchart TD
    Start([process(num)]) --> Init[result = 'Invalid choice']
    Init --> C1{num == 1}
    C1 -- yes --> R1[result = show_data()] --> Join(( ))
    C1 -- no --> C2{num == 2}
    C2 -- yes --> R2[result = add_data()] --> Join
    C2 -- no --> C3{num == 3}
    C3 -- yes --> R3[result = edit_data()] --> Join
    C3 -- no --> C4{num == 4}
    C4 -- yes --> R4[result = delete_data()] --> Join
    C4 -- no --> C5{num == 5}
    C5 -- yes --> R5[result = search_data()] --> Join
    C5 -- no --> C6{num == 6}
    C6 -- yes --> R6[result = 'Exit'] --> Join
    C6 -- no --> Join
    Join --> Ret[return result]
    Ret --> End([Return])
```

---

## 4. Show Data (`show_data()`) - Single Return

```mermaid
flowchart TD
    Start([show_data()]) --> Init[result = 'No tables found']
    Init --> CheckData{data not empty}
    CheckData -- yes --> Build[Build formatted table list string\nresult = text] --> Join(( ))
    CheckData -- no --> Join
    Join --> Ret[return result]
    Ret --> End([Return])
```

---

## 5. Add Data (`add_data()`) - Single Return

```mermaid
flowchart TD
    Start([add_data()]) --> Init[result = 'Invalid input']
    Init --> InputName[table_name = input('table')]
    InputName --> CheckName{table_name not empty}
    CheckName -- yes --> InputDetails[Input x, y coordinates\nInput sld heuristic]
    InputDetails --> InputNeighbors[Input neighbors string e.g. 'T2:4, T3:6']
    InputNeighbors --> ParseNeighbors[Parse neighbors to dict]
    ParseNeighbors --> Save[graph[table_name] = {...}\nsave_file(graph)\nresult = 'Add success'] --> Join(( ))
    CheckName -- no --> Join
    Join --> Ret[return result]
    Ret --> End([Return])
```

---

## 6. Edit Data (`edit_data()`) - Single Return

```mermaid
flowchart TD
    Start([edit_data()]) --> Init[result = 'Table not found']
    Init --> InputName[table_name = input('table to edit')]
    InputName --> CheckExist{table_name in graph}
    CheckExist -- yes --> InputDetails[Input new x, y, sld\nInput new neighbors string]
    InputDetails --> Save[graph[table_name] = {...}\nsave_file(graph)\nresult = 'Edit success'] --> Join(( ))
    CheckExist -- no --> Join
    Join --> Ret[return result]
    Ret --> End([Return])
```

---

## 7. Delete Data (`delete_data()`) - Single Return

```mermaid
flowchart TD
    Start([delete_data()]) --> Init[result = 'Table not found']
    Init --> InputName[table_name = input('table')]
    InputName --> CheckExist{table_name in graph}
    CheckExist -- yes --> DeleteNode[del graph[table_name]]
    DeleteNode --> CleanNeighbors[Remove table from other neighbors]
    CleanNeighbors --> Save[save_file(graph)\nresult = 'Delete success'] --> Join(( ))
    CheckExist -- no --> Join
    Join --> Ret[return result]
    Ret --> End([Return])
```

---

## 8. Search Data Prompt (`search_data()`) - Single Return

```mermaid
flowchart TD
    Start([search_data()]) --> Init[result = ['No tables', []]]
    Init --> Inp1[start = input('start table')]
    Inp1 --> Inp2[dest = input('dest table')]
    Inp2 --> CheckEmpty{start & dest not empty}
    CheckEmpty -- yes --> CallAStar[result = a_star_search(graph, start, dest)] --> Join(( ))
    CheckEmpty -- no --> Join
    Join --> Ret[return result]
    Ret --> End([Return])
```

---

## 9. Core A* Search (`a_star_search(data, start, dest)`) - Single Return

```mermaid
flowchart TD
    Start([a_star_search(data, start, dest)]) --> Init[result = ['Not reachable', [], 0, []]]
    Init --> CheckValid{start in data and dest in data}
    CheckValid -- yes --> InitQ[open_list = [(start_h, 0, start, [start])]\nvisited = [], found = False]
    InitQ --> LoopJoin(( ))
    LoopJoin --> CheckLoop{open_list not empty and not found}
    CheckLoop -- yes --> PopNode[Sort open_list by f\ncurr = open_list.pop(0)\nvisited.append(curr_node)]
    PopNode --> CheckGoal{curr_node == dest}
    CheckGoal -- yes --> GoalFound[found = True\nfinal_path = curr_path\nfinal_cost = curr_g] --> LoopExit(( ))
    CheckGoal -- no --> ExpandNeighbors[for neighbor, dist in neighbors:\nnew_g = curr_g + dist\nnew_f = new_g + sld[neighbor]\nopen_list.append((new_f, new_g, ...))] --> LoopJoin
    CheckLoop -- no --> LoopExit
    LoopExit --> CheckFound{found is True}
    CheckFound -- yes --> SetResult[result = ['Reachable', final_path, final_cost, visited]] --> FinalJoin(( ))
    CheckFound -- no --> FinalJoin
    CheckValid -- no --> FinalJoin
    FinalJoin --> Ret[return result]
    Ret --> End([Return])
```

---

## 10. Output & Exit Handler (`output(result)`)

```mermaid
flowchart TD
    Start([output(result)]) --> ChkNone{result is None}
    ChkNone -- yes --> Join(( ))
    ChkNone -- no --> ChkList{isinstance(result, list) and len(result) >= 3}
    ChkList -- yes --> PrintStatus[print(result[0])]
    PrintStatus --> ChkReachable{result[0] == 'Reachable'}
    ChkReachable -- yes --> PrintDetails[print path, distance, visited] --> Join
    ChkReachable -- no --> Join
    ChkList -- no --> PrintStr[print(result)]
    PrintStr --> ChkExit{result == 'Exit'}
    ChkExit -- yes --> DoExit[sys.exit()] --> Join
    ChkExit -- no --> Join
    Join --> End([Return])
```

---

## 11. File IO (`load_file()` and `save_file(data)`)

```mermaid
flowchart TD
    subgraph Load[load_file()]
        LStart([load_file()]) --> LInit[data = {}]
        LInit --> LChk1{tables.csv exists}
        LChk1 -- yes --> LRead[Read lines & parse x, y, neighbors, sld] --> LJ1(( ))
        LChk1 -- no --> LJ1
        LJ1 --> LChk2{data is empty}
        LChk2 -- yes --> LDef[data = default T1 to T7\nsave_file(data)] --> LJ2(( ))
        LChk2 -- no --> LJ2
        LJ2 --> LRet[return data] --> LEnd([Return])
    end

    subgraph Save[save_file(data)]
        SStart([save_file(data)]) --> SOpen[open tables.csv for writing]
        SOpen --> SHead[Write CSV header]
        SHead --> SLoop[Write each table record]
        SLoop --> SClose[close file]
        SClose --> SMap[generate_map(data)]
        SMap --> SEnd([Return])
    end
```

---

## 12. Map Generation (`generate_map(data)`)

```mermaid
flowchart TD
    Start([generate_map(data)]) --> Init[result = 'Map created']
    Init --> Chk{data not empty}
    Chk -- yes --> Plot[Create figure & axis\nDraw edges & distance labels\nDraw table nodes circles\nDraw names and SLD labels\nsavefig 'restaurant_map.png'] --> Join(( ))
    Chk -- no --> Join
    Join --> Ret[return result]
    Ret --> End([Return])
```
