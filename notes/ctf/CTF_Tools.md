# CTF Tools

## grep

Search text.

``` bash
grep "flag" file
```

Case insensitive:

``` bash
grep -i "flag" file
```

Line numbers:

``` bash
grep -n "secret" file
```

## cut

Extract fields.

Example:

    user:password

Command:

``` bash
cut -d ":" -f 2
```

Result:

    password

## tr

Transform text.

Remove spaces:

``` bash
tr -d ' '
```

## awk

Process text.

Remove duplicates:

``` bash
awk '!seen[$0]++'
```

## pipes

Connect commands:

``` bash
cat log | grep flag
```

