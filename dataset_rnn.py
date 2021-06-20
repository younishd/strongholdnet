#!/usr/bin/env python

import sys
import random
from anytree import Node, RenderTree, Walker, LevelOrderIter
from anytree.search import find_by_attr, findall_by_attr


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


def dump_good_dataset(root: Node, stronghold: int):
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
    entry = random.choice([i+1 for i, r in enumerate(random_start.children) if r.name != 'None'])
    for room in upwards:
        X.append((
                room.name,
                entry,
                room.orientation,
                room.parent.name,
                room.exit,
                *([c.name for c in room.children] + ['None'] * (5 - len(room.children)))))
        y.append(0)
        entry = room.exit
    X.append((
            common.name,
            entry,
            common.orientation,
            common.parent.name,
            common.exit,
            *([c.name for c in common.children] + ['None'] * (5 - len(common.children)))))
    for room in downwards:
        X.append((room.name, 0, room.orientation, room.parent.name, room.exit, *([c.name for c in room.children] + ['None'] * (5 - len(room.children)))))
        y.append(room.exit)
    X = X[:-1]
    list(map(lambda x: print(stronghold, *x[0], x[1]), zip(X, y)))
    
def dump_bad_dataset(root: Node, stronghold: int):
    X = []
    y = []
    stupid_rooms = ['Start', 'SmallCorridor', 'Library', 'PortalRoom', 'None']
    portal = find_by_attr(root, 'PortalRoom')
    library = findall_by_attr(root, 'Library')
    if len(library) == 0:
        return
    library = random.choice(library)
    random_start = random.choice([
            node for node in LevelOrderIter(
                root,
                maxlevel=3,
                filter_=lambda x: x.name not in stupid_rooms and len([c for c in x.children if c.name not in stupid_rooms]) > 0)])
    (upwards, common, downwards) = Walker().walk(random_start, library)
    for room in upwards:
        X.append((
                room.name,
                0,
                room.orientation,
                room.parent.name,
                room.exit,
                *([c.name for c in room.children] + ['None'] * (5 - len(room.children)))))
        (upwards_portal, common_portal, downwards_portal) = Walker().walk(room, portal)
        if len(upwards_portal) > 0:
            label = 0
        elif len(downwards_portal) > 0:
            label = downwards_portal[0].exit
        else:
            raise ValueError
        y.append(label)
    X.append((
            common.name,
            0,
            common.orientation,
            common.parent.name,
            common.exit,
            *([c.name for c in common.children] + ['None'] * (5 - len(common.children)))))
    (upwards_portal, common_portal, downwards_portal) = Walker().walk(common, portal)
    if len(upwards_portal) > 0:
        label = 0
    elif len(downwards_portal) > 0:
        label = downwards_portal[0].exit
    else:
        raise ValueError
    y.append(label)
    for room in downwards:
        X.append((
                room.name,
                1,
                room.orientation,
                room.parent.name,
                room.exit,
                *([c.name for c in room.children] + ['None'] * (5 - len(room.children)))))
        (upwards_portal, common_portal, downwards_portal) = Walker().walk(room, portal)
        if len(upwards_portal) > 0:
            label = 0
        elif len(downwards_portal) > 0:
            label = downwards_portal[0].exit
        else:
            raise ValueError
        y.append(label)
    list(map(lambda x: print(stronghold, *x[0], x[1]), zip(X, y)))
    
    
def dump_ugly_dataset(root: Node, stronghold: int):
    X = []
    y = []
    stupid_rooms = ['Start', 'SmallCorridor', 'Library', 'PortalRoom', 'None']
    portal = find_by_attr(root, 'PortalRoom')
    random_start = random.choice([
            node for node in LevelOrderIter(
                root,
                maxlevel=3,
                filter_=lambda x: x.name not in stupid_rooms and len([c for c in x.children if c.name not in stupid_rooms]) > 0)])
    room = random_start
    for i in range(50):
        next_exit = random.choice([0] if room.parent.name not in stupid_rooms else [] + [j+1 for j, r in enumerate(room.children) if r.name not in stupid_rooms])
        next_room = ([room.parent, *room.children])[next_exit]
        X.append((
                next_room.name,
                0 if next_exit == 0 else 1,
                next_room.orientation,
                next_room.parent.name,
                next_room.exit,
                *([c.name for c in next_room.children] + ['None'] * (5 - len(next_room.children)))))
        (upwards_portal, common_portal, downwards_portal) = Walker().walk(next_room, portal)
        if len(upwards_portal) > 0:
            label = 0
        elif len(downwards_portal) > 0:
            label = downwards_portal[0].exit
        else:
            raise ValueError
        y.append(label)
        room = next_room
    list(map(lambda x: print(stronghold, *x[0], x[1]), zip(X, y)))


def print_stronghold_tree(root: Node):
    for pre, _, node in RenderTree(root):
        print("{}{}".format(pre, node.name))


def main():
    stronghold_file = sys.argv[1] if len(sys.argv) > 1 else '100k_strongholds.txt'
    random.seed(1337)

    print("stronghold room entry orientation parent_room parent_exit child_room_1 child_room_2 child_room_3 child_room_4 child_room_5 exit")
    stronghold = 0
    for root in parse_tree_generator(stronghold_file):
        dump_good_dataset(root, stronghold)
        stronghold += 1
        #dump_bad_dataset(root, stronghold)
        #stronghold += 1
        #dump_ugly_dataset(root, stronghold)
        #stronghold += 1


if __name__ == '__main__':
    main()
