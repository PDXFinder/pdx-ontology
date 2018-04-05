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
PREFIX = "PDX: http://purl.obolibrary.org/obo/PDX_"

# ----------------------------------------
# Top-level targets
# ----------------------------------------

all: sparql_test $(ONT).owl $(ONT).obo results/ncit_module.owl pdx-slim.owl
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

$(ONT)_ncit_merged.owl: $(SRC) pdx-slim.owl $(NCIT)
	$(ROBOT) merge --input $(SRC) --input pdx-slim.owl --input results/hp_module.owl reason -s true -m false -r ELK annotate -V $(BASE)/releases/`date +%Y-%m-%d`/$(ONT)_hpo_merged.owl -o $@


# ----------------------------------------
# Templates
# ----------------------------------------

pdx-generated.owl:../templates/pdx-cancer.tsv
	$(ROBOT) merge --input $(SRC) template --merge-before --prefix $(PREFIX) --template ../templates/pdx-cancer.tsv --output results/pdx-generated.owl

# ----------------------------------------
# Import modules
# ----------------------------------------
# Most ontologies are modularly constructed using portions of other ontologies
# These live in the imports/ folder
# These can be regenerated with make all_imports

IMPORTS = ro
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

# NCIT MODULE USING RESULT OF PYTHON
# need to embed python script into make file!!!

results/ncit_module.owl: results/ncit-xrefs.txt
	$(ROBOT) extract  --method BOT --input $(NCIT) --term-file results/ncit-xrefs.txt --output results/ncit_module.owl
	
pdx-slim.owl: $(GENERATED)
	$(ROBOT) query --input $(GENERATED) --format ttl --construct $(SPARQLDIR)/construct_slim.sparql pdx-slim.owl

## NEEDS EDITING

pdx-ncit-merged.owl: pdx-slim.owl $(GENERATED) results/ncit_module.owl
	owltools results/ncit_module.owl --map2slim --idfile slim.terms --write-gaf annotations.mapped.gaf

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