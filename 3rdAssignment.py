#PAVLIDIS ELEFTHERIOS - 5332
#SOTIRIOS ZOTOS - 5227
# ENTOLES EKTELESIS: 
# python3 meros1.py part1 data10K10.txt
# python3 meros1.py part2 data10K10.txt
# python3 meros1.py part3 data10K10.txt queries10.txt
# python3 meros1.py part4 data10K10.txt queries10.txt
# python3 meros1.py part5 data10K10.txt queries10.txt
import heapq
import sys
import math
import bisect

def read(filename):
    D = []

    with open(filename, "r") as f:
        for point_id, line in enumerate(f):
            coords = [float(x) for x in line.split()]
            D.append((point_id, coords))

    return D


def euclidean_distance(p1, p2):
    total = 0

    for x1, x2 in zip(p1, p2):
        total += (x1 - x2) ** 2

    return math.sqrt(total)


def find_refs(D, num_refs):
    refs = []

    first_point_id, first_point = D[0]

    max_distance = -1
    first_ref = None

    for point_id, point in D:
        if point_id == first_point_id:
            continue

        d = euclidean_distance(first_point, point)

        if d > max_distance:
            max_distance = d
            first_ref = (point_id, point)

    refs.append(first_ref)

    while len(refs) < num_refs:
        best_point = None
        best_sum = -1

        for point_id, point in D:
            already_ref = False

            for ref_id, ref_point in refs:
                if point_id == ref_id:
                    already_ref = True
                    break

            if already_ref:
                continue

            total_distance = 0

            for ref_id, ref_point in refs:
                total_distance += euclidean_distance(point, ref_point)

            if total_distance > best_sum:
                best_sum = total_distance
                best_point = (point_id, point)

        refs.append(best_point)

    ref_ids = []

    for ref_id, ref_point in refs:
        ref_ids.append(ref_id)

    distances = []

    for point_id, point in D:
        row = []

        for ref_id, ref_point in refs:
            d = euclidean_distance(point, ref_point)
            row.append(d)

        distances.append(row)

    return ref_ids, distances


def compute_idistance_array(D, ref_ids, distances):
    nearest_pivots = []
    nearest_distances = []

    maxd_per_pivot = [0] * len(ref_ids)

    for point_id, point in D:
        nearest_pivot = 0
        nearest_distance = distances[point_id][0]

        for j in range(1, len(ref_ids)):
            if distances[point_id][j] < nearest_distance:
                nearest_distance = distances[point_id][j]
                nearest_pivot = j

        nearest_pivots.append(nearest_pivot)
        nearest_distances.append(nearest_distance)

        if nearest_distance > maxd_per_pivot[nearest_pivot]:
            maxd_per_pivot[nearest_pivot] = nearest_distance

    maxd = max(maxd_per_pivot)

    idistance_array = []

    for point_id, point in D:
        pivot_index = nearest_pivots[point_id]
        d = nearest_distances[point_id]

        idistance_value = pivot_index * maxd + d

        # κρατάμε και το pivot_index
        idistance_array.append((idistance_value, point_id, pivot_index))

    idistance_array.sort()

    return idistance_array, maxd_per_pivot, maxd

def naive_search(D, query, r):
    results = []
    distance_computations = 0

    for point_id, point in D:
        d = euclidean_distance(query, point)
        distance_computations += 1

        if d <= r:
            results.append(point_id)

    return results, distance_computations

def get_refs_from_ids(D, ref_ids):
    refs = []

    for ref_id in ref_ids:
        refs.append(D[ref_id])

    return refs

def pivot_based_search(D, refs, distances, query, r):
    results = []
    
    # Ξεκινάμε από το len(refs) γιατί υπολογίζουμε την απόσταση 
    # του query από όλα τα pivots στην αρχή!
    distance_computations = len(refs) 

    query_to_refs = []
    # Φτιάχνουμε ένα mapping από ref_id στο index του για γρήγορο look-up
    ref_id_to_idx = {}

    for idx, (ref_id, ref_point) in enumerate(refs):
        d = euclidean_distance(query, ref_point)
        query_to_refs.append(d)
        ref_id_to_idx[ref_id] = idx

    for point_id, point in D:
        # Αν το σημείο είναι το ίδιο το pivot, ξέρουμε ήδη την απόστασή του 
        # από το query (είναι αποθηκευμένη στο query_to_refs)
        if point_id in ref_id_to_idx:
            pivot_idx = ref_id_to_idx[point_id]
            d = query_to_refs[pivot_idx]
            if d <= r:
                results.append(point_id)
            continue # Δεν χρειάζεται pruning ή extra computation

        candidate = True
        for j in range(len(refs)):
            if abs(distances[point_id][j] - query_to_refs[j]) > r:
                candidate = False
                break

        if candidate:
            d = euclidean_distance(query, point)
            distance_computations += 1

            if d <= r:
                results.append(point_id)

    return results, distance_computations

