#!/usr/bin/env python

import sys
import random
from anytree import Node, RenderTree, Walker, LevelOrderIter
from anytree.search import find_by_attr


def parse_tree_generator(file):
    def create_node(i: int, j: int):
        nonlocal stronghold
        if i < 0:
            return Node('None')
        return Node(
                stronghold[i][0],
                exit=j,
                orientation=stronghold[i][1],
                children=[create_node(int(i), j+1) for j, i in enumerate(stronghold[i][2:])])
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
                    root = create_node(k, 0)
                    break
            yield root


def dump_dataset(root: Node):
    X = []
    y = []
    stupid_rooms = ['Start', 'SmallCorridor', 'Library', 'PortalRoom', 'None']
    portal = find_by_attr(root, 'PortalRoom')
    random_start = random.choice([
            node for node in LevelOrderIter(
                root,
                maxlevel=6,
                filter_=lambda x: x.name not in stupid_rooms and len([c for c in x.children if c.name not in stupid_rooms]) > 0)])
    (upwards, common, downwards) = Walker().walk(random_start, portal)
    for room in upwards:
        X.append((room.name, room.orientation, room.parent.name, room.exit, *([c.name for c in room.children] + ['None'] * (5 - len(room.children)))))
        y.append(0)
    X.append((common.name, common.orientation, common.parent.name, common.exit, *([c.name for c in common.children] + ['None'] * (5 - len(common.children)))))
    for room in downwards:
        X.append((room.name, room.orientation, room.parent.name, room.exit, *([c.name for c in room.children] + ['None'] * (5 - len(room.children)))))
        y.append(room.exit)
    X = X[:-1]
    list(map(lambda x: print(*x[0], x[1]), zip(X, y)))


def print_stronghold_tree(root: Node):
    for pre, _, node in RenderTree(root):
        print("{}{}".format(pre, node.name))


def main():
    stronghold_file = sys.argv[1] if len(sys.argv) > 1 else '1m_strongholds.txt'
    random.seed(1337)

    print("room orientation parent_room parent_exit child_room_1 child_room_2 child_room_3 child_room_4 child_room_5 exit")
    list(map(dump_dataset, parse_tree_generator(stronghold_file)))


if __name__ == '__main__':
    main()
