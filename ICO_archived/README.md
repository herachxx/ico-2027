# ICO 2026 - Archived Platform Dump

Heads up: this folder is different from the rest of the repo. Everything else in `ico-2027` is *my own* writeup of *this year's* (2027) qualifying round. This folder is a snapshot of **last year's** competition platform - ICO 2026, run on the "CybersecNatLab CTF Platform" - kept around as training/reference material, not something I personally solved or wrote up.

## What's in here (locally)

```text
ICO_archived/
├── README.md                                             → this file
├── ICO 2026 - Rules.pdf                                  → last year's official rules doc
└── tasks/
    ├── Challenges - ICO - CybersecNatLab CTF Platform.pdf  → the full 2026 challenge list
    └── *.png                                                → per-challenge screenshots from the platform
```

Just descriptions and reference docs - nothing huge, nothing that needs special handling to push.

## The actual challenge files live on Google Drive instead

The real downloadable files for each 2026 challenge - zips, tar.gz archives, pcaps, a couple of standalone binaries, Python/PowerShell scripts, `.aethmap` files (a custom format used by the "Aetheria" themed challenge set on that platform) - used to sit in a local `tasks/files/` folder here. Two of them (`new_setup_same_problems.7z` at 4.4GB and `in_memory_of_it_all.7z` at 703MB) are way past GitHub's hard 100MB-per-file push limit, so keeping any of it in git directly was never going to work cleanly.

Instead, all of it now lives here:

**[ICO2027 - Google Drive folder](https://drive.google.com/drive/folders/1pKuyT6qqqxKOCK9oq7Dl5VGQzTkIW_ZW)**

That keeps this repo itself small and fast to clone, while the actual files are still one click away.

## Worth knowing

- **The Drive link only works for people it's shared with.** If this repo is public, double check the Drive folder's sharing setting is "Anyone with the link → Viewer" - otherwise anyone reading this README hits a permission wall.
- **A Drive link isn't as permanent as a committed file.** If the folder gets renamed, moved, or the owning account changes, this link breaks and nobody maintaining this repo may notice right away. Worth an occasional check that it still resolves.
- **This is last year's organizers' archive, not something I personally authored** - unlike the rest of this repo, which is my own writeup of challenges I solved myself. Worth keeping in mind if this repo is public: redistributing someone else's full competition archive (even via a Drive link instead of git) is a different thing than sharing your own writeup of challenges you solved. Not a blocker, just flagging it so it's a conscious call.
