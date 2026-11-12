#PAVLIDIS ELEFTHERIOS AM:5332
#ZOTOS SOTIRIOS AM:5227

import sys
import re
import math
import heapq

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

    def point_distance(self, p1, p2):
        # Υπολογίζει την Ευκλείδεια απόσταση μεταξύ δύο σημείων
        return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

    def min_distance(self, point, mbr):
        # Υπολογίζει την ελάχιστη απόσταση σημείου από MBR
        dx = max(mbr[0] - point[0], 0, point[0] - mbr[2])
        dy = max(mbr[1] - point[1], 0, point[1] - mbr[3])
        return math.sqrt(dx*dx + dy*dy)

    def knn_query(self, center, k):
        # χρησιμοποιούμε priority queue για να βρίσκουμε κάθε φορά τον πιο κοντινό 
        # Το type σιγουρεύει ότι σε ισοπαλία αποστάσεων βγαίνουν πρώτα τα σημεία
        results = []
        pq = []

        # αρχικοποιούμε το heap με τα entries της ρίζας
        root = self.nodes[self.root_id]
        if root['flag'] == 0:  # η ρίζα είναι φύλλο
            for rid, pt in root['entries']:
                d = self.point_distance(center, pt)
                heapq.heappush(pq, (d, 1, rid))
        else:  # η ρίζα είναι ενδιάμεσος
            for cid, mbr in root['entries']:
                d = self.min_distance(center, mbr)
                heapq.heappush(pq, (d, 0, cid))

        while pq and len(results) < k: # παίρνουμε το πιο κοντινό στοιχείο μέχρι στιγμής
            dist, entry_type, entry_id = heapq.heappop(pq)

            if entry_type == 1:  # σημείο: είναι ο επόμενος πλησιέστερος γείτονας
                results.append(entry_id)
            else:  # κόμβος: επέκταση
                node = self.nodes[entry_id]
                if node['flag'] == 0:  # φύλλο: βάλε τα σημεία στο heap
                    for rid, pt in node['entries']:
                        d = self.point_distance(center, pt)
                        heapq.heappush(pq, (d, 1, rid))
                else:  # ενδιάμεσος: βάλε τα MBR στο heap
                    for cid, mbr in node['entries']:
                        d = self.min_distance(center, mbr)
                        heapq.heappush(pq, (d, 0, cid))

        return results


def main():
    if len(sys.argv) < 4:
        print(f"Usage: python {sys.argv[0]} rtree.csv NNQueries.txt k")
        sys.exit(1)

    searcher = RTreeSearcher()
    searcher.load_tree(sys.argv[1])
    k_val = int(sys.argv[3])

    with open(sys.argv[2], 'r') as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line: continue
            center = [float(x) for x in line.split()]
            results = searcher.knn_query(center, k=k_val)
            print(f"{i}: {','.join(map(str, results))}")


if __name__ == "__main__":
    main()