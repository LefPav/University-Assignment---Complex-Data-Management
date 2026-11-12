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

#getLinesFromFile(r"C:\Users\user\Desktop\assignment1\μερος2.1α\routes.dat")

def sort_merge_semijoin(r, s):
    joinedResults = []
    i, j = 0, 0
    start_time = time.time()
    
    # Ταξινόμηση και των δύο με βάση το ID (index 0)
    r.sort(key=lambda x: int(x[0]) if (len(x) > 0 and str(x[0]).isdigit()) else -1)
    s.sort(key=lambda x: int(x[5]) if (len(x) > 5 and str(x[5]).isdigit()) else -1)
    
    while i < len(r) and j < len(s):
        try:
            r_id = int(r[i][0])
            s_id = int(s[j][5])
            
            if r_id == s_id:
                # Βρέθηκε match! 
                # Κρατάμε ΟΛΕΣ τις πλειάδες από την r που έχουν αυτό το ID
                current_id = r_id
                while i < len(r) and int(r[i][0]) == current_id:
                    joinedResults.append(r[i])
                    i += 1
                # Αφού εξαντλήσαμε τα matches για αυτό το ID, προχωράμε και στην s
                while j < len(s) and int(s[j][5]) == current_id:
                    j += 1
                    
            elif r_id < s_id:
                i += 1
            else:
                j += 1
        except (ValueError, IndexError):
            i += 1
            j += 1
            continue
            
    print(f"Results: {joinedResults}")
    print(f"Number of results: {len(joinedResults)}")
    end_time = time.time()
    print(f"Sort-Merge Runtime: {end_time - start_time:.4f} seconds")
    return joinedResults
    
def hash_semijoin(r,s):
    # Έστω r η λίστα με τα routes
    # Έστω s η λίστα με τα αεροδρόμια (tuples)
# Κρατάμε μόνο τα ID σε ένα set για ταχύτητα
    start_time = time.time()
    airport_ids_set = set()
    for airport in r:
        airport_ids_set.add(int(airport[0]))
    
    matching_ids = set()
    for route in s:
        dest_id = int(route[5])
        if dest_id in airport_ids_set:
            # Αν το ID της πτήσης υπάρχει στα αεροδρόμια, το αποθηκεύουμε
            matching_ids.add(dest_id)
    # Τώρα φτιάχνουμε την τελική λίστα με τα tuples των αεροδρομίων που βρήκαμε
    result = []
    for airport in r:
        if int(airport[0]) in matching_ids:
            result.append(airport)
    print(result)
    print(f"Number of results: {len(result)}")
    end_time = time.time()    
    print(f"Hash Runtime: {end_time - start_time:.4f} seconds")
        
test_r = [(1,2),(1,4),(2,5)]
test_s = [(1,'a'),(1,'c'),(3,'a')]
newtest_r = getLinesFromFile(r"C:\Users\user\Desktop\assignment1\μερος2.1α\airports.dat")
newtest_s = getLinesFromFile(r"C:\Users\user\Desktop\assignment1\μερος2.1α\routes.dat")
hash_semijoin(newtest_r, newtest_s)         
    


    



    

