#!/bin/bash

while getopts "h" opt; do
  case $opt in
    h) echo "Usage: ./back.sh [TARGET] [ZIP METHOD]"
        echo -e "Available compression methods:\n-\tgzip\n-\tbzip2\n-\txz"
        exit 1
        ;;
    \?) echo "Invalid option: -$OPTARG" >&2 ;;
  esac
done

FOLDER=$1
ZIP=$2

if [ -z "$FOLDER" -o -z "$ZIP" ]; then
    echo "Incorrect usage. Run \"./back.sh -h\" for full syntax."
    exit 1
fi

if [ ! -d $FOLDER ]; then
    echo "back.sh: directory does not exist"
    exit 1
fi

if [ ! -r $FOLDER ];
then
    echo "User does not have necessary permissions."
    exit 1
elif [ ! -w $FOLDER ]; then
    echo "User does not have necessary permissions."
    exit 1
fi

if [[ $ZIP == "gzip" ]]; then
    OUTPUT="backup_$(date +%F-%H_%M_%S).tar.gz"
    tar -czvf $OUTPUT $FOLDER/
elif [[ $ZIP == "bzip2" ]]; then
    OUTPUT="backup_$(date +%F-%H_%M_%S).tar.bz2"
    tar -cjvf $OUTPUT $FOLDER/
elif [[ $ZIP == "xz" ]]; then
    OUTPUT="backup_$(date +%F-%H_%M_%S).tar.xz"
    tar -cJvf $OUTPUT $FOLDER/
else
    echo "back.sh: not a valid compression method"
    exit 1
fi

exit 0