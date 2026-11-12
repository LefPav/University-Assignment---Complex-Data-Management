#PAVLIDIS ELEFTHERIOS AM:5332
#ZOTOS SOTIRIOS AM:5227

import sys
import re

class rTreeSearch:

    def __init__(self):
        self.nodes   = {}
        self.root_id = None

    # λίγο manual parsing γιατί το format μας δυσκολεψε 
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

        
    def overlaps(self, bounding_box, window):       # Ελέγουμε αν το bounding box ενός κόμβου επικαλύπτεται απο το παράθυρο αναζήτησης
        if bounding_box[2] < window[0] or bounding_box[0] > window[2] or bounding_box[3] < window[1] or bounding_box[1] > window[3]:
            return False
        else:
            return True
        

    def is_inside(self, point, window):             # Ελέγουμε αν ένα σημείο βρίσκεται μέσα στο παράθυρο αναζήτησης
        if window[0] <= point[0] <= window[2] and window[1] <= point[1] <= window[3]:
            return True
        else:
            return False

    def window_range_query(self, node_id, window):  
        cur_node = self.nodes[node_id]
        results = []

        if cur_node['flag'] == 0:                   # αν είναι φύλλο ελέγχουμε τα σημεία του
            for record_id, point in cur_node['entries']: 
                if self.is_inside(point, window):
                    results.append(record_id)
        else:                                       # αν είναι εσωτερικός κόμβος ελέγχουμε τα bounding boxes των παιδιών 
            for child_id, bounding_box in cur_node['entries']:
                if self.overlaps(bounding_box, window):
                    results.extend(self.window_range_query(child_id, window)) # recursive search στα children

        return results


def main():
    if len(sys.argv) < 3:
        print(f"Usage: python {sys.argv[0]} rtree.csv windowRangeQueries.txt")
        sys.exit(1)

    search = rTreeSearch()
    search.load_tree(sys.argv[1])

    with open(sys.argv[2], 'r') as file:
        for query_index, line in enumerate(file):
            line = line.strip()
            if not line:
                continue
            window  = [float(value) for value in line.split()]
            results = search.window_range_query(search.root_id, window)
            print(f"{query_index} ({len(results)}): {','.join(map(str, results))}")


if __name__ == "__main__":
    main()