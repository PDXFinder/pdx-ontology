import csv
with open('pdx-cancer.tsv', 'rb') as f:
    reader = csv.reader(f, delimiter='\t')
    l = list(reader)

def extract(x):
    global lst
    global slim
    slim = ('../ontology/results/slim.txt')
    lst = [item[x] for item in l] #takes the first value of each nested list (IDs)
    lst = lst[2:] #removes the two rows of "titles"
    lst = [y for y in lst if "PDXO:" not in y] #removes any PDXO: xrefs
    with open (slim, "w") as output: #writes the result to the slim.txt file
        writer = csv.writer(output, lineterminator='\n')
        for xref in lst:
            writer.writerow([xref])

extract(0)
