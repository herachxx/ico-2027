# picoCTF 2026 - My Git

Category: General Skills / Git Security

## Description

The README stated:

> If you want the flag, make sure to push the flag!

Only `flag.txt` pushed by `root:root@picoctf` would be updated with the
flag.

## Enumeration

Clone the repository:

``` bash
git clone <repository>
```

Check files:

``` bash
ls -la
```

Check history:

``` bash
git log
```

## Vulnerability

Git commits contain metadata:

-   Author
-   Committer

Git does not verify that the user is actually that identity.

Configure:

``` bash
git config user.name "root"
git config user.email "root@picoctf"
```

Create and commit:

``` bash
touch flag.txt
git add flag.txt
git commit -m "Add flag"
```

Verify:

``` bash
git log --format=fuller
```

The commit showed:

``` text
Author: root <root@picoctf>
Commit: root <root@picoctf>
```

Update the remote after the instance expired:

``` bash
git remote set-url origin <new_url>
```

Push:

``` bash
git push
```

Final flag:

``` text
picoCTF{1mp3rs0n4t4_g17_345y_05f9a904}
```

## Security Lesson

Never trust client-controlled metadata. Identity must be verified
through authentication, not user-provided fields.

