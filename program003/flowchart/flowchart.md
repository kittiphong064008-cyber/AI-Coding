# Flowchart - Decision Tree Traffic Jam Prediction Program

Documentation and flowcharts for the Traffic Jam Prediction System using Decision Tree (`program003`).
All functions follow structured single-exit design (exactly 1 `return result` per function, zero comments in code, English-only labels in flowcharts).

---

## Overview of Files

| Filename | Function | Description |
|---|---|---|
| [`01_main.png`](./01_main.png) / [`.drawio`](./01_main.drawio) | `main()` | Continuous event loop (`readKey` -> `process` -> `output`) |
| [`02_readKey.png`](./02_readKey.png) / [`.drawio`](./02_readKey.drawio) | `readKey()` | Display 13 options menu, sanitize input and parse choice |
| [`03_process.png`](./03_process.png) / [`.drawio`](./03_process.drawio) | `process(num)` | Menu dispatcher mapping numbers 1-13 to function calls |
| [`04_show_training_data.png`](./04_show_training_data.png) / [`.drawio`](./04_show_training_data.drawio) | `show_training_data()` | Formats and displays all training dataset records |
| [`05_add_training_data.png`](./05_add_training_data.png) / [`.drawio`](./05_add_training_data.drawio) | `add_training_data()` | Adds a new training record with validation and saves |
| [`06_edit_training_data.png`](./06_edit_training_data.png) / [`.drawio`](./06_edit_training_data.drawio) | `edit_training_data()` | Modifies existing record attributes and updates file |
| [`07_search_training_data.png`](./07_search_training_data.png) / [`.drawio`](./07_search_training_data.drawio) | `search_training_data()` | Searches dataset by keyword across all columns |
| [`08_delete_training_data.png`](./08_delete_training_data.png) / [`.drawio`](./08_delete_training_data.drawio) | `delete_training_data()` | Removes a training record by index and updates file |
| [`09_train_decision_tree.png`](./09_train_decision_tree.png) / [`.drawio`](./09_train_decision_tree.drawio) | `train_decision_tree()` | Trains Decision Tree, saves JSON model and generates PNG plot |
| [`10_build_tree.png`](./10_build_tree.png) / [`.drawio`](./10_build_tree.drawio) | `build_tree(train)` | Recursive CART tree construction using Gini index |
| [`11_gini_index.png`](./11_gini_index.png) / [`.drawio`](./11_gini_index.drawio) | `gini_index(groups, classes)` | Calculates Gini Impurity metric for split evaluation |
| [`12_get_split.png`](./12_get_split.png) / [`.drawio`](./12_get_split.drawio) | `get_split(data)` | Evaluates all attribute values to find best split |
| [`13_show_tree_structure.png`](./13_show_tree_structure.png) / [`.drawio`](./13_show_tree_structure.drawio) | `show_tree_structure()` | Formats indented hierarchy of the decision tree |
| [`14_file_io.png`](./14_file_io.png) / [`.drawio`](./14_file_io.drawio) | `load/save data & tree` | Reads and writes CSV dataset and JSON tree model |
| [`15_test_decision_tree.png`](./15_test_decision_tree.png) / [`.drawio`](./15_test_decision_tree.drawio) | `test_decision_tree()` | Prompts sample attributes and predicts TrafficJam class |
| [`16_output.png`](./16_output.png) / [`.drawio`](./16_output.drawio) | `output(result)` | Prints operation results or handles program exit |
| [`flowchart.png`](./flowchart.png) / [`.drawio`](./flowchart.drawio) | Master Unified Canvas | Complete master diagram containing all 16 functions |

---

## 1. Main Program Loop (`main()`)

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
    Init --> PrintMenu[Print menu (1 to 13)]
    PrintMenu --> InputVal[val = input('choice')]
    InputVal --> Clean[val = val.strip().replace('.', '')]
    Clean --> CheckDigit{val.isdigit()}
    CheckDigit -- yes --> SetResult[result = int(val)] --> Join(( ))
    CheckDigit -- no --> Join
    Join --> Ret[return result]
    Ret --> End([Return])
