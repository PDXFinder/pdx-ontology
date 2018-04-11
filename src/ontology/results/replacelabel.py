# Read in the file
with open('./results/ncit_module.owl', 'r') as file :
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('<rdfs:label>', '<rdfs:label rdf:datatype="http://www.w3.org/2001/XMLSchema#string">')

# Write the file out again
with open('./results/ncit_module2.owl', 'w') as file:
  file.write(filedata)
