#!/bin/bash
DIR=$1
[[ -z $DIR ]] && DIR=files

[[ ! -d $DIR ]] && mkdir $DIR

for i in 1 10 100 1024; do
   SIZE=$(( i ))
   for j in $(seq 1 100); do
      dd if=/dev/urandom of=$DIR/file-$SIZE-${j}.raw bs=1024 count=$SIZE
   done
done

SIZE=$(( 100 * (2 ** 10) ))
for j in $(seq 1 10); do
   dd if=/dev/urandom of=$DIR/file-$SIZE-${j}.raw bs=1024 count=$SIZE

done

SIZE=$(( SIZE * 10 ))
dd if=/dev/urandom of=$DIR/file-$SIZE-1.raw bs=1024 count=$SIZE

