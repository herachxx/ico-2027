# Networking Basics

## IP

Address of a device.

Private ranges:

-   10.x.x.x
-   172.16-31.x.x
-   192.168.x.x

## Ports

Services listen on ports.

Examples:

22 SSH 80 HTTP 443 HTTPS 53 DNS

## DNS

Converts names to IPs.

Tools:

``` bash
nslookup domain
dig domain
```

## SSH

Remote shell:

``` bash
ssh user@host
```

## curl

HTTP requests:

``` bash
curl https://example.com
```

## ss

Network sockets:

``` bash
ss -tulpn
```

