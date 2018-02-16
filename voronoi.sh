#!/bin/sh

convert voronoi_input.png \
\( +clone -alpha extract -morphology edgein diamond:1 \) \
-alpha off -compose copy_opacity -composite \
-background black -alpha background -depth 8 txt:- |\
grep -v "none" |\
sed -n 's/^\(.*,.*\):.*[#][^ ]*  \(.*\)$/\1,\2/p' | \
convert voronoi_input.png \
\( +clone -alpha off -sparse-color voronoi '@-' \) \
+swap -compose over -composite output.png