def idistance_search(D, refs, distances, idistance_array, maxd_per_pivot, maxd, query, r):
    results = []
    candidates = set()
    distance_computations = len(refs)

    # Απομονώνουμε τα κλειδιά για το binary search
    keys = [entry[0] for entry in idistance_array]

    # 1. Υπολογισμός αποστάσεων του query από όλα τα pivots
    query_to_refs = []
    for ref_id, ref_point in refs:
        d = euclidean_distance(query, ref_point)
        query_to_refs.append(d)

    # 2. Έλεγχος για κάθε pivot (partition) ξεχωριστά
    for j in range(len(refs)):
        query_to_ref = query_to_refs[j]

        # Καθορισμός του δακτυλίου (Bnd(q, r)) που τέμνει το partition j
        left_distance = query_to_ref - r
        right_distance = query_to_ref + r

        # Αν ο δακτύλιος δεν τέμνει καθόλου τη σφαίρα επιρροής του pivot, προσπέρνα το
        if left_distance > maxd_per_pivot[j] or right_distance < 0:
            continue

        # Περιορισμός των αποστάσεων στα όρια του partition j
        left_distance = max(left_distance, 0.0)
        right_distance = min(right_distance, maxd_per_pivot[j])

        # Μετατροπή σε iDistance τιμές
        left_bound = j * maxd + left_distance
        right_bound = j * maxd + right_distance

        # Δυαδική αναζήτηση στον ταξινομημένο πίνακα
        start = bisect.bisect_left(keys, left_bound)
        end = bisect.bisect_right(keys, right_bound)

        # Σάρωση των στοιχείων που βρέθηκαν στο εύρος
        for k in range(start, end):
            idistance_value, point_id, pivot_index = idistance_array[k]
            
            # Διασφάλιση ότι το σημείο ανήκει όντως στο pivot j (αποφυγή overlap)
            if pivot_index == j:
                candidates.add(point_id)

    # 3. Επαλήθευση των υποψηφίων (Refinement step)
    for point_id in candidates:
        point = D[point_id][1]
        d = euclidean_distance(query, point)
        distance_computations += 1

        if d <= r:
            results.append(point_id)

    return results, distance_computations

def part1(data_file, num_refs=5):
    D = read(data_file)
    ref_ids, distances = find_refs(D, num_refs)
    print(f"pivots: {ref_ids}")


def part2(data_file, num_refs=5):
    D = read(data_file)
    ref_ids, distances = find_refs(D, num_refs)
    idistance_array, maxd_per_pivot, maxd = compute_idistance_array(D, ref_ids, distances)

    print("maxd_per_pivot:", maxd_per_pivot)
    print("maxd:", maxd)
    print("first 10 iDistance entries:")

    for entry in idistance_array[:10]:
        print(entry)

def part3(data_file, query_file, num_refs=10, r=0.2):
    import time
    D = read(data_file)
    Q = read(query_file)

    ref_ids, distances = find_refs(D, num_refs)
    refs = get_refs_from_ids(D, ref_ids)

    idistance_array, maxd_per_pivot, maxd = compute_idistance_array(
        D, ref_ids, distances
    )

    total_naive = 0
    total_pivot = 0
    total_idistance = 0

    t0 = time.time()
    for query_id, query in Q:
        _, c = naive_search(D, query, r)
        total_naive += c
    time_naive = time.time() - t0

    t0 = time.time()
    for query_id, query in Q:
        _, c = pivot_based_search(D, refs, distances, query, r)
        total_pivot += c
    time_pivot = time.time() - t0

    t0 = time.time()
    for query_id, query in Q:
        _, c = idistance_search(D, refs, distances, idistance_array, maxd_per_pivot, maxd, query, r)
        total_idistance += c
    time_idistance = time.time() - t0

    print("average distance comp per query (Naive) =", total_naive / len(Q))
    print("average distance comp per query (Pivot-based) =", total_pivot / len(Q))
    print("average distance comp per query (iDistance) =", total_idistance / len(Q))
    print("total time Naive =", time_naive)
    print("total time Pivot-based =", time_pivot)
    print("total time iDistance =", time_idistance)


