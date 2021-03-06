# WWF_ecoregion_checklist

This repository contains code for making species checklists for ecoregions defined by WWF using the effechecka API and submitting through Jenkins. The code works by submitting polygons to effechecka which then assembles deduplicated lists of all the taxa with occurrence data within the polygon. 

## Getting the Polygons

The polygons used in this code are from WWF and Google (https://fusiontables.google.com/DataSource?docid=1wAlo-9OT2NWlx-0XfdzxqzT8uwvdHyth-_HXHb4) and can be downloaded as a csv file, which is too large for GitHub. Each row in the file is a separate polygon, so ecoregions will have multiple rows depending on how disconnected they are. There are 827 unique ecoregions and X polygons. The polygons were translated into wkt strings for submission to effechecka (wkt_large.txt and wkt_small.txt). The polygons were also grouped into wkt strings - one for each ecoregion (all_wkt_string.txt), but these wkt strings were far too long for effechecka. The wkt strings in wkt_large.txt were too long to be submitted to the API. Only the wkt strings in wkt_small.txt were submitted to effechecka.

## Getting the lists

The effechecka API was used in two steps. First, the query had to be submitted, then the results downloaded. Since these are very large lists, it can take some time between the initial query and completion of the list. The first time a query is submitted, effechecka starts compiling the list. The second time it is submitted, the results are downloaded, if they are ready. If they are not ready, you will have to submit the query again later. The Jenkins job will automatically do this for you. The code for the Jenkins job is in checklists_script_gen.sh.

Effechecka gives lists back as tsv files. These files are downloaded into a checklists directory with the id # used to tag the wkt string as the file name, in this case, the id is a number assigned by Google. When all of the checklists are complete and downloaded, the script compresses all the lists in checklist.tar.gz. This needs to be downloaded to a local machine outside of this directory because the files will be too large for GitHub. Every ecoregion polygon has a checklist file and the filename is the id number. When you are done, you shoud have a directory that has a subdirectory for every polygon, with the corresponding tsv checklist file in that directory.

## Making the TraitBank files

Checklists need to be translated into DwC format for upload into TraitBank. This is done with checklist_to_traitbank.py which uses functions in checklist_functions.py. The first block of code makes the dictionaries needed to keep track of all the taxon ids and parent ids. The second block of code generates the TraitBank files. These files are compressed and uploaded into EOL opendata for eventual upload into TraitBank. Each water body will have its own TraitBank DwC-A.

I have not written any code to automatically generate the zipped archives for upload into opendata. This can be done manually or via the command line using the zipfile Python library. An example, that creates and archive for the Red Sea is below.

python -m zipfile -c red_sea.zip tb_measurement.txt tb_occurrence.txt tb_taxon tb_references meta.xml

The archive is submitted to https://opendata.eol.org/dataset/water-body-checklists manually.

## File Descriptions

checklist_functions.py - This file contains commonly-used functions to prepare the tsv checklist for processing into TraitBank files. They are used in checklist_to_traitbank.py

checklist_script_gen.sh - A bash script for creating the effechecka queries from a list of wkt strings (wkt_string.tsv). It also creates two other scripting files, checklist_status.sh and checklist_download.sh. These are the scripts that run in Jenkins. Every time this GitHub repository is updated, the Jenkins job is triggered. So, if the wkt_string.tsv file is updated, the scripts get run automatically.

checklist_to_traitbank.py - This code iterates over the directory containing the checklists that were obtained via the Jenkins job (checklist_script_gen.sh). In the directory is a subdirectory containing the effechecka output (tsv) for each country. The code goes through each directory and creates the taxon id and parent dictionaries needed to create the measurement, taxon, and occurrence files for each country-based DwC-A. The input is the tsv checklist. The outputs are the files for the TraitBank DwC-A. This code also outputs some summary stats for each water body to a separate file.

list_results.tsv - This is a list of all the water bodies with their mrgid and some stats about their checklists. These stats are out of date! Ignore the stats. Use the list to iterate over all the water bodies with their mrgids.

low_res_sea.json - 

make_water_dict.py - This code made polygon_dict.p that links mrgids and polygons and water_dict.p that links water bodies with their mrgids.

make_wkstring.py - This code makes wkt strings for every polygon in low_res_sea.json. These are the wkt strings used by checklists_script_gen.sh. The result is wkt_string.tsv.

marine_filter.py - This code filters out non-marine taxa only. It is no longer used in lieu of the rename_and_filter_checklist.py code.

marine_taxa.p - This is a list of taxa that were collated from the existing checklists and cross-referenced with WoRMS. According to WoRMS the taxa on this list are marine. It acts as a "white list". 

meta.xml - This is a file that describes the contents of the DwC-A. It must be included in the archive. You should not have to change this.

not_marine_taxa.p - This is a list of taxa that were collated from the existing checklists and cross-referenced with WoRMS. According to WoRMS the taxa on this list are NOT marine. It acts as a "black list". 

parent_dict.p - This dictionary is for looking up a parent for any taxon. The taxon is the key and its parent is the value. It is created by rename_and_filter_checklist.py. This dictionary is redone for every water body.

polygon_dict.p - This dictionary allows looking up a polygon by the corresponding water body's mrgid. It was created by make_country_dict.py

reduce_polygon.py - This file iterates over all the JSON files in this repo and reduces the resolution of the polygons. It creates the low_res_sea.json file.

rename_and_filter_checklist.py - This code changes file names from a mrgid to a water body name and creates directories for each water body. All checklists except for the major oceans (Indian, Pacific, Southern, Atlantic, Arctic) are filtered using data from WoRMS to remove all non-marine taxa. This code uses marine_taxa.p and non_marine_taxa.p to do the filtering. Any taxa that does not show up as being either marine or non-marine is output in a separate file. The output of this code will print a message to tell you if a taxon in the list is not showing up.

taxon_id.p - This dictionary is for looking up the taxon id for any taxon. The taxon is the key and its id is the value. It is created by rename_and_filter_checklist.py. The identifier in question is local and only valid within the Darwin Core Archive. This dictionary is redone for every water body.

tb_references.txt - This is the references file extension for the DwC-A. The Date accessed for IHO and Fresh Data MAY need to be changed.

wkt_string.tsv - A list with one wkt string for each country and its mrgid. This file is used by checklists_script_gen.sh to formulate the effechecka queries
