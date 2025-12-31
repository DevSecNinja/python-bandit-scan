# Bandit Scan

Run Python [Bandit](https://github.com/PyCQA/bandit) scan on your codebase.

## About

Bandit is a tool designed to find common security issues in Python code. This action will run Bandit on your codebase. The results of the scan will be found under the Security tab of your repository.

### Fork

The fork includes the following new features:

- Allow the use of a bandit config file besides the ini file
- Automatic dependency updates by Renovate

## Usage

To run a bandit scan include a step like this:

```yaml
name: Bandit Security Scanner
on:
  push:
    branches: [ "main" ]
  pull_request:
    # The branches below must be a subset of the branches above
    branches: [ "main" ]
  schedule:
    - cron: '36 6 * * 0'

permissions:
  contents: read

jobs:
  bandit:
    permissions:
      contents: read # for actions/checkout to fetch code
      security-events: write # for github/codeql-action/upload-sarif to upload SARIF results
      #actions: read # only required for a private repository by github/codeql-action/upload-sarif to get the Action run status

    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - name: Bandit Scanner
        uses: DevSecNinja/python-bandit-scan@v1.0.0
        with: # optional arguments
          # exit with 0, even with results found
          exit_zero: true # optional, default is DEFAULT
          # Github token of the repository (automatically created by Github)
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }} # Needed to get PR information.
          # File or directory to run bandit on
          # path: # optional, default is .
          # Report only issues of a given severity level or higher. Can be LOW, MEDIUM or HIGH. Default is UNDEFINED (everything)
          # level: # optional, default is UNDEFINED
          # Report only issues of a given confidence level or higher. Can be LOW, MEDIUM or HIGH. Default is UNDEFINED (everything)
          # confidence: # optional, default is UNDEFINED
          # comma-separated list of paths (glob patterns supported) to exclude from scan (note that these are in addition to the excluded paths provided in the config file) (default: .svn,CVS,.bzr,.hg,.git,__pycache__,.tox,.eggs,*.egg)
          # excluded_paths: # optional, default is DEFAULT
          # comma-separated list of test IDs to skip
          # skips: # optional, default is DEFAULT
          # path to a .bandit file that supplies command line arguments
          # config_path: bandit.yml # Use .bandit file for configuration

```

## Inputs

### `path`

**Optional** The path to run bandit on

**Default** `"."`

### `level`

**Optional** Report only issues of a given severity level or higher. 
Can be LOW, MEDIUM or HIGH. Default is UNDEFINED (everything).

**Default** `"UNDEFINED"`

### `confidence`

**Optional** Report only issues of a given confidence level or higher. 
Can be LOW, MEDIUM or HIGH. Default is UNDEFINED (everything).

**Default** `"UNDEFINED"`

### `excluded_paths`

**Optional** Comma-separated list of paths (glob patterns supported) to exclude from scan 
(note that these are in addition to the excluded paths provided in the config file) (default is from the Bandit itself)

**Default** `".svn,CVS,.bzr,.hg,.git,__pycache__,.tox,.eggs,*.egg"`

### `exit_zero`

**Optional** Exit with 0, even with results found (set `"true"` to use it)

### `skips`

**Optional** Comma-separated list of test IDs to skip

### `ini_path`

**Optional** Path to a .bandit file that supplies command line arguments

### `config_path`

**Optional** Path to a config file (YAML or pyproject.toml) for bandit. 
Use this to specify a bandit.yaml or pyproject.toml configuration file with the `-c` flag.

Example:
```yaml
    uses: DevSecNinja/bandit-action@v1
    with: 
        path: "."
        config_path: "bandit.yaml"
```

## Outputs

The action will create an artifact containing the sarif output.

## Credits

- :bow: This is a fork of [python-bandit-scan](https://github.com/shundor/python-bandit-scan) by [shundor](https://github.com/shundor/).
- :bow: This action is based on [bandit-action](https://github.com/mdegis/bandit-action) by [Melih Değiş](https://github.com/mdegis/).
