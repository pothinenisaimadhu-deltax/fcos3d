# DeltaX India project documentation

## Audience and purpose

This guide supports perception engineers, data engineers, researchers and
maintainers preparing a transparent company-managed release. It describes
this checkout, not the entire upstream toolbox.

Start with [installation](installation.md), then [data preparation](data-preparation.md).
Run a smoke check before [training](training.md). Read [evaluation](evaluation.md)
to interpret results, and [troubleshooting](troubleshooting.md) when learning
or alignment is poor. Complete [the publication checklist](publication.md)
before a company release.

## Documentation map

- [Repository handbook and command reference](repository-handbook.md)
- [Complete repository file inventory](file-inventory.md)
- [Installation and compatibility](installation.md)
- [Data preparation and geometry](data-preparation.md)
- [Training, fine-tuning and continuation](training.md)
- [Evaluation and visualization](evaluation.md)
- [Architecture and losses](architecture.md)
- [Validation evidence and reporting](validation.md)
- [Troubleshooting](troubleshooting.md)
- [Company publication](publication.md)

## Support boundaries

Supported training paths are FCOS3D, PGD and the NuScenes MultiViewDfM
adaptation. Custom JSON support is for mono workflows. Custom multi-view data
also requires frame-level GT, calibration and a matching evaluation protocol.

NuScenes detectors consume images only. Standard PKL conversion still uses
sensor calibration, metadata and potentially LiDAR availability/sweep records.
Camera-only model input does not make the converter a generic six-image-folder
importer.

## Source of truth and ownership

The resolved config and local implementation define behavior. Recipe names
such as `1x`, `8xb2` or `1xb1` do not enforce runtime duration or batch size.
Command-line overrides can change both.

The company identity is DeltaX India. Public project URL:
https://github.com/pothinenisaimadhu-deltax/fcos3d.
General support uses this fork's issue tracker. A private security contact and
named release approver still need organizational confirmation.

Legacy `docs/en/` pages remain useful framework references, but are not a
support promise for all upstream architectures.
