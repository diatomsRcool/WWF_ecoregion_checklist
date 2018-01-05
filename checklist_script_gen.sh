#!/bin/bash
# generates checklist_status.sh using wkt_string.tsv
# the generated checklist_status.sh produces checklist_status.tsv
# checklist_status.tsv contains a status overview of all checklists associated with wkt_string.tsv
# see https://github.com/effechecka/effechecka_scripts

source <(curl -s https://raw.githubusercontent.com/effechecka/effechecka-scripts/master/checklist_script_gen.sh)