def naive_knn(D, query, k):
    heap = []
    distance_computations = 0

    for point_id, point in D:
        d = euclidean_distance(query, point)
        distance_computations += 1

        if len(heap) < k:
            heapq.heappush(heap, (-d, point_id))
        elif d < -heap[0][0]:
            heapq.heapreplace(heap, (-d, point_id))

    results = [(pid, -neg_d) for neg_d, pid in heap]
    return results, distance_computations


def pivot_based_knn(D, refs, distances, query, k):
    heap = []
    distance_computations = len(refs)

    query_to_refs = []
    ref_id_to_idx = {}

    for idx, (ref_id, ref_point) in enumerate(refs):
        d = euclidean_distance(query, ref_point)
        query_to_refs.append(d)
        ref_id_to_idx[ref_id] = idx

    for point_id, point in D:
        if point_id in ref_id_to_idx:
            d = query_to_refs[ref_id_to_idx[point_id]]
            if len(heap) < k:
                heapq.heappush(heap, (-d, point_id))
            elif d < -heap[0][0]:
                heapq.heapreplace(heap, (-d, point_id))
            continue

        if len(heap) == k:
            r = -heap[0][0]
            pruned = False
            for j in range(len(refs)):
                if abs(distances[point_id][j] - query_to_refs[j]) > r:
                    pruned = True
                    break
            if pruned:
                continue

        d = euclidean_distance(query, point)
        distance_computations += 1

        if len(heap) < k:
            heapq.heappush(heap, (-d, point_id))
        elif d < -heap[0][0]:
            heapq.heapreplace(heap, (-d, point_id))

    results = [(pid, -neg_d) for neg_d, pid in heap]
    return results, distance_computations


def idistance_knn(D, refs, distances, idistance_array, maxd_per_pivot, maxd, query, k):
    heap = []
    distance_computations = len(refs)

    keys = [entry[0] for entry in idistance_array]

    query_to_refs = []
    for ref_id, ref_point in refs:
        d = euclidean_distance(query, ref_point)
        query_to_refs.append(d)

    nearest_pivot = min(range(len(refs)), key=lambda j: query_to_refs[j])

    def scan_partition(j, use_pruning):
        nonlocal distance_computations
        if use_pruning and len(heap) == k:
            r = -heap[0][0]
            if query_to_refs[j] - r > maxd_per_pivot[j] or query_to_refs[j] + r < 0:
                return
            left_distance = max(query_to_refs[j] - r, 0.0)
            right_distance = min(query_to_refs[j] + r, maxd_per_pivot[j])
        else:
            left_distance = 0.0
            right_distance = maxd_per_pivot[j]

        left_bound = j * maxd + left_distance
        right_bound = j * maxd + right_distance

        start = bisect.bisect_left(keys, left_bound)
        end = bisect.bisect_right(keys, right_bound)

        for i in range(start, end):
            idist_val, point_id, pivot_index = idistance_array[i]
            if pivot_index != j:
                continue
            point = D[point_id][1]
            d = euclidean_distance(query, point)
            distance_computations += 1
            if len(heap) < k:
                heapq.heappush(heap, (-d, point_id))
            elif d < -heap[0][0]:
                heapq.heapreplace(heap, (-d, point_id))

    scan_partition(nearest_pivot, use_pruning=False)

    for j in range(len(refs)):
        if j == nearest_pivot:
            continue
        scan_partition(j, use_pruning=True)

    results = [(pid, -neg_d) for neg_d, pid in heap]
    return results, distance_computations


