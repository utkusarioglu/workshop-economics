#!/bin/bash
set -o vi
export PS1="\$(git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/\1/') \t \u@\h \w \[$(tput sgr0)\]"
source activate econ
