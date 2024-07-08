# Contribute

Thank you for your interest in contributing to the development of new detectors.

### Getting Started

Create a new issue on our [repository](https://github.com/CoinFabrik/stacy) with the name of the new detector or test case you wish to contribute. Then, link a new branch to that issue.

> :exclamation: **Requirement**: All detectors should follow the CamelCase naming convention.

### Detectors

To contribute a new detector:

1. Browse our templates at [`templates/detectors`](https://github.com/CoinFabrik/stacy/tree/main/templates/detectors) and check the structure a new detector should follow. 

2. Add your modified `DetectorName.py` file inside the [`detectors`](https://github.com/CoinFabrik/stacy/tree/main/src/stacy_analyzer/detectors) directory.

3. To check if your detector is working properly, run the following command `pip install . && stacy-analyzer lint <path_to_contract_test.clar>`.

### Test Cases

When you create a new detector, please also add a new test case. To add a new one:

1. Create a new folder in the [`tests`](https://github.com/CoinFabrik/stacy/tree/main/tests) directory. **Remember to follow the snake_case/underscore naming convention for the folder name**.

2. Within this folder, create two directories: `vulnerable-example` and `remediated-example`. Fill each with the relevant files for their respective test cases. 

For guidance, refer to the `detector_name` template in [`templates/test-case`](https://github.com/CoinFabrik/stacy/tree/main/templates/tests).
