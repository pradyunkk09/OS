"""Page Replacement Algorithm Simulator (FIFO, Optimal, LRU).

21CSC202J - Operating Systems mini-project.

Usage:
    python page_replacement.py                       # built-in textbook example
    python page_replacement.py -r 7 0 1 2 0 3 0 4 -f 3
    python page_replacement.py -r 1 2 3 4 1 2 5 -f 3 --algo fifo optimal
"""
import argparse
from collections import deque

DEFAULT_REFS = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
DEFAULT_FRAMES = 3


def fifo(refs, n_frames):
    """Evict the page that has been in memory the longest."""
    frames, queue, steps, faults = [], deque(), [], 0
    for page in refs:
        fault = page not in frames
        if fault:
            faults += 1
            if len(frames) == n_frames:
                victim = queue.popleft()
                frames[frames.index(victim)] = page
            else:
                frames.append(page)
            queue.append(page)
        steps.append((page, list(frames), fault))
    return steps, faults


def optimal(refs, n_frames):
    """Evict the page whose next use is farthest in the future (Belady's)."""
    frames, steps, faults = [], [], 0
    for i, page in enumerate(refs):
        fault = page not in frames
        if fault:
            faults += 1
            if len(frames) == n_frames:
                future = refs[i + 1:]
                # Pages never used again get infinite distance -> evicted first.
                dist = {p: (future.index(p) if p in future else float("inf"))
                        for p in frames}
                victim = max(frames, key=lambda p: dist[p])
                frames[frames.index(victim)] = page
            else:
                frames.append(page)
        steps.append((page, list(frames), fault))
    return steps, faults


def lru(refs, n_frames):
    """Evict the page that was used least recently (bonus algorithm)."""
    frames, last_used, steps, faults = [], {}, [], 0
    for i, page in enumerate(refs):
        fault = page not in frames
        if fault:
            faults += 1
            if len(frames) == n_frames:
                victim = min(frames, key=lambda p: last_used[p])
                frames[frames.index(victim)] = page
            else:
                frames.append(page)
        last_used[page] = i
        steps.append((page, list(frames), fault))
    return steps, faults


ALGORITHMS = {"fifo": ("FIFO", fifo), "optimal": ("Optimal", optimal), "lru": ("LRU", lru)}


def print_table(name, steps, faults, n_frames):
    print(f"\n=== {name} ({n_frames} frames) ===")
    print(f"{'Step':<5}{'Page':<6}" + "".join(f"F{i+1:<4}" for i in range(n_frames)) + "Result")
    for i, (page, frames, fault) in enumerate(steps, 1):
        cells = "".join(f"{(str(frames[j]) if j < len(frames) else '-'):<5}" for j in range(n_frames))
        print(f"{i:<5}{page:<6}{cells}{'FAULT' if fault else 'hit'}")
    total = len(steps)
    print(f"Page faults: {faults} | Hits: {total - faults} | "
          f"Fault rate: {faults / total:.1%} | Hit ratio: {(total - faults) / total:.1%}")


def main():
    ap = argparse.ArgumentParser(description="Page replacement simulator")
    ap.add_argument("-r", "--refs", type=int, nargs="+", default=DEFAULT_REFS,
                    help="page reference string")
    ap.add_argument("-f", "--frames", type=int, default=DEFAULT_FRAMES,
                    help="number of frames")
    ap.add_argument("--algo", nargs="+", choices=ALGORITHMS, default=list(ALGORITHMS),
                    help="algorithms to run (default: all)")
    args = ap.parse_args()
    if args.frames < 1:
        ap.error("--frames must be at least 1")

    print(f"Reference string: {' '.join(map(str, args.refs))}")
    results = {}
    for key in args.algo:
        name, fn = ALGORITHMS[key]
        steps, faults = fn(args.refs, args.frames)
        print_table(name, steps, faults, args.frames)
        results[name] = faults

    print("\n=== Comparison ===")
    for name, faults in sorted(results.items(), key=lambda kv: kv[1]):
        print(f"{name:<8} {faults} faults")


if __name__ == "__main__":
    main()
