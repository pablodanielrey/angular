#/bin/bash

for i in `list_lists -b`;
do
      for a in `list_members $i`;
      do
              withlist -r mod.set $i $a
      done
done
