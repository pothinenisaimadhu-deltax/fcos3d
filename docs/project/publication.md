# Company publication and release checklist

## Identity and ownership

The public identity supplied for this fork is **DeltaX India** and its repository
is [pothinenisaimadhu-deltax/fcos3d](https://github.com/pothinenisaimadhu-deltax/fcos3d).
That branding does not establish a legal copyright transfer or approval to
redistribute datasets and model weights. Obtain the organization's release
approval before pushing or publishing. This documentation change does not
publish a release or perform a complete legal/security review.

General support is the fork's GitHub issue tracker. Assign a release owner,
maintenance policy and private security-reporting contact before release.
Do not put undisclosed vulnerabilities or confidential data in public issues.

## Preserve provenance

- Retain [LICENSE](../../LICENSE), original source headers and
  [CITATION.cff](../../CITATION.cff). Do not replace OpenMMLab attribution with
  a claim that DeltaX invented FCOS3D, PGD or the framework.
- Identify fork-specific adapters, checks and velocity integration separately
  from upstream algorithms. Record the upstream revision where available.
- Review applicable license/NOTICE obligations and any added third-party code
  with the responsible company reviewer. Dependency, dataset and checkpoint
  terms are separate from this source license.
- The Python package remains mmdet3d and inherited packaging metadata remains
  upstream-oriented. Review distribution naming and metadata deliberately
  before publishing a package; documentation branding is not a package rename.

Primary references used for these guides:

| Source | Purpose |
| --- | --- |
| [MMDetection3D repository](https://github.com/open-mmlab/mmdetection3d) | Framework provenance and original model recipes |
| [Upstream installation](https://mmdetection3d.readthedocs.io/en/latest/get_started.html) | Dependency/build context, subject to this fork's local bounds |
| [Upstream configuration guide](https://mmdetection3d.readthedocs.io/en/latest/user_guides/config.html) | Config inheritance and entry-point conventions |
| [nuScenes detection specification](https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/eval/detection/README.md) | Benchmark metric definitions |

The local code and resolved config define this fork's actual behavior. These
guides are original project documentation informed by primary references, not
a copy of upstream's entire manual or performance claims.

## Data, privacy and repository hygiene

Before publication inspect tracked files **and history** for credentials,
internal paths, employee names, customer information, vehicle identifiers,
private logs and prohibited footage. Ignore rules do not remove already tracked
files or history. Do not rewrite shared history without an approved plan.

Exclude proprietary PKLs, datasets, checkpoints and generated results unless
explicitly approved for redistribution. Use a permitted, de-identified small
example if necessary. Pickle/checkpoint loading can execute code; accept only
trusted artifacts. Preserve a manifest and checksums for approved release assets.

Do not imply that all legacy documentation or inherited config defaults are
sanitized. Some mono recipes still require machine-specific path overrides.
Review remaining docs, diagrams and binary office documents separately; the
project guides are the authoritative supported workflow.

## Technical release gates

- Run focused regression tests and record pass/skip/failure counts and environment.
- Run the real-data CUDA smoke check with permitted data.
- Verify full-grid training and validation independently of the small smoke grid.
- Confirm Mini/trainval version, six-camera pairing, box conventions and official
  evaluation token coverage. Inspect GT projection visually.
- Evaluate a trained checkpoint and report the full protocol; never market a
  random-init smoke score as trained accuracy.
- Record resolved config, commit, seed, initialization, dataset provenance,
  checkpoint selection and limitations for every advertised result.
- Review inherited CI/docs deployment settings and organization permissions
  before enabling deployment. No CI badge should imply an unexecuted test.
- Build the documentation site in its intended environment; local Markdown
  link checks do not substitute for a Sphinx build or hosted-site verification.

See [validation](validation.md) for current focused evidence and remaining work.
Historical scores from different class subsets, datasets and checkpoints must
remain separate; no consolidated company benchmark is established here.

## Release notes template

Record: release/tag and commit; supported workflows; integration changes;
breaking changes; environment; tests performed; dataset/evaluation protocol;
approved asset locations/checksums; known limitations; upgrade instructions;
maintainer and support route. Label unfinished improvements as planned work.

Do not deploy this research fork directly as a safety-critical driving system.
Release documentation should communicate both capability and uncertainty.
