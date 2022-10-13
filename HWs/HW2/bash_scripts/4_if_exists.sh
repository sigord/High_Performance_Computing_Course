#!/bin/bash
filenamedefault=Linux
truemessagedefault="course"
falsemessagedefault="very easy"
filemessagedefault="course is easy"
filename=${1:-$filenamedefault}
truemessage=${2:-$truemessagedefault}
falsemessage=${3:-$falsemessagedefault}
filemessage=${4:-$filemessagedefault}

if [ -f "$filename" ]; then
    echo $truemessage
else
    echo $falsemessage
    echo $filemessage > $filename
fi
