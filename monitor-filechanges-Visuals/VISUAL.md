# monitor-filechanges, drawn out

I made these five pictures because the program is a loop, and a loop
is easier to see than to read about. Everything in them comes from
the one file that does the work, main.py: FileChangeHandler,
setup_argparse, and main, built on the watchdog library.

## The visuals

- [architecture.svg](architecture.svg): the watcher in four parts,
  left to right: the run command, the checks in main, the watchdog
  Observer, and FileChangeHandler logging each event.
- [sequence.svg](sequence.svg): one file appearing in the watched
  folder, followed across five actors from the run command to the
  log line.
- [flowchart.svg](flowchart.svg): a run from start to Ctrl+C, with
  the two checks that can end it early and the sleep loop that keeps
  it alive.
- [product-map.svg](product-map.svg): the product in one frame: the
  three event kinds it logs, who it serves, what goes in, what comes
  out, and where it stops.
- [statistics.svg](statistics.svg): the numbers from the table below,
  drawn as bars on paper: lines by kind, with the file and commit
  counts noted under them.

Each sheet also ships as a PNG beside its SVG (architecture.png,
sequence.png, and so on): the same drawing, finished as a photograph
of the paper page.

Every sheet here is drawn to look like what it is: a page sketched by
hand on paper, and each one is signed GK somewhere in the drawing,
never twice in the same place, because that is what I do with a page
I made.

## Written product map

What it is: a foreground monitor for one directory. It uses the
watchdog library to watch for file and directory creation,
modification, and deletion, and logs each event with a timestamp. It
runs until I stop it with Ctrl+C.

Who it serves: me, watching a folder while something else writes
into it, and anyone who wants a plain event log of a directory.

Capabilities, grouped:

- Watching: an Observer from watchdog schedules FileChangeHandler on
  one directory, at the top level only, or through its
  subdirectories when --recursive is set.
- Events: on_created, on_modified, and on_deleted, each logging
  whether the path is a file or a directory, and the path itself.
- Output routing: events always log to the console, and also to a
  file when --logfile names one. Logging stays at INFO level.
- Staying alive honestly: a one second sleep loop in the foreground,
  and on Ctrl+C a Stopping monitoring line, observer.stop, and join.

Inputs: one directory path, plus the optional --recursive and
--logfile flags. Outputs: the timestamped log lines described above.

Boundaries, what it does NOT do: move and rename events are not
handled separately, and file content is never read. A path that does
not exist, or that is not a directory, logs an error and exits with
status 1. One behaviour worth knowing, from the README: creating a
file usually also logs a modification event for the file and one for
its parent directory, because that is how the filesystem
notifications underneath behave.

## Statistics, with citations

Counted 2026-10-30, from the clone this folder ships in, at the
commit before this visuals work (15f1e09).

| Number | Value | How it was counted, and from what |
|---|---|---|
| Files in the repo | 6 | git ls-files in the clone, counted 2026-10-30 |
| Python lines | 103 | Line count over the 1 tracked .py file (main.py), binary and image files excluded, 2026-10-30 |
| Markdown lines | 61 | Line count over the 1 tracked .md file (README.md), same method, 2026-10-30 |
| License text lines | 674 | Line count over the 1 tracked file with no extension (LICENSE), same method, 2026-10-30 |
| Text lines | 1 | Line count over the 1 tracked .txt file (requirements.txt), same method, 2026-10-30 |
| Commits | 7 | git log in the clone, counted 2026-10-30 |
| First commit | 2025-01-02 | git log, oldest entry, 2026-10-30 |
| Last commit before this one | 2026-10-30 | git log, newest entry, 2026-10-30 |
| Tests | 0 test files, no suite to run | File listing of the clone and the README both say there are no bundled tests, counted 2026-10-30. No pass is claimed. The monitor was not run either: the watchdog package is not installed in my sandbox, installs are out of scope for this work, and python3 main.py stops at its import line with ModuleNotFoundError, observed 2026-10-30 |
| Languages (API) | Python 3,163 bytes | GitHub API, GET /repos/ShadowGuard-AI/monitor-filechanges/languages, read 2026-10-30 |
| Repo size (API) | 77 KB | GitHub API, GET /repos/ShadowGuard-AI/monitor-filechanges, size field, read 2026-10-30 |
| Stars / forks (API) | 1 / 0 | Same API response, read 2026-10-30 |

External statistics: none. No outside number says anything honest
about this repo, so the repo's own numbers are the whole table.

## Roadmap summary

Done: the three event handlers, the recursive flag, the optional log
file, and the idle busy wait fixed so the loop sleeps a full second.
Working now: nothing in flight. Next, if I return to it: a first
test file for the handler, fed with fake watchdog events. The full
roadmap, with the Later and Not planned sections, is in
[ROADMAP.md](ROADMAP.md).