```

---

## 3. Menu Dispatcher (`process(num)`) - Single Return

```mermaid
flowchart TD
    Start([process(num)]) --> Init[result = 'Invalid choice']
    Init --> C1{num == 1}
    C1 -- yes --> R1[result = load_training_data()] --> Join(( ))
    C1 -- no --> C2{num == 2}
    C2 -- yes --> R2[result = save_training_data()] --> Join
    C2 -- no --> C3{num == 3}
    C3 -- yes --> R3[result = show_training_data()] --> Join
    C3 -- no --> C4{num == 4}
    C4 -- yes --> R4[result = add_training_data()] --> Join
    C4 -- no --> C5{num == 5}
    C5 -- yes --> R5[result = edit_training_data()] --> Join
    C5 -- no --> C6{num == 6}
    C6 -- yes --> R6[result = search_training_data()] --> Join
    C6 -- no --> C7{num == 7}
    C7 -- yes --> R7[result = delete_training_data()] --> Join
    C7 -- no --> C8{num == 8}
    C8 -- yes --> R8[result = train_decision_tree()] --> Join
    C8 -- no --> C9{num == 9}
    C9 -- yes --> R9[result = show_tree_structure()] --> Join
    C9 -- no --> C10{num == 10}
    C10 -- yes --> R10[result = load_tree_file()] --> Join
    C10 -- no --> C11{num == 11}
    C11 -- yes --> R11[result = save_tree_file()] --> Join
    C11 -- no --> C12{num == 12}
    C12 -- yes --> R12[result = test_decision_tree()] --> Join
    C12 -- no --> C13{num == 13}
    C13 -- yes --> R13[result = 'Exit'] --> Join
    C13 -- no --> Join
    Join --> Ret[return result]
    Ret --> End([Return])
```

---

## 4. Show Training Data (`show_training_data()`) - Single Return

```mermaid
flowchart TD
    Start([show_training_data()]) --> Init[result = 'No training data available']
    Init --> CheckData{dataset not empty}
    CheckData -- yes --> Build[Format headers & table rows\nresult = formatted_string] --> Join(( ))
    CheckData -- no --> Join
    Join --> Ret[return result]
    Ret --> End([Return])
```

---

## 5. Add Training Data (`add_training_data()`) - Single Return

```mermaid
flowchart TD
    Start([add_training_data()]) --> Init[result = 'Invalid input. Not added.']
    Init --> InputFields[Input weather, time_of_week,\ntime_of_day, traffic_jam]
    InputFields --> CheckValid{Inputs in valid categories}
    CheckValid -- yes --> AppendRow[dataset.append(new_row)\nsave_training_data()\nresult = 'Added record successfully'] --> Join(( ))
    CheckValid -- no --> Join
    Join --> Ret[return result]
    Ret --> End([Return])
```

---

## 6. Edit Training Data (`edit_training_data()`) - Single Return

```mermaid
flowchart TD
    Start([edit_training_data()]) --> Init[result = 'No data to edit']
    Init --> CheckData{dataset not empty}
    CheckData -- no --> Join(( ))
    CheckData -- yes --> InputIdx[val = input('record number')]
    InputIdx --> CheckIdx{val.isdigit() &\n0 <= idx < len(dataset)}
    CheckIdx -- no --> SetErr[result = 'Invalid record number'] --> Join
    CheckIdx -- yes --> UpdateRow[Input new values\ndataset[idx] = updated\nsave_training_data()\nresult = 'Record updated'] --> Join
    Join --> Ret[return result]
    Ret --> End([Return])
```

---

## 7. Search Training Data (`search_training_data()`) - Single Return

```mermaid
flowchart TD
    Start([search_training_data()]) --> Init[result = 'No data available']
    Init --> CheckData{dataset not empty}
    CheckData -- no --> Join(( ))
    CheckData -- yes --> InputKw[keyword = input('keyword')]
    InputKw --> CheckKw{keyword not empty}
    CheckKw -- no --> SetErr[result = 'Keyword empty'] --> Join
    CheckKw -- yes --> FindMatches[Find rows containing keyword\nresult = formatted_matches] --> Join
    Join --> Ret[return result]
    Ret --> End([Return])
```

---

## 8. Delete Training Data (`delete_training_data()`) - Single Return

```mermaid
flowchart TD
    Start([delete_training_data()]) --> Init[result = 'No data to delete']
    Init --> CheckData{dataset not empty}
    CheckData -- no --> Join(( ))
    CheckData -- yes --> InputIdx[val = input('record number')]
    InputIdx --> CheckIdx{val.isdigit() &\n0 <= idx < len(dataset)}
    CheckIdx -- no --> SetErr[result = 'Invalid record number'] --> Join
    CheckIdx -- yes --> PopRow[removed = dataset.pop(idx)\nsave_training_data()\nresult = 'Deleted successfully'] --> Join
    Join --> Ret[return result]
    Ret --> End([Return])
