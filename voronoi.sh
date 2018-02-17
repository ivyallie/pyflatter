#!/bin/sh

convert /tmp/voronoi_input.png \
\( +clone -alpha extract -morphology edgein diamond:1 \) \
-alpha off -compose copy_opacity -composite \
-background black -alpha background -depth 8 txt:- |\
grep -v "none" |\
sed -n 's/^\(.*,.*\):.*[#][^ ]*  \(.*\)$/\1,\2/p' > /tmp/vortemp
convert /tmp/voronoi_input.png \
\( +clone -alpha off -sparse-color voronoi '@/tmp/vortemp' \) \
+swap -compose over -composite output.png

rm /tmp/vortemp
