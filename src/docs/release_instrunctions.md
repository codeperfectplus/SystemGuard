# SystemGuard Release Guidelines

This document provides instructions for preparing and publishing a new release of SystemGuard.

## Versioning

SystemGuard uses [Semantic Versioning](https://semver.org/) with the format `MAJOR.MINOR.PATCH`:

- **MAJOR**: Increased for changes that break backward compatibility.
- **MINOR**: Increased when new features are added.
- **PATCH**: Increased for bug fixes and minor improvements.

## Release Notes

Update the release notes in the `Release.md` file located in the `docs` directory. Include the following details:

- **Version**: The version number for the release.
- **Release Date**: The date the release is created.
- **Status**: The release status (e.g., Pre-release, Stable, In Testing).
- **Key Features**: Highlight the main features introduced in this release.
- **Changelog**: A summary of changes included in the release.
- **Upgrade Instructions**: Any specific steps or considerations for upgrading.
- **Known Issues**: List any known problems or limitations.

## Release Process

Follow these steps to release SystemGuard:

- **Pre-release Versions**: Use a `-pre` suffix (e.g., `v1.0.4-pre`) for testing releases from the `dev` branch.
- **Stable Versions**: Use a plain version number (e.g., `v1.0.4`) for production releases from the `production` branch.

Before proceeding with a release, ensure the version numbers and flags are correctly set in the `config.py` file.

## Release Checklist

Before creating a new release, make sure the following tasks are completed:

- [ ] Update the version number in the `config.py` file.
- [ ] Add and update release notes in the `Release.md` file.
- [ ] Test the release in a staging environment.
- [ ] Merge changes into the `production` branch.
- [ ] Create a new release on GitHub.
- [ ] Update the website with the new release details.
- [ ] Revise the documentation to reflect the new release.
