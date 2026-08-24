# Linux File Analysis

## file

Identify file type.

``` bash
file suspicious.jpg
```

Do not trust extensions.

## stat

Metadata:

``` bash
stat file
```

Shows: - size - owner - timestamps - permissions

## strings

Extract readable text:

``` bash
strings binary
```

Useful for: - hidden flags - malware analysis - binaries

## xxd

Hex view:

``` bash
xxd file
```

Useful to inspect raw bytes.

