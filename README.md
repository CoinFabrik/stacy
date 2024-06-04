# STACY - Stacks Static Analyzer for Clarity

`Stacy` is an open-source static analyzer for Clarity smart contracts. It is intended to assist Clarity smart contract developers and auditors detect common security issues and deviations from best practices. 

This tool will help developers write secure and more robust smart contracts.


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

## Documentation


## Detectors

Severities are based on worst case scenarios and the detector's finding may vary depending on the context.

| Detector ID                                                                                                              | What it Detects                                                                                                                                                                                           | Test Cases                                                                                                                                                                                                                                               | Severity    |
| ------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| [assert-block-height](https://github.com/CoinFabrik/stacy/blob/main/docs/vulnerabilities/1-assert-block-height.md)         | Usage of `block-height` as time tracker.                  | [1](https://github.com/CoinFabrik/stacy/tree/main/tests/assert_block_height) | Critical    |
| [set-contract-storage](https://coinfabrik.github.io/scout/docs/detectors/set-contract-storage)                           | [Insufficient access control on set_contract_storage() function.](https://coinfabrik.github.io/scout/docs/vulnerabilities/set-contract-storage)                                                           | [1](https://github.com/CoinFabrik/scout/tree/main/test-cases/set-contract-storage/set-contract-storage-1)                                                                                                                                                | Critical    |
| [reentrancy](https://coinfabrik.github.io/scout/docs/detectors/reentrancy)                                               | [Consistency of contract state under recursive calls.](https://coinfabrik.github.io/scout/docs/vulnerabilities/reentrancy)                                                                                | [1](https://github.com/CoinFabrik/scout/tree/main/test-cases/reentrancy-1/reentrancy-1), [2](https://github.com/CoinFabrik/scout/tree/main/test-cases/reentrancy-1/reentrancy-2), [3](https://github.com/CoinFabrik/scout/tree/main/test-cases/reentrancy-2/reentrancy-1)                                                                             | Critical    |
| [panic-error](https://coinfabrik.github.io/scout/docs/detectors/panic-error)                                          | [Code panics on error instead of using descriptive enum.](https://coinfabrik.github.io/scout/docs/vulnerabilities/panic-error)                                                                         | [1](https://github.com/CoinFabrik/scout/tree/main/test-cases/panic-error/panic-error-1)                                                                                                                                                                  | Enhancement |
## About CoinFabrik

We - [CoinFabrik](https://www.coinfabrik.com/) - are a research and development company specialized in Web3, with a strong background in cybersecurity. Founded in 2014, we have worked on over 180 blockchain-related projects, EVM based and also for Solana, Algorand, and Polkadot. Beyond development, we offer security audits through a dedicated in-house team of senior cybersecurity professionals, currently working on code in Substrate, Solidity, Clarity, Rust, and TEAL.

Our team has an academic background in computer science and mathematics, with work experience focused on cybersecurity and software development, including academic publications, patents turned into products, and conference presentations. Furthermore, we have an ongoing collaboration on knowledge transfer and open-source projects with the University of Buenos Aires.

