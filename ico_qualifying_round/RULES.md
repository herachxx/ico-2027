# ICO 2027 - Rules & Timeline

So this used to be `rules.txt`, which was literally just me copy-pasting a pile of Telegram announcements from the organizers into one file - three languages, congratulation spam, actual rules, and my own scribbled note all mixed together. It worked as a personal backup, but it's not something you'd want to actually read. This is that same info, same meaning, just sorted into something a human can skim.

(P.S. What's below is a faithful clean-up/translation, not an official document - if anything here ever contradicts what the organizers post directly, believe them, not this file.)

---

## The timeline, at a glance

| Stage | When | Where | Format |
|---|---|---|---|
| Registration | closed Sept 9, 11:30 | `cyberolympiad.kz` | solo sign-up, code below |
| Qualifying round (online) | Sept 9, 12:00 -9 Sept 10, 12:00 | the CTFd-style platform | Jeopardy CTF, solo, 24 hours |
| Results | - | - | top 40 move on |
| Finals (in person) | **Sept 29-30** | Astana, Palace of Independence, KazHackStan conference | 2 days, 3 tasks total |

Categories across both stages: **Web, Crypto, Reverse, Forensics, Pwn** (finals also add a **Misc** bucket).

---

## Qualifying round rules (already happened, keeping for the record)

**Allowed:**
- Any tool you want - internet, docs, AI assistants (ChatGPT, Claude, whatever), no restrictions there at all.
- Attacking the challenges themselves, by any method the challenge's own description allows.
- Messaging organizers if you hit a technical problem with the platform.

**Not allowed:**
- Touching the platform's own infrastructure (`cyberolympiad.kz` itself, including ports 80/443). That's not a challenge, that's just the website - leave it alone.
- Brute-forcing a flag instead of solving for it. Doesn't matter if it would've worked, guessing instead of solving is a violation on its own.
- Sharing flags or solutions with other participants while the round is still live.
- Registering without your name matching the Google Form - auto-disqualified. If you signed up after the form closed, you were supposed to message an organizer directly.

Breaking any of this = instant disqualification, no warning shot.

---

## Finals rules (Sept 29-30, Astana) - the ones that actually matter right now

**Scoring:** 2 tasks on day one, 1 task on day two. Each task is worth 100 points total, broken into subtasks, each subtask has its own flag shaped like `ICO{...}`. Final rank = points from both days added together; ties get broken by whoever landed their last correct flag earliest.

**Equipment:**
- One laptop per person. No second monitor, no phone, no other electronics on the desk.
- No remote or cloud compute - whatever you're running has to run on that one laptop, locally.

**Behavior - the hard bans:**
- Don't discuss any task with anyone except the organizers, through any channel, for any reason.
- Don't attack the competition's own infrastructure, other participants, or anything that isn't explicitly in a task's scope - that includes trying to escape a challenge's Docker container or sandbox.

**The AI policy (read this twice):**
Third-party AI tools are banned outright during the finals - cloud assistants, local models, even the AI autocomplete built into your IDE or browser. The *only* thing you're allowed to use is the competition's own official AI chat, which the organizers said runs on `gpt-5-mini`.

My own note from when I first read this: pretty sure it's `gpt-5-mini` wrapped in some custom front-end specifically so you *can't* upload files through it - just a locked-down chat box. And there's a hard cap of **100,000 tokens a day** on it.

**Recording & audit (this is mandatory, not optional):**
- OBS has to be recording your screen continuously for the *entire* competition day - all ~7 hours, with specific technical settings the organizers laid out.
- You upload a SHA-256 hash of the recording within 30 minutes of the day ending, and the actual recording file by 22:00 that same day.
- No recording = you lose the benefit of the doubt in any dispute. If something looks weird and there's no footage, that's on you.
- Organizers can ask you, at any point, to explain exactly how you got a flag. Be ready to actually explain your own solve path.

---

## Why bother with any of this

Making the national team isn't just a certificate. Per the organizers:
- A year of mentorship from actual infosec people.
- Regular CTF reps - local competitions and international ones.
- Top 4 finishers get a fully-paid trip to **Italy, 2027** (flights + stay covered).
- You end up surrounded by people who are into the same stuff, which honestly matters more than it sounds.

---

## Where to actually train

The organizers dropped this list when the qualifying round was announced - still good advice for finals prep:

| Category | Platform |
|---|---|
| General (all categories) | [TryHackMe](https://tryhackme.com/), [HackTheBox Academy](https://academy.hackthebox.com/), [Root-Me](https://www.root-me.org/) |
| Web | [PortSwigger Web Security Academy](https://portswigger.net/web-security) |
| Crypto | [CryptoHack](https://cryptohack.org/) |
| Pwn | [pwn.college](https://pwn.college/), [OverTheWire: Narnia](https://overthewire.org/wargames/) (start here, it's the beginner one) |
| Reverse | [crackmes.one](https://crackmes.one/) |
| Forensics | [CyberDefenders](https://cyberdefenders.org/) |

---

## The announcement, condensed

Passed the online qualifying round, which is what put me in the pool for the national team selection finals at KazHackStan. The organizers' public posts (Kazakh/Russian/English, all saying basically the same thing) framed it as: talented students from across Kazakhstan competed in a CTF spanning Web, Crypto, Reverse, Forensics, and Pwn, and the strongest performers advance to fight for a spot on the national team representing Kazakhstan internationally. Event: **September 29-30, Astana, Palace of Independence** - `kazhackstan.com`.
