# ICO 2027 CTF Writeups

<p align="center">

International Cybersecurity Olympiad 2027 - Kazakhstan national qualifiers

  <img src="https://img.shields.io/badge/ICO-2027-111827?style=for-the-badge" alt="ICO 2027">
  <img src="https://img.shields.io/badge/Language-English%20%7C%20Russian-7c3aed?style=for-the-badge" alt="English and Russian">
  <img src="https://img.shields.io/badge/CTF-Writeups-2563eb?style=for-the-badge" alt="CTF Writeups">

  ![смишой гиф тепа бибизяна психует кабута я](бибизяна.gif)

</p>

---

## What this repo actually is

This is writeup repo for **ICO 2027** - the International Cybersecurity Olympiad's Kazakhstan national selection.

It's a CTF, run in two stages: an online qualifying round, then an in-person finals at KazHackStan where they pick the actual national team.

I finished the qualifying round 4th place, 10/10 tasks solved. This repo is the full writeup of how - every command, every script, every "wait, why does this work" moment, explained so you don't need to already be a hacker to follow along. Finals haven't happened yet (they're September 29-30, 2026, in Astana), so that folder's still a placeholder for now.

---

## Pew pew

Screenshots from the platform while the round was live (idk why u need this but ok js leave it there)

![Live scoreboard, 4th place](ico_qualifying_round/contest_scoreboard.png)

*Yeah, that's me at 4th!*


![Top 10 users' score progress over the 24 hours](ico_qualifying_round/top_10_users.png)

*Everyone in the top 10, score-over-time.*

---

## Start here

| Round | Status | Writeup |
|---|---:|---|
| ICO 2027 Qualifying Round | Complete, 10/10 tasks solved | [Open full writeup](./ico_qualifying_round/ico_ctf_writeup.md) |
| ICO 2027 Finals | Not happened yet (Sept 29-30, 2026) | [Open finals folder](./ico_finals/) |

Also worth a look: [`ico_qualifying_round/RULES.md`](./ico_qualifying_round/RULES.md) - the actual competition rules and timeline, cleaned up from the organizers' Telegram announcements into something readable. Has the finals AI policy in it too, which matters if you're prepping for one of these.

---

## Qualifying round tasks

| # | Task | Category | Result |
|---:|---|---|---|
| 1 | Rev Zero | Reverse Engineering | Solved |
| 2 | Wolf Protocol | Reverse Engineering | Solved |
| 3 | Can you hear the flag? | Forensics | Solved |
| 4 | Five Shards | Forensics | Solved |
| 5 | NorthStar | Web | Solved |
| 6 | Backdoor | Web | Solved |
| 7 | PixelMart | Crypto / Scripting | Solved |
| 8 | VIP Club | Crypto / Hash Length Extension | Solved |
| 9 | Journal Operator | Pwn | Solved |
| 10 | AEZAKMI | Pwn | Solved |

Full breakdown of each one is in the writeup linked above. The actual downloadable challenge files (binaries, the stego image, the Five Shards bundle, etc.) aren't stored in this repo - see why and where to get them just below.

---

## Where the actual challenge files live

This repo holds the *writeup* - descriptions, code, explanations. The actual files each challenge hands you (binaries, images, a WAV, a pcap, etc.) live in one shared Google Drive folder instead, so the git repo itself stays small and fast to clone:

**[ICO2027 - Google Drive folder](https://drive.google.com/drive/folders/1pKuyT6qqqxKOCK9oq7Dl5VGQzTkIW_ZW)**

The writeup links to that same folder right under each challenge's "Challenge file(s)" line, so you don't have to go hunting - just open the challenge you're reading about and the link's right there.

---

## Notes

Everything in this repository is for educational CTF learning only. The techniques here are explained in the context of a legitimate, sanctioned competition - don't go pointing any of this at systems you don't own or don't have explicit permission to test.
