[![Build Status](https://travis-ci.org/zoependlington/pdx-ontology.svg?branch=master)](https://travis-ci.org/zoependlington/pdx-ontology)
[![DOI](https://zenodo.org/badge/13996/zoependlington/pdx-ontology.svg)](https://zenodo.org/badge/latestdoi/13996/zoependlington/pdx-ontology)

# pdx-ontology

This ontology... YOUR DESCRIPTION HERE

## Build a OLS docker instance with ontologies in

```
docker build . -t pdxo-ols
docker run -p 8080:8080 -t pdxo-ols 
``` 

OLS should now be running at http://localhost:8080

## Versions

### Stable release versions

The latest version of the ontology can always be found at:

http://purl.obolibrary.org/obo/pdxo.owl

(note this will not show up until the request has been approved by obofoundry.org)

### Editors' version

Editors of this ontology should use the edit version, [/src/templates/pdx-cancer.tsv](/src/templates/pdx-cancer.tsv).
**NOTE:** It is important to define parent terms before the child terms in this template. Mandatory fields are the ID, Label, Parent and Preferred Label.

Once the edited template file has been saved, you can run the makefile.

```
cd src/ontology/
make

``` 

This will build the ontology from the template file.

Once this is complete, you will have a src/ontology/pdxo.owl file.
In order to release this to the top level directory:

```
make release 
``` 
You can now do a git commit and git push:

```
git add -u
git commit -m "message"
git push 

``` 

## Contact

Please use this GitHub repository's [Issue tracker](https://github.com/zoependlington/pdx-ontology/issues) to request new terms/classes or report errors or specific concerns related to the ontology.

## Acknowledgements

This ontology repository was created using the [ontology starter kit](https://github.com/INCATools/ontology-starter-kit)
