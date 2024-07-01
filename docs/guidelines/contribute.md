# Contribute

Thank you for your interest in contributing to the development of new detectors.

### Getting Started

Create a new issue on our [repository](https://github.com/CoinFabrik/stacy) with the name of the new detector or test case you wish to contribute. Then, link a new branch to that issue.

> :exclamation: **Requirement**: All detectors should follow the CamelCase naming convention.

### Detectors

To contribute a new detector:

1. Browse our templates at [`templates/detectors`](https://github.com/CoinFabrik/stacy/tree/main/templates/detectors) and check the structure your detector should follow. 

2. Add your modified DetectorName.py file inside the [`detectors`](https://github.com/CoinFabrik/stacy/tree/main/src/stacy_analyzer/detectors) directory.

### Test Cases

To contribute a new test case:

1. Create a new folder in the [`tests`](https://github.com/CoinFabrik/stacy/tree/main/tests) directory. **Remember to follow the underscore naming convention for the folder name**.

2. Within this folder, create two directories: `vulnerable-example` and `remediated-example`. Fill each with the relevant files for their respective test cases. 

For guidance, refer to the `detector_name` template in [`templates/test-case`](https://github.com/CoinFabrik/stacy/tree/main/templates/tests).
