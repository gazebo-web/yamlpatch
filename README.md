# Ignition Robotics

Ignition YAML Patch is a tool that allows patching yaml config files.

## Installation
In order to install Ignition YAML Patch, go to the `Releases` page and download the latest version.

`yamlpatch` needs to be placed in either `/usr/bin`, `/usr/local/bin` or correctly configured through the `PATH` variable.

Ignition YAML Patch was primarily designed to be used in a CI/CD environment, that's why we provide a public
Docker image:

`registry.gitlab.com/ignitionrobotics/web/yamlpatch:latest`

## Usage

Ignition YAML Patch uses a manifest called `yamlpatcher.yaml` that allows configuring what YAML Patch needs to do:

```yaml
base: base.yaml

patches:
- patches/patch.yaml
- patches/patch_2.yaml

output: config.yaml
```

Without this manifest, `yamlpatch` will not run. We suggest including this manifest in your project's root folder.

If everything was properly configured, running `yamlpatch` in your project's root folder will produce the following output file:
`config.yaml` that contains a base config from `base.yaml` but with all the patch files applied from the `patches` list.

Feel free to try out `yamlpatch` with the example provided in this repository.

## Contributing
In order to contribute to Ignition YAML Patch, follow the steps described below:

1. Open an issue where we can discuss your change.
2. Submit a MR once the solution has been discussed.
3. Tag Maintainers for reviews.

## References
Ignition YAML Patch uses [yamlpath](https://github.com/wwkimball/yamlpath) as its core tool for merging yaml files, but it was adapted for our own use cases.

## Licenses
- `yamlpath` by William W. Kimball, Jr. (@wwkimball) - [ISC License](https://github.com/wwkimball/yamlpath/blob/master/LICENSE)
- Ignition YAML Patch by Ignition Robotics - [Apache License](https://gitlab.com/ignitionrobotics/web/yamlpatch/-/blob/main/LICENSE)