# monitor-filechanges roadmap

Written 2026-10-30 from the repo as it stands. No dates on the future
items, because I do not know when I will be back in this code, and a
date I invent here would be a small lie in a public file.

## Done

- FileChangeHandler with on_created, on_modified, and on_deleted,
  each logging file and directory events with their paths.
- setup_argparse and main: one directory as a positional argument,
  a --recursive flag, and an optional --logfile that adds a file
  handler beside the console output.
- Directory checking in main: a missing path and a path that is not
  a directory both log an error and exit with status 1.
- The foreground loop with a clean stop: Ctrl+C logs Stopping
  monitoring, then observer.stop and join (the idle busy wait was
  fixed 2026-10-30, so the loop now sleeps a full second between
  checks instead of spinning).
- First version of these visuals.

## Working now

- Nothing in flight. I found no TODO or FIXME notes in the code.
  One honest limit on my own checking: the watchdog package is not
  installed in the sandbox I drew these sheets in, so I read this
  code closely but did not run the monitor there.

## Next

- A first test file for FileChangeHandler. Its three methods take a
  watchdog event and log one line, so a test could feed it fake
  events and check the lines, with no real directory watching at
  all. The repo has no tests today.

## Later

- Nothing honest to put here yet. Move and rename handling is the
  obvious candidate people ask about, but I have not decided to add
  it, and it sits in Not planned below until I do.

## Not planned

- Reading file content. The monitor logs that something changed and
  where; opening the files would make it a different tool.
- Move and rename events as their own event kinds. Watchdog reports
  them in its own shape, and the three handled kinds cover what I
  use this for. If that changes, this section changes first.
- Running as a background service. The foreground run with Ctrl+C
  to stop is the shape I want.
