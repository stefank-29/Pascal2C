#!/bin/bash
wd=$(pwd) && cd $(dirname ${BASH_SOURCE[0]})
for i in `find . ! -path . -type d | sort`; do
    rm -f "$i/gen" && ok=true
    for j in {1..5}; do
        t="$i/$j" && out=$(<"$t.out")
        src=$(python main.py "$i/src.pas" "$i/gen.c" <"$t.in")
        make "$i/gen" &> /dev/null && gen=$("$i/gen" <"$t.in")
        if [ "$src" != "$out" ] || [ "$gen" != "$out" ]; then
            printf "$t\tERROR\n\nIN\n$(<"$t.in")\n\nSRC\n$src\n\nGEN\n$gen\n\nOUT\n$out\n"
            ok=false && break
        fi
    done
    $ok && printf "$i\tOK\n"
done
cd $wd