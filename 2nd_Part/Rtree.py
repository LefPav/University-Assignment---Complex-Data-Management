#PAVLIDIS ELEFTHERIOS AM:5332
#ZOTOS SOTIRIOS AM:5227

import math
import sys

# όρια για  τα entries
MAX_LEAF = 51
MIN_LEAF = 20
MAX_INT = 28
MIN_INT = 11

class rTreeNode:
    def __init__(self, id, is_fyllo):
        self.id = id
        self.is_fyllo = is_fyllo
        self.entries = []
        self.mbr = None

# υπολογίζει το MBR είτε από σημεία είτε από ήδη υπάρχοντα MBRs
def calculate_mbr(items):
    if not items:
        return None

    if len(items[0]) == 2:
        is_point_list = True
    else:
        is_point_list = False

    if is_point_list:
        xs = [p[0] for p in items]
        ys = [p[1] for p in items]
    else:
        xs = [b[0] for b in items] + [b[2] for b in items]
        ys = [b[1] for b in items] + [b[3] for b in items]

    return [min(xs), min(ys), max(xs), max(ys),]

# μικρό fix για να μην έχουμε underflow στο τελευταίο node, λίγο hacky αλλά δουλεύει 
def update_komvon(nodes, min_capacity):
    if len(nodes) > 1 and len(nodes[-1].entries) < min_capacity:
        needed = min_capacity - len(nodes[-1].entries)

        nodes[-1].entries = nodes[-2].entries[-needed:] + nodes[-1].entries
        nodes[-2].entries = nodes[-2].entries[:-needed]

    return nodes

# φτιάχνει κομβους (είτε leaf είτε internal) 
def packing_komvon(objects, is_fyllo, counter_komvon):
    max_entries = MAX_LEAF     if is_fyllo else MAX_INT
    min_entries = MIN_LEAF     if is_fyllo else MIN_INT

    nodes = []

    # Αν είναι φύλλο κάνουμε διαχωρισμό σε κάθετη και οριζόντια κατεύθυνση για καλύτερη κατανομή
    if is_fyllo:
        total_objects = len(objects)
        num_nodes  = math.ceil(total_objects / max_entries)
        num_slices = math.ceil(math.sqrt(num_nodes))
        slice_size = num_slices * max_entries

        # sort by x
        objects.sort(key=lambda obj: obj[1][0])
        
        for i in range(0, total_objects, slice_size):
            vertical_slice = objects[i : i + slice_size]

            # μετά sort by y
            vertical_slice.sort(key=lambda obj: obj[1][1])

            for j in range(0, len(vertical_slice), max_entries):
                node_entries = vertical_slice[j : j + max_entries]
                node = rTreeNode(0, is_fyllo=True)
                node.entries = node_entries
                nodes.append(node)

    else: 
        # απλό grouping
        for i in range(0, len(objects), max_entries):
            node_entries = objects[i : i + max_entries]
            node = rTreeNode(0, is_fyllo=False)
            node.entries = node_entries
            nodes.append(node)

        nodes = update_komvon(nodes, min_entries)
    
    # assign ids + mbr
    for n in nodes:
        n.id  = counter_komvon[0]
        counter_komvon[0] += 1
        n.mbr = calculate_mbr(
            [obj[1] for obj in n.entries]
        )

    return nodes

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <input_file> <output_file>")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]


    points = []
    with open(input_file, 'r') as file:
        lines = file.readlines()
 
        for i, line in enumerate(lines[1:], 1):
            parts = line.split()
            if parts:
                x, y = float(parts[0]), float(parts[1])
                points.append((i, [x, y]))

    levels = []
    counter_komvon = [0] 

    # Δημιουργεί το πρώτο επίπεδο 
    current_level = packing_komvon(points, True, counter_komvon)
    levels.append(current_level)

    # Δημιουργεί τα επόμενα επίπεδα μέχρι να φτάσουμε στην ρίζα
    while len(levels[-1]) > 1:
        prev_level = levels[-1]
 
        next_input = [(n.id, n.mbr) for n in prev_level]
        
        new_nodes = packing_komvon(next_input, False, counter_komvon)
        levels.append(new_nodes)
    
    # stats για κάθε επίπεδο
    for i, level in enumerate(levels):
 
        if i > 0:
            total_area = sum((n.mbr[2] - n.mbr[0]) * (n.mbr[3] - n.mbr[1]) for n in level) # Υπολογίζει το άθροισμα των εμβαδών των MBRs στο επίπεδο
            avg_area = total_area / len(level)                                             # Υπολογίζει τον μέσο όρο του εμβαδού των MBRs στο επίπεδο
        else:
            avg_area = 0.0 
            
        print(f"{len(level)} nodes at level {i} with average MBR Area: {avg_area}")


    with open(output_file, 'w') as newfile: 
        for level in levels:
            for node in level:
            
                flag = 0 if node.is_fyllo else 1
       
                header = f"{node.id} , {len(node.entries)} , {flag}" 
       
                entry_strings = []
                for ptr, geo in node.entries:
                    if node.is_fyllo:   # Για φύλλα τα γεωγραφικά δεδομένα είναι σημεία 
                        entry_strings.append(f"({ptr},({geo[0]}, {geo[1]}))") 
                    else:               # Για εσωτερικούς κόμβους τα γεωγραφικά δεδομένα είναι MBRs οπότε τα μορφοποιούμε ανάλογα
                        entry_strings.append(f"({ptr},[{geo[0]}, {geo[1]}, {geo[2]}, {geo[3]}])")
                
                newfile.write(f"{header} , {' , '.join(entry_strings)}\n")

if __name__ == "__main__":
    main()