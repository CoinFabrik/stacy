![Tests passing](https://github.com/coinfabrik/stacy/actions/workflows/test.yml/badge.svg)

# STACY - Stacks Static Analyzer for Clarity

Stacy is an open-source static analyzer for Clarity smart contracts. It is intended to assist Clarity smart contract developers and auditors detect common security issues and deviations from best practices. 

This tool will help developers write secure and more robust smart contracts.

## Install

```shell
pip install git+https://github.com/xlittlerag/tree-sitter-clarity
pip install stacy-analyzer
```

## Documentation

- [Vulnerabilities](https://github.com/CoinFabrik/stacy/tree/main/docs/vulnerabilities)
- [Guidelines](https://github.com/CoinFabrik/stacy/tree/main/docs/guidelines)

## Detectors

Severities are based on worst case scenarios and the detector's finding may vary depending on the context.

| Detector ID                                                                                                              | What it Detects                                                                                                                                                                                           | Test Cases                                                                                                                                                                                                                                               | Severity    |
| ------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| [assert-block-height](https://github.com/CoinFabrik/stacy/blob/main/docs/vulnerabilities/1-assert-block-height.md)         | Usage of `block-height` as time tracker.                  | [1](https://github.com/CoinFabrik/stacy/tree/main/tests/assert_block_height) | Critical    |
| [call-inside-as-contract](https://github.com/CoinFabrik/stacy/blob/main/docs/vulnerabilities/2-call-inside-as-contract.md)                           | Calling another contract losing the first contract's context.                                                           | [1](https://github.com/CoinFabrik/stacy/tree/main/tests/call_inside_as_contract)                                                                                                                                                | Critical    |
| [divide-before-multiply](https://github.com/CoinFabrik/stacy/blob/main/docs/vulnerabilities/3-divide-before-multiply.md)                                               | Performing a division operation before a multiplication, leading to loss of precision.                                                                                | [1](https://github.com/CoinFabrik/stacy/tree/main/tests/divide_before_multiply)                                                                             | Critical    |
| [private-function-not-used](https://github.com/CoinFabrik/stacy/blob/main/docs/vulnerabilities/4-private-function-not-used.md)                                          | Dead code(private functions) inside the smart contract.                                                                        | [1](https://github.com/CoinFabrik/stacy/tree/main/tests/private_function_not_used)                                                                                                                                                                  | Enhancement |
| [todo-comment](https://github.com/CoinFabrik/stacy/blob/main/docs/vulnerabilities/5-todo-comment.md)                                          | TODO comments left in the smart contract.                                                                        | [1](https://github.com/CoinFabrik/stacy/tree/main/tests/todo_comment)                                                                                                                                                                  | Enhancement |
| [tx-sender-in-assert](https://github.com/CoinFabrik/stacy/blob/main/docs/vulnerabilities/5-tx-sender-in-assert.md)                                          | Usage of tx-sender in assert is truly intended.                                                                       | [1](https://github.com/CoinFabrik/stacy/tree/main/tests/tx_sender_in_assert)                                                                                                                                                                  | High |
| [unwrap-panic-usage](https://github.com/CoinFabrik/stacy/blob/main/docs/vulnerabilities/6-unwrap-panic-usage.md)                                          | Inappropriate usage of the `unwrap-panic` method, causing unexpected program crashes.                                                                         | [1](https://github.com/CoinFabrik/stacy/tree/main/tests/unwrap_panic_usage)                                                                                                                                                                  | Enhancement |
| [var-could-be-constant](https://github.com/CoinFabrik/stacy/blob/main/docs/vulnerabilities/7-var-could-be-constant.md)                                          | Code that does not change and could be re-define.                                                                         | [1](https://github.com/CoinFabrik/stacy/tree/main/tests/var_could_be_constant)                                                                                                                                                                  | Enhancement |
| [updated-functions](https://github.com/CoinFabrik/stacy/blob/main/docs/vulnerabilities/9-updated-functions.md)                                          | Old functions.                                                                         | [1](https://github.com/CoinFabrik/stacy/tree/main/tests/updated_functions)                                                                                                                                                                  | Enhancement |
| [tx-sender-in-assert](https://github.com/CoinFabrik/stacy/blob/main/docs/vulnerabilities/6-tx-sender-in-assert.md)                                          | Usage of tx-sender in assert is truly intended.                                                                       | [1](https://github.com/CoinFabrik/stacy/tree/main/tests/tx_sender_in_assert)                                                                                                                                                                  | High |
| [unwrap-panic-usage](https://github.com/CoinFabrik/stacy/blob/main/docs/vulnerabilities/7-unwrap-panic-usage.md)                                          | Inappropriate usage of the `unwrap-panic` method, causing unexpected program crashes.                                                                         | [1](https://github.com/CoinFabrik/stacy/tree/main/tests/unwrap_panic_usage)                                                                                                                                                                  | Enhancement |
| [var-could-be-constant](https://github.com/CoinFabrik/stacy/blob/main/docs/vulnerabilities/8-var-could-be-constant.md)                                          | Code that does not change and could be re-define.                                                                         | [1](https://github.com/CoinFabrik/stacy/tree/main/tests/var_could_be_constant)                                                                                                                                                                  | Enhancement |


## About CoinFabrik

We - [CoinFabrik](https://www.coinfabrik.com/) - are a research and development company specialized in Web3, with a strong background in cybersecurity. Founded in 2014, we have worked on over 180 blockchain-related projects, EVM based and also for Solana, Algorand, and Polkadot. Beyond development, we offer security audits through a dedicated in-house team of senior cybersecurity professionals, currently working on code in Substrate, Solidity, Clarity, Rust, and TEAL.

Our team has an academic background in computer science and mathematics, with work experience focused on cybersecurity and software development, including academic publications, patents turned into products, and conference presentations. Furthermore, we have an ongoing collaboration on knowledge transfer and open-source projects with the University of Buenos Aires.

## License


Stacy is licensed and distributed under a MIT license. [Contact us](https://www.coinfabrik.com/) if you're looking for an exception to the terms.
