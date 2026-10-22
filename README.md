# Page Replacement Algorithm Simulator

Mini-project for **21CSC202J – Operating Systems** (SRM Institute of Science and Technology, Ramapuram).

A Python simulator that runs **FIFO** and **Optimal** page replacement (plus **LRU** as a bonus) on a page reference string, shows a step-by-step frame table, and compares page faults.

## Concepts covered
Virtual memory, demand paging, page faults, page replacement, Belady's anomaly.

## Requirements
Python 3.8+ (standard library only).

## Run
```bash
# Built-in textbook example (20 references, 3 frames)
python page_replacement.py

# Custom input
python page_replacement.py -r 7 0 1 2 0 3 0 4 2 3 0 3 2 -f 3

# Only some algorithms
python page_replacement.py -r 1 2 3 4 1 2 5 1 2 3 4 5 -f 4 --algo fifo optimal
```

## Test
```bash
python -m unittest -v
```

## Expected results (reference string `7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1`, 3 frames)
| Algorithm | Page faults |
|-----------|-------------|
| Optimal   | 9           |
| LRU       | 12          |
| FIFO      | 15          |

## How each algorithm works
- **FIFO** – evicts the page that has been in memory the longest (queue).
- **Optimal** – evicts the page whose next use is farthest in the future. Gives the minimum possible faults but needs future knowledge, so it is used as a benchmark.
- **LRU** – evicts the page not used for the longest time.

## Belady's anomaly
FIFO on `1 2 3 4 1 2 5 1 2 3 4 5` gives 9 faults with 3 frames but 10 with 4 frames. This is covered by a unit test.

## Team
Add your names and register numbers here.
