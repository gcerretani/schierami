# OpenAI directory submission

A GitHub release, a ChatGPT skill upload, workspace sharing and public plugin
directory approval are different operations. This repository automates only its
own GitHub releases and does not claim an approved public listing.

OpenAI's current submission documentation explicitly supports skills-only plugins.
The submission portal is [platform.openai.com/plugins](https://platform.openai.com/plugins).
At the time this document was checked, a submitter needed an organization role
with **Apps Management: Write** and a verified developer or business identity.
Confirm those requirements in the live portal before submitting.

## Prepare the submission

Use a tested release rather than a ZIP assembled from a working folder. For a
skills-only submission, upload the final skill bundle requested by the portal.
Do not invent an MCP server, authentication flow or external data integration:
Schierami currently has none.

Use [the plugin manifest](../.codex-plugin/plugin.json) as the canonical source for
English listing copy and starter prompts. Use the
[skill icon](../skills/schierami/assets/schierami-icon.svg) where its format is
accepted, and provide the public [privacy](privacy.md), [terms](terms.md) and
[support](support.md) pages. Release notes come from [CHANGELOG.md](../CHANGELOG.md),
not from a separate submission draft.

Before upload, run the automated checks and the relevant
[behavioral scenarios](../evals/README.md), then test the packaged skill in the
target host. Describe calculator coverage and current-data dependencies accurately;
do not claim complete Mantra automation or measured predictive superiority.

OpenAI reviews the draft before publication. Approval status is managed in the
portal; successful GitHub CI or a local skill scan is not directory approval.

Official references checked 2026-09-05:

- [Submit plugins](https://developers.openai.com/plugins/deploy/submission)
- [Package plugins](https://developers.openai.com/plugins/build/plugins)
- [Skills in ChatGPT](https://help.openai.com/en/articles/20001066)
