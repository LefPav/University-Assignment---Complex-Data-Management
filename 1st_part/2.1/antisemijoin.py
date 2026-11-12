import time

def getLinesFromFile(filename):
    airports = []
    routes = []
    try:
        infile = open(filename, 'r', encoding='utf-8')
        if filename.endswith("airports.dat"):
            for line in infile:
                parts = line.strip().split(',')
                tupleConverted = tuple(parts)
                airports.append(tupleConverted)
       
            return  airports
        elif filename.endswith("routes.dat"):
            for line in infile:
                parts = line.strip().split(',')
                tupleConverted = tuple(parts)
                routes.append(tupleConverted)
            
            return  routes
    except FileNotFoundError:
        print(f"File not found: {filename}")
    return  None

def sort_merge_antisemijoin(a, r):
    joinedResults = []
    number0fResults = 0
    i,j = 0,0
    start_time = time.time()
    r.sort(key=lambda x: int(x[5])) #if x[0].isdigit() else 0)
    a.sort(key=lambda x: int(x[0])) #if x[0].isdigit() else 0)
    while j < len(a):
        # Αν τελειώσουν οι πτήσεις, όλα τα επόμενα αεροδρόμια είναι anti-matches
        if i >= len(r):
            joinedResults.append(a[j])
            j += 1
            continue

        try:
            r_id = int(r[i][5])
            a_id = int(a[j][0])
        except:
            j += 1
            continue

        if a_id == r_id:
            # Υπάρχει πτήση! Άρα το αεροδρόμιο αυτό ΔΕΝ μπαίνει στο anti-semijoin
            current_id = a_id
            while j < len(a) and int(a[j][0]) == current_id:
                j += 1
            # Προσπερνάμε και όλες τις πτήσεις που έχουν αυτό το ID
            while i < len(r) and (int(r[i][5]) if str(r[i][5]).isdigit() else -1) == current_id:
                i += 1
        elif a_id < r_id:
            # Το αεροδρόμιο έχει μικρότερο ID από την τρέχουσα πτήση.
            # Επειδή οι πτήσεις είναι ταξινομημένες, δεν θα βρεθεί ποτέ.
            joinedResults.append(a[j])
            j += 1
        else:
            # Η πτήση έχει μικρότερο ID, προχωράμε για να φτάσουμε το αεροδρόμιο
            i += 1
    print(joinedResults)
    print(f"Number of results: {len(joinedResults)}")
    end_time = time.time()    
    print(f"Sort-Merge antisemijoin Runtime: {end_time - start_time:.4f} seconds")
    return joinedResults

     
    
def hash_antisemijoin(a, r):
    start_time = time.time()
    airport_ids_set = set()
    for route in r:
        try:
            dest_id = int(route[5])
            airport_ids_set.add(dest_id)
        except:
            continue
    
    result = []
    for airport in a:
        try:
            airport_id = int(airport[0])
            if airport_id not in airport_ids_set:
                result.append(airport)
        except:
            continue
    print(result)
    print(f"Number of results: {len(result)}")
    print(f"Βρέθηκαν {len(airport_ids_set)} μοναδικά IDs αεροδρομίων.")
    end_time = time.time()    
    print(f"Hash Anti-Semijoin Runtime: {end_time - start_time:.4f} seconds")


test_a = [(1,2),(1,4),(2,5)]
test_r = [(1,'a'),(1,'c'),(3,'a')]
newtest_a = getLinesFromFile(r"C:\Users\user\Desktop\assignment1\μερος2.1α\airports.dat")
newtest_r = getLinesFromFile(r"C:\Users\user\Desktop\assignment1\μερος2.1α\routes.dat")
sort_merge_antisemijoin(newtest_a, newtest_r)  
hash_antisemijoin(newtest_a, newtest_r)