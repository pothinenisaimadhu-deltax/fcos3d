# Contributing to the DeltaX India fork

Contribute to [this repository](https://github.com/pothinenisaimadhu-deltax/fcos3d),
not the upstream issue tracker, unless the problem is independently reproduced
upstream. Read [the project guides](docs/project/index.md) first.

## Changes and review

Keep patches scoped and explain their purpose. Preserve existing mono behavior
when extending MV support. Prefer opt-in registrations/adapters to broad changes
in shared geometry, coders or metrics. Describe any compatibility impact and
provide migration instructions. Do not silently change class order, units,
coordinate frames, checkpoint semantics or evaluation splits.

Use the repository's existing formatting/lint conventions. Add regression tests
for changed behavior and update commands/documentation together. For geometry
changes test transformations, pairing and inverse conversions; for velocity
changes test finite targets, gradients and 9D decoding in both train and predict.
See [validation](docs/project/validation.md) for focused commands.

## Evidence required in a pull request

- Problem, implementation and affected workflows.
- Test commands, environment and actual results, including skipped CUDA tests.
- Data/geometry or checkpoint compatibility implications.
- Documentation updates and known limitations.
- For accuracy claims, a reproducible protocol and comparable baselines, not
  only a lower training loss or successful smoke run.

Do not commit proprietary data, model weights, private paths or credentials.
Use only permitted minimal fixtures; do not ask maintainers to load untrusted
pickle/checkpoint attachments. Preserve upstream attribution and license headers.
Company maintainers must confirm redistribution rights and release approval.

General bugs may use GitHub issues. A private security-reporting contact still
needs organizational confirmation; do not disclose sensitive vulnerabilities
publicly while that channel is unresolved.
