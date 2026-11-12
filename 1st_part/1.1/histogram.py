def getAgesFromFile(filename):
    agelist = []
    splitedRow = []
    try:
        infile = open(filename, 'r')
        for line in infile:
            splitedRow = line.split()  
            agelist.append(int(splitedRow[1]))
        infile.close()
        return agelist
    except FileNotFoundError:
        print("File not found.")
    
        

def equalWidthHistogram(agelist):
    maxAge = max(agelist)
    minAge = min(agelist)
    W = (maxAge - minAge) / 10
    bins = [0] * 10
    for age in agelist:
        if age == maxAge:
            bins[9] += 1
        else:
            index = int((age - minAge) / W)
            bins[index] += 1
    return bins



def equalFrequencyHistogram(agelist):
    sorted_ages = sorted(agelist)
    n = len(sorted_ages)
    depth = n // 10
    boundaries = []
    for i in range(10):
        boundaries.append(sorted_ages[i * depth])
        
    boundaries.append(sorted_ages[-1])
    return boundaries




def main():
    outfile = open(r"C:\Users\user\Desktop\assignment1\μερος1.1\histogram_output.txt", 'w')
    filename = r"C:\Users\user\Desktop\assignment1\μερος1.1\final_general.dat"
    agelist = getAgesFromFile(filename)
    widthHistogram = equalWidthHistogram(agelist)
    frequencyHistogram = equalFrequencyHistogram(agelist)
    outfile.write("Ages: " + str(len(agelist)) + "\n" + "Min age: " + str(min(agelist)) + "\n" + "Max age: " + str(max(agelist)) + "\n" + "Width: " + str((max(agelist) - min(agelist)) / 10) + "\n")
    outfile.write("Equal-width histogram bins: " + str(widthHistogram) + "\n")
    outfile.write("Equi-depth boundaries: " + str(frequencyHistogram) + "\n")
    outfile.close()
    
main()
    

    
