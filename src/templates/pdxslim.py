import csv
with open('pdx-cancer.tsv', 'rb') as f: #opens the template file
    reader = csv.reader(f, delimiter='\t') #reads it as a tsv
    l = list(reader) #makes a list from tsv

def extract(x): #extracts the ncit xrefs from the tsv id list
    global lst
    global xrefs
    xrefs = ('../ontology/results/ncit-xrefs.txt')
    lst = [item[x] for item in l] #takes the first value of each nested list (IDs)
    lst = lst[2:] #removes the two rows of "titles"
    lst = [y for y in lst if "PDXO:" not in y] #removes any PDXO: xrefs
    with open (xrefs, "w") as output: #writes the result to the slim.txt file
        writer = csv.writer(output, lineterminator='\n')
        for xref in lst:
            writer.writerow([xref])

extract(0)
