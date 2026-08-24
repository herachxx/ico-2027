# Linux Fundamentals

Core commands:

## pwd

Shows current directory.

``` bash
pwd
```

## ls

Lists files.

``` bash
ls -la
```

Important flags:

-a hidden files -l detailed information

## cd

Changes directory.

``` bash
cd folder
cd ..
cd ~
```

## permissions

Linux permissions:

r = read w = write x = execute

Example:

    -rwxr-xr--

Owner: rwx

Group: r-x

Others: r--

## chmod

Changes permissions.

Example:

``` bash
chmod 600 secret.txt
```

## Processes

A running program has a PID.

``` bash
ps
```

Current shell:

``` bash
ps -p $$ -o pid,ppid,comm,args
```

## Shell

A shell interprets commands.

Examples:

-   bash
-   zsh

Check:

``` bash
echo $SHELL
```

## PATH

Where the shell searches for programs:

``` bash
echo $PATH
```

## Command discovery

``` bash
which python
command -v python
type python
```

They help determine what command will execute.

