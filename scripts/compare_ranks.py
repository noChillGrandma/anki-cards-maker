#!/usr/bin/env python3
import re
import argparse

def parse_list(path):
    """Read a rank list and return a dict phrase→rank."""
    d = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            m = re.match(r'(\d+):\s*(.+)', line.strip())
            if m:
                d[m.group(2).strip()] = int(m.group(1))
    return d

def compare(prev_path, curr_path, out_path=None):
    """Compare two rank lists and print each item’s position change."""
    prev = parse_list(prev_path)
    out = open(out_path, 'w', encoding='utf-8') if out_path else None

    with open(curr_path, 'r', encoding='utf-8') as f:
        for line in f:
            m = re.match(r'(\d+):\s*(.+)', line.strip())
            if not m: continue
            rank = int(m.group(1))
            phrase = m.group(2).strip()
            old = prev.get(phrase)
            if old is None:
                sign = 'new'
            else:
                delta = old - rank
                sign = f'+{delta}' if delta>0 else (f'-{abs(delta)}' if delta<0 else '-')
            out_line = f'{rank:04d}: [ {sign} ] {phrase}'
            (out.write(out_line + '\n') if out else print(out_line))

    if out: out.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Compare two ranked lists and show up/down moves')
    parser.add_argument('previous', help='old rank list file')
    parser.add_argument('current',  help='new rank list file')
    parser.add_argument('-o','--output', help='save results to file')
    args = parser.parse_args()
    compare(args.previous, args.current, args.output)
