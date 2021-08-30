# Ignition Robotics

YAML Patch is a tool that allows patching yaml config files.

## Installation
In order to install YAML Patch, go to the [Releases](https://gitlab.com/ignitionrobotics/web/yamlpatch/-/releases) page and download the latest version.

`yamlpatch` needs to be placed in either `/usr/bin`, `/usr/local/bin` or correctly configured through the `PATH` variable.

YAML Patch was primarily designed to be used in a CI/CD environment, that's why we provide a public
Docker image:

`registry.gitlab.com/ignitionrobotics/web/yamlpatch:latest`

## Usage

YAML Patch uses a manifest called `yamlpatcher.yaml` that allows configuring what YAML Patch needs to do:

```yaml
base: base.yaml

patches:
- patches/patch.yaml
- patches/patch_2.yaml

output: config.yaml
```

If everything was properly configured, running `yamlpatch` in your project's root folder will produce the following output file:
`config.yaml` that contains a base config from `base.yaml` but with all the patch files applied from the `patches` list.

Without this manifest, `yamlpatch` will not run. We suggest including this manifest in your project's root folder.

Feel free to try out `yamlpatch` with the example provided in this repository.

```shell
cd ./examples/local
yamlpatch
```

## Contributing
In order to contribute to YAML Patch, follow the steps described below:

1. Open an issue where we can discuss your change.
2. Submit a MR once the solution has been discussed.
3. Tag Maintainers for reviews.

## References
YAML Patch uses [yamlpath](https://github.com/wwkimball/yamlpath) as its core tool for merging yaml files, we built our tool on top of it.

## Licenses
- `yamlpath` by William W. Kimball, Jr. (@wwkimball) - [ISC License](https://github.com/wwkimball/yamlpath/blob/master/LICENSE)
- YAML Patch by Ignition Robotics - [Apache License](https://gitlab.com/ignitionrobotics/web/yamlpatch/-/blob/main/LICENSE)