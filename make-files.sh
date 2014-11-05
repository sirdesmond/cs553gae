#!/bin/bash
DIR=$1
[[ -z $DIR ]] && DIR=files

[[ ! -d $DIR ]] && mkdir $DIR

function random_name {
   FNAME=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 10 | head -n 1)
   while [ -e $DIR/$FNAME ]; do
      FNAME=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 10 | head -n 1)
   done
   echo $FNAME
}

function gen_sequential {

   for i in 1 10 100 1024; do
      SIZE=$(( i ))
      for j in $(seq 1 100); do
         dd if=/dev/urandom of=$DIR/file-$SIZE-${j}.raw bs=1024 count=$SIZE
      done
   done

   SIZE=$(( 10 * (2 ** 10) ))
   for j in $(seq 1 10); do
      dd if=/dev/urandom of=$DIR/file-$SIZE-${j}.raw bs=1024 count=$SIZE

   done

   SIZE=$(( SIZE * 10 ))
   dd if=/dev/urandom of=$DIR/file-$SIZE-1.raw bs=1024 count=$SIZE
}

function gen_random_names {
   for i in 1 10 100 1024; do
      SIZE=$(( i ))
      for j in $(seq 1 100); do
         NAME=$(random_name)
         dd if=/dev/urandom of=$DIR/$NAME bs=1024 count=$SIZE
      done
   done

   SIZE=$(( 10 * (2 ** 10) ))
   for j in $(seq 1 10); do
      NAME=$(random_name)
      dd if=/dev/urandom of=$DIR/$NAME bs=1024 count=$SIZE

   done

   SIZE=$(( SIZE * 10 ))
   NAME=$(random_name)
   dd if=/dev/urandom of=$DIR/$NAME bs=1024 count=$SIZE
}

gen_random_names
