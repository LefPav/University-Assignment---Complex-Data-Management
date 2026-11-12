import sys
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
            return airports
        elif filename.endswith("routes.dat"):
            for line in infile:
                parts = line.strip().split(',')
                tupleConverted = tuple(parts)
                routes.append(tupleConverted)
            return routes
    except FileNotFoundError:
        print(f"File not found: {filename}")
    return None

def selection_sort_merge_semijoin(aircraft_type):
    # Φόρτωση δεδομένων με τη δική σου συνάρτηση
    # Προσοχή: Βεβαιώσου ότι τα αρχεία είναι στον ίδιο φάκελο ή βάλε το πλήρες path
    airports = getLinesFromFile(r"C:\Users\user\Desktop\assignment1\μερος2.2\airports.dat")
    all_routes = getLinesFromFile(r"C:\Users\user\Desktop\assignment1\μερος2.2\routes.dat")
    
    if not airports or not all_routes:
        print("Σφάλμα κατά τη φόρτωση των αρχείων.")
        return

    # 1. SELECTION: Φιλτράρισμα βάσει τύπου αεροσκάφους (τελευταίο πεδίο στο routes.dat)
    # Χρησιμοποιούμε r[-1] γιατί ο τύπος είναι το τελευταίο στοιχείο, 
    # και αφαιρούμε τυχόν εισαγωγικά για σωστή σύγκριση.
    filtered_routes = [
        r for r in all_routes 
        if len(r) > 0 and r[-1].replace('"', '').strip() == aircraft_type
    ]

    # 2. SORTING: Ταξινόμηση των φιλτραρισμένων διαδρομών βάσει ID προορισμού (index 5)
    # Τα αεροδρόμια είναι ήδη ταξινομημένα από το αρχείο, οπότε δεν τα πειράζουμε.
    filtered_routes.sort(key=lambda x: int(x[5].replace('"', '')) if x[5].replace('"', '').isdigit() else -1)

    # 3. SORT-MERGE SEMIJOIN (Η δική σου λογική προσαρμοσμένη στο Selection)
    joinedResults = []
    i, j = 0, 0
    
    # i για airports (index 0), j για filtered_routes (index 5)
    while i < len(airports) and j < len(filtered_routes):
        try:
            # Καθαρισμός IDs από εισαγωγικά πριν τη μετατροπή σε int
            r_id = int(airports[i][0].replace('"', ''))
            s_id = int(filtered_routes[j][5].replace('"', ''))
            
            if r_id == s_id:
                # Βρέθηκε ταίριασμα! Προσθέτουμε την πλειάδα του αεροδρομίου
                joinedResults.append(airports[i])
                
                # Επειδή θέλουμε Semijoin (τουλάχιστον μία διαδρομή), 
                # προχωράμε στο επόμενο αεροδρόμιο αμέσως
                current_id = r_id
                while i < len(airports) and int(airports[i][0].replace('"', '')) == current_id:
                    i += 1
                # Προσπερνάμε και όλες τις διαδρομές προς αυτό το αεροδρόμιο
                while j < len(filtered_routes) and int(filtered_routes[j][5].replace('"', '')) == current_id:
                    j += 1
                    
            elif r_id < s_id:
                i += 1
            else:
                j += 1
        except (ValueError, IndexError):
            i += 1
            j += 1
            continue

    # Εκτύπωση αποτελεσμάτων
    for row in joinedResults:
        print(",".join(row))
        
    print(f"\nΑποτελέσματα για τύπο {aircraft_type}: {len(joinedResults)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        t = sys.argv[1]
        selection_sort_merge_semijoin(t)
    else:
        print("Usage: python script_name.py <aircraft_type>")
        # Παράδειγμα: python myscript.py SU9