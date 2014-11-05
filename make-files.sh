#!/bin/bash
DIR=$1
[[ -z $DIR ]] && DIR=files

[[ ! -d $DIR ]] && mkdir $DIR

function random_string {
   COUNT=$1
   FNAME=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w $COUNT | head -n 1)
   while [ -e $DIR/$FNAME ]; do
      FNAME=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w $COUNT | head -n 1)
   done
   echo $FNAME
}

function gen_random_names {
   for i in 1 10 100 1024; do
      SIZE=$(( i * 1024 ))
      for j in $(seq 1 100); do
         NAME=$(random_string 10)
         for k in $(seq 1 100 $SIZE ); do
            random_string 100 >> $DIR/$NAME
         done
      done
   done

   SIZE=$(( 10 * (2 ** 20) ))
   for j in $(seq 1 10); do
      NAME=$(random_string 10)
      for k in $(seq 1 100 $SIZE ); do
         random_string 100 >> $DIR/$NAME
      done

   done

   SIZE=$(( SIZE * 10 ))
   NAME=$(random_string 10)
   for k in $(seq 1 100 $SIZE ); do
      random_string 100 >> $DIR/$NAME
   done
}

gen_random_names
