# Addon-Template

This repository is a starter template for creating your own addons. It is meant to provide a basic file structure and release workflow so you can build and publish your addon quickly.

## How to use this template

1. Fork or copy this repository.
2. Replace the placeholder values in `author.json` with your addon information.
3. Update the addon name in `.github/workflow/release.yml`.
4. Build your addon logic in the included files.
5. Commit your changes and create a release using the required tag pattern.

## Required config changes

### Update `author.json`

Edit `author.json` and replace the default values with your own addon details.

Example:

```json
{
  "author": "YourName",
  "name": "MyAddon",
  "version": "1.0.0",
  "description": "A custom addon"
}
```

Important: change the values to match your addon. This metadata is used by the project and may also be included in the release package.

### Update release workflow name

Open `.github/workflow/release.yml` and change the words CHANGE ME!!!! to your addon name on line 49.


Example:

```yaml
name: CHANGE ME!!!! ${{ steps.version.outputs.tag }}


```

becomes

```yaml
name: MyAddon ${{ steps.version.outputs.tag }}
```

This ensures the GitHub Actions release job uses your addon name instead of the template placeholder.

## Creating a release

To trigger the release pipeline, use a commit message in this format:

```bash
Bump vX.Y.Z
```

Example:

```bash
Bump v1.2.3
```

This commit message is used to trigger the release workflow. The workflow grabs the addon that is zippped  containing put the zip in the Release folder:

- `_init_.py`
- `author.json`
- `server.py`

The generated release zip is intended to be the distributable addon package.

## Example settings page

T

This is just a sample structure to show how a settings interface could be built. Replace it with your actual addon settings and UI logic as needed.

## Notes

- This repository is a template and file structure example only.
- Add your own logic, modules, and configuration as needed.
- Keep `author.json`, `_init_.py`, and `server.py` aligned with your addon version and metadata.

## Recommended release flow

1. Edit `author.json`.
2. Edit the name in `.github/workflow/release.yml`.
3. Update your addon code.
4. zip the addon files and place them in the Release folder.
5. commit your changes with a message like `Bump vX.Y.Z` where `X.Y.Z` is your new version.
