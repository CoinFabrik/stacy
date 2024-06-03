# Stacks Static Analyzer

## Install

### HTTPS
```shell
git clone --recurse-submodules -j8 https://github.com/CoinFabrik/stacy.git
cd stacy
make
```

### SSH
```shell
git clone --recurse-submodules -j8 git@github.com:CoinFabrik/stacy.git
cd stacy
make
```

If you already have an initialized python venv, use `make install`

If you have a shell other than `bash`, use `make <shell>`

## Run

```shell
stacy-analyzer lint <path/to/.clar>
```

You can run recursively over all `.clar` files in a directory. For this, run

```shell
stacy-analyzer lint <path/to/contract/folder>
```

## Tests

To run tests, run
```shell
make test
```

## Common issues

### `tree-sitter-clar` installation fails
If the installation of `tree-sitter-clar` fails, go into `stacks_analyzer/tree-sitter-clarity` and run

```shell
tree-sitter generate && tree-sitter-build
```

Ensure that the submodule is loaded.
