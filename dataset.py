#!/usr/bin/env python

import sys
from anytree import Node, RenderTree, Walker
from anytree.search import find_by_attr


def parse_tree_generator(file):
    def create_node(i: int, j: int):
        nonlocal stronghold
        if i < 0:
            return Node("None")
        return Node(stronghold[i][0], exit=j, children=[create_node(int(i), j+1) for j, i in enumerate(stronghold[i][1:])])
    with open(file, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            while 'START' not in line:
                pass
            f.readline()
            stronghold = []
            while 'END' not in line:
                line = f.readline()
                if not line:
                    break
                stronghold.append(line.rstrip('\n').split(' '))
            for k, v in enumerate(stronghold):
                if v[0] == 'Start':
                    root = create_node(k, 1)
                    break
            yield root


def print_stronghold_tree(root: Node):
    for pre, _, node in RenderTree(root):
        print("{}{}".format(pre, node.name))


def dump_dataset(root: Node):
    X = []
    y = []
    w = Walker()
    portal = find_by_attr(root, 'PortalRoom')
    (upwards, common, downwards) = w.walk(root, portal)
    for depth, room in enumerate(downwards):
        if room.name not in ['FiveWayCrossing', 'Corridor', 'SquareRoom']:
            continue
        if len([ c for c in room.children if c.name != 'None' ]) < 2:
            continue
        X.append((depth, room.parent.name, room.exit, room.name, *([child.name for child in room.children] + ['None'] * (5 - len(room.children)))))
        y.append(room.exit)
    X = X[:-1]
    y = y[1:]
    for v in zip(X, y):
        print(*v[0], v[1])
    return X, y


def main():
    print("depth prev_room prev_exit room exit_1 exit_2 exit_3 exit_4 exit_5 exit_portal")

    stronghold_file = sys.argv[1] if len(sys.argv) > 1 else '100k_strongholds.txt'

    for root in parse_tree_generator(stronghold_file):
        dump_dataset(root)


if __name__ == '__main__':
    main()
