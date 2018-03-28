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

# ----------------------------------------
# Top-level targets
# ----------------------------------------

all: sparql_test $(ONT).owl $(ONT).obo
test: sparql_test all
prepare_release: all
	cp $(ONT).owl $(ONT).obo $(RELEASEDIR) &&\
	echo "Release files are now in $(RELEASEDIR) - now you should commit, push and make a release on github"

# ----------------------------------------
# Main release targets
# ----------------------------------------

# by default we use Elk to perform a reason-relax-reduce chain
# after that we annotate the ontology with the release versionInfo
$(ONT).owl: $(SRC) pdx-generated.owl
	$(ROBOT) merge --input $(SRC) reduce -r ELK annotate --ontology-iri $(BASE)/$(ONT).owl -V $(BASE)/releases/`date +%Y-%m-%d`/$(ONT).owl -o $@
$(ONT).obo: $(ONT).owl
	$(ROBOT) convert -i $< -f obo -o $(ONT).obo.tmp && mv $(ONT).obo.tmp $@

# ----------------------------------------
# Templates
# ----------------------------------------

pdx-generated.owl:../templates/pdx-cancer.tsv
	$(ROBOT) merge --input $(SRC) template --merge-before --template ../templates/pdx-cancer.tsv --output results/pdx-generated.owl

# ----------------------------------------
# Import modules
# ----------------------------------------
# Most ontologies are modularly constructed using portions of other ontologies
# These live in the imports/ folder
# These can be regenerated with make all_imports


# sparql

imports/ncit_import.txt: $(GENERATED) imports/ncit.owl
	$(ROBOT) merge --input imports/ncit.owl --input $(GENERATED) query --select $(SPARQLDIR)/get_ncit_mappings.sparql imports/ncit_import.txt 

results/ncit_module.owl: imports/ncit_import.txt
	$(ROBOT) extract  --method BOT --input imports/ncit.owl --term-file imports/ncit_import.txt --output results/ncit_module.owl

pdx_ncit_bridge.owl: $(GENERATED) imports/ncit.owl
	$(ROBOT) query --input $(GENERATED) --format ttl --construct $(SPARQLDIR)/construct_ncit_bridge.sparql pdx_ncit_bridge.owl

# ----------------------------------------
# Release
# ----------------------------------------
# copy from staging area (this directory) to top-level
release: $(ONT).owl $(ONT).obo
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