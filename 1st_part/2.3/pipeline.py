def pipelined_merge_join(r, s, t):
    # Εσωτερικός generator για το πρώτο join (r, s)
    def join_rs(r_list, s_list):
        i, j = 0, 0
        while i < len(r_list) and j < len(s_list):
            r_id = r_list[i][0]
            s_id = s_list[j][0]
            
            if r_id == s_id:
                # Βρήκαμε match, ελέγχουμε όλες τις συνδυαστικές πλειάδες
                # για την περίπτωση που έχουμε πολλαπλά ίδια IDs
                temp_j = j
                while temp_j < len(s_list) and s_list[temp_j][0] == r_id:
                    # Yield αντί για list.append για pipelining
                    yield (r_list[i][0], r_list[i][1], s_list[temp_j][1])
                    temp_j += 1
                i += 1
            elif r_id < s_id:
                i += 1
            else:
                j += 1

    # Κυρίως join του ενδιάμεσου αποτελέσματος με την t
    results = []
    rs_generator = join_rs(r, s) # Αυτό δεν αποθηκεύει λίστα, είναι iterator
    
    t_idx = 0
    # Καταναλώνουμε τον generator έναν-έναν
    for rs_tuple in rs_generator:
        rs_id = rs_tuple[0]
        
        # Επειδή η t είναι ταξινομημένη, προχωράμε τον δείκτη της
        while t_idx < len(t) and t[t_idx][0] < rs_id:
            t_idx += 1
            
        # Έλεγχος για match με την t
        temp_t = t_idx
        while temp_t < len(t) and t[temp_t][0] == rs_id:
            results.append((rs_tuple[0], rs_tuple[1], rs_tuple[2], t[temp_t][1]))
            temp_t += 1
            
    return results

def three_way_sort_merge_join(r, s, t):
    i, j, k = 0, 0, 0
    results = []
    
    while i < len(r) and j < len(s) and k < len(t):
        r_id = r[i][0]
        s_id = s[j][0]
        t_id = t[k][0]
        
        # Αν και τα τρία IDs είναι ίσα, έχουμε match
        if r_id == s_id == t_id:
            # Βρίσκουμε όλα τα s και t που έχουν αυτό το ID για να κάνουμε το καρτεσιανό γινόμενο
            # μόνο για το συγκεκριμένο ID
            curr_s = j
            while curr_s < len(s) and s[curr_s][0] == r_id:
                curr_t = k
                while curr_t < len(t) and t[curr_t][0] == r_id:
                    results.append((r_id, r[i][1], s[curr_s][1], t[curr_t][1]))
                    curr_t += 1
                curr_s += 1
            i += 1 # Προχωράμε στο επόμενο r
        else:
            # Αν δεν είναι ίσα, προχωράμε τον δείκτη που έχει το μικρότερο ID
            max_id = max(r_id, s_id, t_id)
            if r_id < max_id: i += 1
            if s_id < max_id: j += 1
            if t_id < max_id: k += 1
            
    return results

r = [(1, 'b1'), (2, 'b2'), (3, 'b3'), (4, 'b4')]
s = [(1, 'c1'), (1, 'c2'), (2, 'c3'), (3, 'c4')]
t = [(1, 'd1'), (2, 'd2'), (3, 'd3'), (5, 'd4')]

print("Pipelined Result:")
print(pipelined_merge_join(r, s, t))

print("\nThree-way Result:")
print(three_way_sort_merge_join(r, s, t))