```

---

## 9. Train Decision Tree (`train_decision_tree()`) - Single Return

```mermaid
flowchart TD
    Start([train_decision_tree()]) --> Init[result = 'No data available']
    Init --> CheckData{dataset not empty}
    CheckData -- no --> Join(( ))
    CheckData -- yes --> TrainWork[current_tree = build_tree(dataset)\nsave_tree_file()\ngenerate_tree_image(current_tree)\nresult = 'Trained successfully'] --> Join
    Join --> Ret[return result]
    Ret --> End([Return])
```

---

## 10. Build Tree (`build_tree(train)`) - Single Return

```mermaid
flowchart TD
    Start([build_tree(train)]) --> Init[result = None]
    Init --> CheckTrain{train not empty}
    CheckTrain -- no --> Join(( ))
    CheckTrain -- yes --> BuildWork[root = get_split(train)\nsplit_node(root, max_depth, 1, 1)\nresult = root] --> Join
    Join --> Ret[return result]
    Ret --> End([Return])
```

---

## 11. Gini Impurity Metric (`gini_index(groups, classes)`) - Single Return

```mermaid
flowchart TD
    Start([gini_index(groups, classes)]) --> Init[result = 0.0\nn_instances = sum(len(g))]
    Init --> CheckSize{n_instances > 0}
    CheckSize -- no --> Join(( ))
    CheckSize -- yes --> CalcGini[for group in groups:\n  size = len(group)\n  score = sum(p^2 for class in classes)\n  gini += (1-score)*(size/n_instances)\nresult = gini] --> Join
    Join --> Ret[return result]
    Ret --> End([Return])
```

---

## 12. Best Split Evaluation (`get_split(data)`) - Single Return

```mermaid
flowchart TD
    Start([get_split(data)]) --> Init[b_idx, b_val, b_score = 999, 999, 999.0\nb_groups = None]
    Init --> LoopAll[for index in range(columns-1):\n  for row in data:\n    groups = test_split(index, row[index])\n    gini = gini_index(groups, classes)]
    LoopAll --> CheckBest{gini < b_score}
    CheckBest -- yes --> SaveBest[b_idx = index\nb_val = row[index]\nb_score = gini\nb_groups = groups] --> Join(( ))
    CheckBest -- no --> Join
    Join --> Ret[return {'index': b_idx, 'value': b_val, 'groups': b_groups}]
    Ret --> End([Return])
```

---

## 13. Tree Structure Display (`show_tree_structure()`) - Single Return

```mermaid
flowchart TD
    Start([show_tree_structure()]) --> Init[result = 'Tree not trained yet']
    Init --> CheckTree{current_tree not None}
    CheckTree -- no --> Join(( ))
    CheckTree -- yes --> FormatTree[result = format_tree_text(current_tree)] --> Join
    Join --> Ret[return result]
    Ret --> End([Return])
```

---

## 14. File IO Operations (`load/save data & tree`)

```mermaid
flowchart TD
    subgraph DataIO[Data File Operations]
        DStart([load_training_data()]) --> DChk{traffic_data.csv exists}
        DChk -- yes --> DRead[Read rows & set dataset] --> DJ(( ))
        DChk -- no --> DDef[dataset = default\nsave_training_data()] --> DJ
        DJ --> DRet[return result] --> DEnd([Return])
    end

    subgraph TreeIO[Tree Model Operations]
        TStart([load_tree_file()]) --> TChk{decision_tree.json exists}
        TChk -- yes --> TRead[current_tree = json.load(f)\ngenerate_tree_image()] --> TJ(( ))
        TChk -- no --> TJ
        TJ --> TRet[return result] --> TEnd([Return])
    end
```

---

## 15. Test & Predict (`test_decision_tree()`) - Single Return

```mermaid
flowchart TD
    Start([test_decision_tree()]) --> Init[result = 'Tree not trained yet']
    Init --> CheckTree{current_tree not None}
    CheckTree -- no --> Join(( ))
    CheckTree -- yes --> InputSample[Input weather, time_of_week,\ntime_of_day]
    InputSample --> CheckInput{Inputs valid categories}
    CheckInput -- no --> SetErr[result = 'Invalid categories'] --> Join
    CheckInput -- yes --> PredictSample[pred = predict(current_tree, sample)\nresult = f'TrafficJam: {pred}'] --> Join
    Join --> Ret[return result]
    Ret --> End([Return])
```

---

## 16. Output & Exit Handler (`output(result)`)

```mermaid
flowchart TD
    Start([output(result)]) --> ChkNone{result is None}
    ChkNone -- yes --> Join(( ))
    ChkNone -- no --> PrintRes[print(result)]
    PrintRes --> ChkExit{result == 'Exit'}
    ChkExit -- yes --> DoExit[sys.exit(0)] --> Join
    ChkExit -- no --> Join
    Join --> Ret[return None]
    Ret --> End([Return])
```
