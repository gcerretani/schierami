# Releases

## Version and notes

The version in [.codex-plugin/plugin.json](../.codex-plugin/plugin.json) is the
single source of truth. Use `MAJOR.MINOR.PATCH` and a matching `vMAJOR.MINOR.PATCH`
Git tag. During the 0.x phase, document changes to supported contracts explicitly;
do not imply compatibility solely from a version number.

Keep work in `Unreleased` in [CHANGELOG.md](../CHANGELOG.md). To release, move it
under a dated version heading and change the manifest in the same commit.
README describes the product; the changelog describes changes; release notes are
extracted from that version's changelog section.

The 0.1.0 and 0.2.0 entries were reconstructed from source history. Do not backdate
GitHub publication or retag old commits to make those entries appear published.

## Build locally

```sh
python -m unittest discover -s tests -v
python tools/check_project.py
python tools/build_release.py --output dist
```

The builder produces `skill.zip`, `schierami-plugin.zip`, `SHA256SUMS`,
`RELEASE_NOTES.md` and `VERSION`. It sorts entries, fixes ZIP metadata and stores
file contents without compression for byte-identical builds across supported
Python environments. Each ZIP must remain below the project's 25 MB limit.

`skill.zip` contains `schierami/` with the runtime resources, a generated `VERSION`
and a copy of the root MIT license. The plugin archive contains the manifest,
`skills/schierami/` with those same resources, and the root MIT license. No tests,
maintainer documentation, build scripts, caches or private profiles are included.
Do not commit generated archives to Git; distribute them as release assets.

## Publish on GitHub

The release workflow runs after checks on pushes to `main`. For the manifest's
current version it either publishes the missing release or leaves an existing
published release untouched. A draft for the same tested commit can be completed;
a tag or draft pointing elsewhere is treated as an error rather than moved.

The workflow uses the repository's `GITHUB_TOKEN`, with `contents: write` only for
the release job. It does not publish from pull requests or forks and does not need
a personal token. CI uses read-only permissions. Repository policies can still
prevent publication; do not weaken them automatically.

After publishing, verify the tag's commit, notes, all three downloadable assets
and the Latest marker. Corrections to published artifacts require a new patch
version rather than overwriting history.

GitHub publication does not install the skill or submit it to OpenAI. Follow
[the separate submission checklist](submission.md) for public directory review.

Primary references: [GitHub release creation](https://cli.github.com/manual/gh_release_create)
and [editing drafts](https://cli.github.com/manual/gh_release_edit).
