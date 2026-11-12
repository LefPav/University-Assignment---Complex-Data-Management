#PAVLIDIS ELEFTHERIOS AM:5332
#ZOTOS SOTIRIOS AM:5227

import sys
import re
import math

class RTreeSearcher:

    def __init__(self):
        self.nodes = {}
        self.root_id = None

    def load_tree(self, rtree_file):
        with open(rtree_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(' , ')
                node_id = int(parts[0])
                leaf_flag = int(parts[2])

                entries = []
                i = 0
                while i < len(line):
                    start = line.find('(', i)
                    if start == -1:
                        break
                    depth = 0
                    for j in range(start, len(line)):
                        if line[j] == '(':
                            depth += 1
                        elif line[j] == ')':
                            depth -= 1
                            if depth == 0:
                                token = line[start+1:j]
                                comma = token.index(',')
                                ptr_id = int(token[:comma].strip())
                                geo_str = token[comma+1:].strip().strip('[]() ')
                                coords = [float(x.strip()) for x in geo_str.split(',')]
                                entries.append((ptr_id, coords))
                                i = j + 1
                                break
                    else:
                        break

                self.nodes[node_id] = {'flag': leaf_flag, 'entries': entries}

        self.root_id = node_id

    def point_distance(self, p1, p2):                                           # Υπολογίζουμε την Ευκλείδεια απόσταση μεταξύ δύο σημείων
        return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

    def min_distance(self, point, mbr): 
        # Υπολογίζει την ελάχιστη απόσταση σημείου από MBR
        dx = max(mbr[0] - point[0], 0, point[0] - mbr[2])
        dy = max(mbr[1] - point[1], 0, point[1] - mbr[3])
        return math.sqrt(dx*dx + dy*dy) 

    # Distance Range Query
    def distance_range_query(self, node_id, center, r, results):
        node = self.nodes[node_id]
        if node['flag'] == 0:
            for rid, pt in node['entries']:
                if self.point_distance(center, pt) <= r:                        # απλό check απόστασης για τα σημεία 
                    results.append(rid)
        else:
            # κατεβαίνουμε αναδρομικά μόνο όπου υπάρχει πιθανότητα overlap
            for cid, mbr in node['entries']:
                if self.min_distance(center, mbr) <= r:
                    self.distance_range_query(cid, center, r, results)

def main():
    if len(sys.argv) < 3:
        print(f"Usage: python {sys.argv[0]} <rtree_file> <queries_file>")
        sys.exit(1)
    
    search = RTreeSearcher()
    search.load_tree(sys.argv[1])
    
    infile = open(sys.argv[2], 'r')
    for i, line in enumerate(infile):
        parts = [float(x) for x in line.replace('[','').replace(']','').split()]
        if not parts: 
            continue
        center, r = parts[:2], parts[2]
        results = []
        search.distance_range_query(search.root_id, center, r, results)
        print(f"{i} ({len(results)}): {','.join(map(str, results))}")

if __name__ == "__main__":
    main()