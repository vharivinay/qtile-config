#!/bin/sh

sed -n '/START_KEYS/,/END_KEYS/p' \
 ~/.config/qtile/sxhkd/sxhkdrc |\
  grep -v '###' |\
  grep -v '  ' | \
  sed -e 's/^#*//'\
  -e 's/ KB_GROUP /\n/' | \
  yad --text-info --back=#282c38 --fore=#46d9ff --geometry=1200x800