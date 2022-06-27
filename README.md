# cmo-core-version-validator

Read version of [cmo-core](https://github.com/Orfium/cmo-core) library in a specified requirements file or toml file
for a specific commit hash for 2 repositories and check that the version of the source
dependency is lower or equal to the one in the destination repository.


## Description

This action can be used in order to detect and block incompatible code from being deployed in an environment.
The check is built on top of [semantic versioning](https://semver.org/). 
The basic idea behind the comparison is the fact that the `cmo-core` migrations are being executed
during the deployment of the [cmo-configuration](https://github.com/Orfium/cmo-configuration).
That means that it is essential to perform a cross check when new code is to be deployed on any environment
and on any repository that uses the shared database to have a compatible version of cmo-core as a dependency.

The steps followed on the check are the following:

1. Detect cmo-core version of the source repository. That means parsing the dependency from either a pyproject.toml or a requirements.txt file for a given revision of the code.
2. Detect cmo-core version of the cmo-configuration repository yet again for a specific revision.
3. Check that the version in the source repository is lower or equal to the one found in cmo-configuration repository

## Usage

An example usage of the action is the following inside a github workflow:

### Sample Workflow

```yaml
- name: Check cmo core version compatibility
  uses: Orfium/cmo-core-version-validator@main
  with:
    github_access_token: ${{ secrets.ORG_ACCESS_TOKEN }}
    current_repo: "Orfium/cmo-allocation"
    current_hash: "d251bb697005779e9d91c6437b09bf43264b5a3a"
    current_requirements_file: "pyproject.toml"
    current_requirements_file_format: "toml"
    ref_repo: "Orfium/cmo-configuration"
    ref_hash: "0f68c000360525b65312e73ed81aef379fe8f828"
    ref_requirements_file: "requirements/base.txt"
    ref_requirements_file_format: "txt"
```

## Input Variables

| Name                               | Description                                                      | Default |
|------------------------------------|------------------------------------------------------------------|---------|
| `github_access_token`              | An access token for performing requests to Github                | -       |
| `current_repo`                     | The current repository                                           | -       |
| `current_hash`                     | The current hash                                                 | -       |
| `current_requirements_file`        | The path to the current requirements file                        | -       |
| `current_requirements_file_format` | The type of the requirements file. toml or txt are supported     | -       |
| `ref_repo`                         | The reference repository                                         | -       |
| `ref_hash`                         | The reference hash                                               | -       |
| `ref_requirements_file`            | The patch to the reference requirements file                     | -       |
| `ref_requirements_file_format`     | The type of the ref requirements file. toml or txt are supported | -       |