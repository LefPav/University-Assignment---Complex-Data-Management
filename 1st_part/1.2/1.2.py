def getAgesFromFile(filename):
    agelist = []
    splitedRow = []
    try:
        infile = open(filename, 'r')
        for line in infile:
            splitedRow = line.split()  
            agelist.append(int(splitedRow[1]))
        print(f"Διαβάστηκαν {len(agelist)} ηλικίες.")
        infile.close()
        return agelist
    except FileNotFoundError:
        print("File not found.")

def main(a, b):
    infile = open(r"C:\Users\user\Desktop\assignment1\μερος1.1\histogram_output.txt", 'r')
    ListOfAges = getAgesFromFile(r"C:\Users\user\Desktop\assignment1\μερος1.1\final_general.dat")
    equiwidth_histogram = []
    equiFrequency_histogram = []
    numberOfAges = 0
    width = 0
    minAge = 0
    maxAge = 0
    estimatedCountDepth = 0
    estimatedCountWidth = 0
    RealCount = 0
    Bins = []
    
    for line in infile:
        if line.startswith("Equal-width histogram bins:"):
            # Μετατροπή του string "[1, 2, 3]" σε πραγματική λίστα αριθμών
            data = line.split(":")[1].strip().strip('[]')
            equiwidth_histogram = [int(x.strip()) for x in data.split(',') if x.strip()]
        elif line.startswith("Equi-depth boundaries:"):
            # Παρομοίως για το equi-depth
            data = line.split(":")[1].strip().strip('[]')
            equiFrequency_histogram = [float(x.strip()) for x in data.split(',') if x.strip()]
        elif line.startswith("Ages:"):
            numberOfAges = int(line.split(":")[1].strip()) # Μετατροπή σε int
        elif line.startswith("Min age:"):
            minAge = float(line.split(":")[1].strip())     # Μετατροπή σε float
        elif line.startswith("Max age:"):
            maxAge = float(line.split(":")[1].strip())     # Μετατροπή σε float
        elif line.startswith("Width:"):
            width = float(line.split(":")[1].strip())      # Μετατροπή σε float
    print(f"---------------------------------|-----------------------------------")
    print(f"Equal-width histogram calculation for ages between {a} and {b}:")     
    for i in range(10):
        lower = minAge + float(i) * width
        upper = minAge + float((i + 1)) * width
        Bins.append((lower, upper))
    for i in range(10):
        current_bin = Bins[i]
        lower = current_bin[0]
        upper = current_bin[1]
        # Έλεγχος επικάλυψης
        if max(lower, a) < min(upper, b):
            overlap = min(upper, b) - max(lower, a)
            # Χρησιμοποιούμε += για να προσθέτουμε στο σύνολο
            estimatedCountWidth += equiwidth_histogram[Bins.index(current_bin)] * (overlap / width)
    print(f"Estimated count for ages between {a} and {b}: {estimatedCountWidth}")
    print(f"---------------------------------|-----------------------------------")
    print(f"Equi-depth histogram calculation for ages between {a} and {b}:")    
    for i in range(10):
    # Καθαρίζουμε τις τιμές από τυχόν αγκύλες ή κενά πριν τις κάνουμε int
        lower_raw = str(equiFrequency_histogram[i]).replace('[','').replace(']','').replace('(','').replace(')','').replace(',', '').strip()
        upper_raw = str(equiFrequency_histogram[i+1]).replace('[','').replace(']','').replace('(','').replace(')','').replace(',', '').strip()
        
        if lower_raw and upper_raw:
            lower = int(float(lower_raw))
            upper = int(float(upper_raw))
        # Έλεγχος αν το bin έχει επικάλυψη με το διάστημα [a, b]
            if max(lower, a) < min(upper, b):
                # Υπολογισμός του μέρους του bin που επικαλύπτεται
                overlap_dist = min(upper, b) - max(lower, a)
                bin_dist = upper - lower
                
                if bin_dist > 0:
                    # Ο τύπος σου: (Πλήθος ανά bin) * (Ποσοστό κάλυψης)
                    estimatedCountDepth += (numberOfAges / 10) * (overlap_dist / bin_dist)
                else:
                    # Αν lower == upper, το bin περιέχεται ολόκληρο
                    estimatedCountDepth += (numberOfAges / 10)
    print(f"Estimated count for ages between {a} and {b}: {estimatedCountDepth}")
    for age in ListOfAges:
        if age >= a and age <= b:
            RealCount +=1
    print(f"---------------------------------|-----------------------------------")
    print(f"Real count for ages between {a} and {b}: {RealCount}")
    infile.close()

val_a = int(input("Enter lower bound: "))
val_b = int(input("Enter upper bound: "))
main(val_a, val_b) # Περνάς τις τιμές στην main