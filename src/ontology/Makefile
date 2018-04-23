# ----------------------------------------
# Standard Constants
# ----------------------------------------
# these can be overwritten on the command line

OBO=http://purl.obolibrary.org/obo
ONT=pdxo
BASE=$(OBO)/$(ONT)
SRC=$(ONT)-edit.owl
RELEASEDIR=../..
ROBOT= ../../bin/robot
OWLTOOLS= ../../bin/owltools
USECAT= --use-catalog
SPARQLDIR = ../sparql
NCIT = ../../imports/ncit.owl
GENERATED = ./results/pdx-generated.owl
PREFIX = "PDXO: http://purl.obolibrary.org/obo/PDXO_"
NCITPREFIX = "NCIT: http://purl.obolibrary.org/obo/NCIT_"
UPPER = ./imports/upper_class.owl

# ----------------------------------------
# Top-level targets
# ----------------------------------------

all: sparql_test $(SRC) $(ONT).owl $(GENERATED) results/ncit_module.owl pdx-slim.owl results/ncit-xrefs.txt pdx-ncit.owl pdx-module.owl #pdx-label.owl
test: sparql_test all
prepare_release: all
	cp $(ONT).owl $(RELEASEDIR) &&\
	echo "Release files are now in $(RELEASEDIR) - now you should commit, push and make a release on github"

# ----------------------------------------
# Main release targets
# ----------------------------------------

# by default we use Elk to perform a reason-relax-reduce chain
# after that we annotate the ontology with the release versionInfo
$(SRC): pdx-module.owl
	$(ROBOT) merge --input $(SRC) --input pdx-module.owl --prefix $(PREFIX) --prefix $(NCITPREFIX) -o $@

$(ONT).owl: $(SRC) pdx-module.owl
	$(ROBOT) merge --input $(SRC) --prefix $(PREFIX) --prefix $(NCITPREFIX) reduce -r ELK annotate --ontology-iri $(BASE)/$(ONT).owl -V $(BASE)/releases/`date +%Y-%m-%d`/$(ONT).owl -o $@



# ----------------------------------------
# Templates
# ----------------------------------------

$(GENERATED):../templates/pdx-cancer.tsv
	$(ROBOT) merge --input $(UPPER) template --merge-before --prefix $(PREFIX) --prefix $(NCITPREFIX) --template ../templates/pdx-cancer.tsv reason -s true -m false -r ELK --output $(GENERATED)

# ----------------------------------------
# Import modules
# ----------------------------------------
# Most ontologies are modularly constructed using portions of other ontologies
# These live in the imports/ folder
# These can be regenerated with make all_imports

IMPORTS =
IMPORTS_OWL = $(patsubst %, imports/%_import.owl,$(IMPORTS)) $(patsubst %, imports/%_import.obo,$(IMPORTS))

# Make this target to regenerate ALL
all_imports: $(IMPORTS_OWL)

# Use ROBOT, driven entirely by terms lists NOT from source ontology
imports/%_import.owl: mirror/%.owl imports/%_terms.txt
	$(ROBOT) extract -i $< -T imports/$*_terms.txt --method BOT -O $(BASE)/$@ -o $@
.PRECIOUS: imports/%_import.owl

# we use owltools for making the obo file until: https://github.com/ontodev/robot/issues/64
imports/%_import.obo: imports/%_import.owl
	$(OWLTOOLS) $(USECAT) $< -o -f obo $@

# clone remote ontology locally, perfoming some excision of relations and annotations
mirror/%.owl: $(SRC)
	$(OWLTOOLS) $(OBO)/$*.owl --remove-annotation-assertions -l -s -d --remove-dangling-annotations  -o $@
.PRECIOUS: mirror/%.owl

# ----------------------------------------
# Slim & Annotations
# ----------------------------------------

# creating the ncit module
## uses the python script to extract all ncit uris and outputs them to a text file
## the text file is then used to extract these terms from the ncit.owl file to form a
## module containing all desired terms. this prevents the ncit.owl file from being directly
## accessed by the make file or edited too often, which slows down the generation of the
## ontology and also uses up bandwidth on git-lfs.

results/ncit-xrefs.txt: ../templates/pdxslim.py
	python ../templates/pdxslim.py > results/ncit-xrefs.txt

results/ncit_module.owl: results/ncit-xrefs.txt
	$(ROBOT) extract  --method BOT --input $(NCIT) --term-file results/ncit-xrefs.txt --output results/ncit_module.owl
	
# ensures all labels are of datatype string to avoid duplicates
results/ncit_module2.owl: results/replacelabel.py
	python results/replacelabel.py > results/ncit_module2.owl

# creating the slim
## SPARQL query
## extracts the URIs and attaches inSubset pdx_slim annotation to each term

pdx-slim.owl: $(GENERATED)
	$(ROBOT) query --input $(GENERATED) --format ttl --construct $(SPARQLDIR)/construct_slim.sparql pdx-slim.owl
	

### Merging ttl with template terms, resulting in the slim annotation of "pdx_slim" being applied to the terms
### no term annotations are added at this point

pdx-ncit.owl: $(GENERATED) results/ncit_module2.owl pdx-slim.owl
	$(ROBOT) merge --input $(GENERATED) --input results/ncit_module2.owl --input pdx-slim.owl --prefix $(PREFIX) --prefix $(NCITPREFIX) -o pdx-ncit.owl

### owltools extraction of annotations
### adds ncit annotations to the merged slim and generated file.

pdx-module.owl: pdx-ncit.owl
	$(OWLTOOLS) pdx-ncit.owl --extract-ontology-subset -u $(BASE).owl -s pdx_slim -o pdx-module.owl
	
# ----------------------------------------
# Release
# ----------------------------------------
# copy from staging area (this directory) to top-level
release: $(ONT).owl
	cp $^ $(RELEASEDIR) && cp imports/* $(RELEASEDIR)/imports

# ----------------------------------------
# Sparql queries: Q/C
# ----------------------------------------

# these live in the ../sparql directory, and have suffix -violation.sparql
# adding the name here will make the violation check live
VCHECKS = equivalent-classes trailing-whitespace owldef-self-reference xref-syntax nolabels

# run all violation checks
VQUERIES = $(foreach V,$(VCHECKS),$(SPARQLDIR)/$V-violation.sparql)
sparql_test: $(SRC)
	$(ROBOT) verify -i $< --queries $(VQUERIES) -O reports/

# ----------------------------------------
# Sparql queries: Reports
# ----------------------------------------

REPORTS = basic-report class-count-by-prefix edges xrefs obsoletes synonyms
REPORT_ARGS = $(foreach V,$(REPORTS),-s $(SPARQLDIR)/$V.sparql reports/$V.tsv)
all_reports: $(SRC)
	robot query -f tsv -i $< $(REPORT_ARGS)