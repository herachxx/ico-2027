# picoCTF 2026 - Log Hunt

Category: General Skills / Forensics

## Description

The challenge provided server logs containing scattered and duplicated
flag fragments.

Goal: reconstruct the original flag.

## Solution

Search for flag-related entries:

``` bash
grep -i "flag" server.log
```

`grep` searches text patterns. `-i` makes the search case-insensitive.

Extract the fragment field:

``` bash
cut -d ":" -f 4
```

-   `cut` splits text into fields.
-   `-d ":"` uses `:` as the separator.
-   `-f 4` selects the fourth field.

Remove spaces:

``` bash
tr -d ' '
```

Remove duplicates while preserving order:

``` bash
awk '!seen[$0]++'
```

Final flag:

``` text
picoCTF{us3_y0urlinux_sk1lls_cedfa5fb}
```

## Lessons Learned

-   grep
-   cut
-   tr
-   awk
-   Linux pipelines
-   log analysis