def part4(data_file, query_file, num_refs=10, k=5):
    import time
    D = read(data_file)
    Q = read(query_file)

    ref_ids, distances = find_refs(D, num_refs)
    refs = get_refs_from_ids(D, ref_ids)

    idistance_array, maxd_per_pivot, maxd = compute_idistance_array(
        D, ref_ids, distances
    )

    total_naive = 0
    total_pivot = 0
    total_idistance = 0

    t0 = time.time()
    for query_id, query in Q:
        _, c = naive_knn(D, query, k)
        total_naive += c
    time_naive = time.time() - t0

    t0 = time.time()
    for query_id, query in Q:
        _, c = pivot_based_knn(D, refs, distances, query, k)
        total_pivot += c
    time_pivot = time.time() - t0

    t0 = time.time()
    for query_id, query in Q:
        _, c = idistance_knn(D, refs, distances, idistance_array, maxd_per_pivot, maxd, query, k)
        total_idistance += c
    time_idistance = time.time() - t0

    print("average distance comp per query (Pivot-based kNN) =", total_pivot / len(Q))
    print("average distance comp per query (iDistance kNN) =", total_idistance / len(Q))
    print("total time Naive kNN =", time_naive)
    print("total time Pivot-based kNN =", time_pivot)
    print("total time iDistance kNN =", time_idistance)


def part5():
    import time

    D = read("data10K10.txt")
    Q = read("queries10.txt")

    num_refs = 10
    ref_ids, distances = find_refs(D, num_refs)
    refs = get_refs_from_ids(D, ref_ids)
    idistance_array, maxd_per_pivot, maxd = compute_idistance_array(D, ref_ids, distances)

    epsilons = [0.1, 0.2, 0.4, 0.8]
    ks = [1, 5, 10, 50, 100]

    print("=== RANGE QUERIES ===")
    print(f"{'epsilon':<10} {'Method':<15} {'Total Time':>12} {'Avg Dist Comps':>16}")
    print("-" * 57)

    for r in epsilons:
        for name, fn, args in [
            ("Naive", naive_search, (D,)),
            ("Pivot-based", pivot_based_search, (D, refs, distances)),
            ("iDistance", idistance_search, (D, refs, distances, idistance_array, maxd_per_pivot, maxd)),
        ]:
            total_c = 0
            t0 = time.time()
            for qid, q in Q:
                _, c = fn(*args, q, r)
                total_c += c
            elapsed = time.time() - t0
            avg_c = total_c / len(Q)
            print(f"{r:<10} {name:<15} {elapsed:>12.4f} {avg_c:>16.2f}")

    print()
    print("=== kNN QUERIES ===")
    print(f"{'k':<10} {'Method':<15} {'Total Time':>12} {'Avg Dist Comps':>16}")
    print("-" * 57)

    for k in ks:
        for name, fn, args in [
            ("Naive", naive_knn, (D,)),
            ("Pivot-based", pivot_based_knn, (D, refs, distances)),
            ("iDistance", idistance_knn, (D, refs, distances, idistance_array, maxd_per_pivot, maxd)),
        ]:
            total_c = 0
            t0 = time.time()
            for qid, q in Q:
                _, c = fn(*args, q, k)
                total_c += c
            elapsed = time.time() - t0
            avg_c = total_c / len(Q)
            print(f"{k:<10} {name:<15} {elapsed:>12.4f} {avg_c:>16.2f}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python meros1.py part1 <data_file> [num_refs]")
        print("   or: python meros1.py part2 <data_file> [num_refs]")
        print("   or: python meros1.py part3 <data_file> <query_file> [num_refs] [r]")
        print("   or: python meros1.py part4 <data_file> <query_file> [num_refs] [k]")
        print("   or: python meros1.py part5 <data_file> <query_file> [num_refs]")
    elif sys.argv[1] == "part1":
        data_file = sys.argv[2]
        num_refs = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        part1(data_file, num_refs)
    elif sys.argv[1] == "part2":
        data_file = sys.argv[2]
        num_refs = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        part2(data_file, num_refs)
    elif sys.argv[1] == "part3":
        data_file = sys.argv[2]
        query_file = sys.argv[3]
        num_refs = int(sys.argv[4]) if len(sys.argv) > 4 else 10
        r = float(sys.argv[5]) if len(sys.argv) > 5 else 0.2
        part3(data_file, query_file, num_refs, r)
    elif sys.argv[1] == "part4":
        data_file = sys.argv[2]
        query_file = sys.argv[3]
        num_refs = int(sys.argv[4]) if len(sys.argv) > 4 else 10
        k = int(sys.argv[5]) if len(sys.argv) > 5 else 5
        part4(data_file, query_file, num_refs, k)
    elif sys.argv[1] == "part5":
        data_file = sys.argv[2]
        query_file = sys.argv[3]
        num_refs = int(sys.argv[4]) if len(sys.argv) > 4 else 10
        part5(data_file, query_file, num_refs)
    else:
        print("Unknown option")