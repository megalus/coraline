# CHANGELOG


## v1.0.0 (2024-10-09)

### Breaking

* ci!: Add support to 3.13

This is a BREAKING CHANGE commit ([`ead99a2`](https://github.com/megalus/coraline/commit/ead99a22222b391fca2f983f476000707c66edca))


## v0.3.1 (2024-04-22)

### Unknown

* Merge remote-tracking branch 'origin/main' ([`763fbbd`](https://github.com/megalus/coraline/commit/763fbbd325751744cc589bf5b3d64244d60c09ba))


## v0.3.0 (2023-10-03)

### Features

* feat: Add TableClass attribute to Coraline and update Python version

Added a new attribute "TableClass" to Coraline to allow specification of the type of the table when creating it. This improves the flexibility of table creation, allowing users to select the desired TableClass depending on their usage pattern. The Python version constraint was also refined from ">=3.9,<=3.11" to ">3.9,<4" for better compatibility and to limit usage to supported Python versions. Furthermore, the Python version utilised was upgraded from "3.10" to "3.11.4" for improved performance and newer features. ([`1f010a4`](https://github.com/megalus/coraline/commit/1f010a4d7b340e58ba65c55b9b600ba841342664))

### Fixes

* fix: model_config error ([`417c9fe`](https://github.com/megalus/coraline/commit/417c9fe43a736d1997e6e6791ee0831a4e19ccf3))


## v0.2.2 (2023-09-26)

### Unknown

* Merge remote-tracking branch 'origin/main' ([`9cff875`](https://github.com/megalus/coraline/commit/9cff87511949fe0d498babab96cc6561a8816642))


## v0.2.1 (2023-09-26)

### Fixes

* fix: Update Docker port, add tests AWS credentials and rename exception

Changed the port number in docker-compose.yml from 8000 to 8001 to avoid port conflict. AWS credentials were added in the local test cases to ensure proper authentication during testing. The name for the exception 'NotFound' was updated to 'CoralNotFound' to enhance clear identification and minimize mix up with other NotFound exceptions. ([`e565bce`](https://github.com/megalus/coraline/commit/e565bcef49214eac021327f83ba1e1ab9c40f830))

### Unknown

* Merge remote-tracking branch 'origin/main' ([`cfac883`](https://github.com/megalus/coraline/commit/cfac883213b35da9abccf19dfef68676dc32e3d7))


## v0.2.0 (2023-09-25)

### Features

* feat: Update various funcs for lib's improved handling & added table creation protection.

Implemented environmental variable checking to prevent accidental table creations in AWS during unit tests. Particularly, adjusted the client_args configuration to prioritize data from ModelConfig > Coraline Envs > AWS Envs. Further, where a JSON object does not contain an `aws_endpoint_url`, it is now configured to a localized DynamoDB instance.
Added deletion protection to a table during creation, thus protecting from accidental exclusions.

Enhanced _get_client_parameters method to refine how it collects environment data and handle corner cases. Updated the 'save' method to handle fields of NumberSet type correctly.

Extended the library's functionality by introducing the TTLField to handle Time to Live attributes and `_get_table_info` method to retrieve table's details like backups, limits, etc. Updated other methods and tests accordingly to make them compatible with the new changes.

Also, incorporated improvements in handling Python data types and AWS response parsing in various methods. Added tests to verify these changes.

Please note, the library is still in progress and not ready for production use. ([`f35458e`](https://github.com/megalus/coraline/commit/f35458eeda8b46ed6d6a27cb4a801a2d57a9b599))

### Fixes

* fix: add missing import ([`cdd9d37`](https://github.com/megalus/coraline/commit/cdd9d378b4d0450e23c3c5cd4c37598ccb254321))

### Unknown

* Merge remote-tracking branch 'origin/main' ([`4204254`](https://github.com/megalus/coraline/commit/4204254dcd51b9952b5bd6ecb6d059dc6dd220a5))


## v0.1.4 (2023-08-30)

### Unknown

* tests: disallow table creation in AWS during unit tests. ([`93b7593`](https://github.com/megalus/coraline/commit/93b7593b37a501f0beeac32d55cc3a8dc6dbe8a2))

* Merge remote-tracking branch 'origin/main' ([`3d55fed`](https://github.com/megalus/coraline/commit/3d55fedb98bd31a5ad548a79904d95a49336c2cd))


## v0.1.3 (2023-08-30)

### Fixes

* fix: correct table default name. ([`137d9ed`](https://github.com/megalus/coraline/commit/137d9ed6d2c8cf24b585ab1543b23db0c4fa36a8))

### Unknown

* Merge remote-tracking branch 'origin/main' ([`792fa50`](https://github.com/megalus/coraline/commit/792fa50717de79ed4832fc4be750d5045c14818b))


## v0.1.2 (2023-08-30)

### Fixes

* fix: Make boto optional.

This is to avoid issues with AWS Lambda, which already has boto3 installed. ([`0c16092`](https://github.com/megalus/coraline/commit/0c1609295cd8b75455c22fa07c6c565edd648bfe))

### Unknown

* Merge remote-tracking branch 'origin/main' ([`6c5fcc2`](https://github.com/megalus/coraline/commit/6c5fcc21a203e9416e22105582247fe3cf386a3c))


## v0.1.1 (2023-08-30)

### Fixes

* fix: Move mypy-boto3-dynamodb to dev dependencies

This commit moves the mypy-boto3-dynamodb dependency from the main dependencies to dev-dependencies in pyproject.toml file. This resolves the Poetry issue to download all botocore versions to resolve dependencies. ([`5077094`](https://github.com/megalus/coraline/commit/5077094b3a2a58b164304d78c8ed86b606c76bdb))

* fix: error when provisioned throughput is not defined ([`f5dd104`](https://github.com/megalus/coraline/commit/f5dd1049084b1774e7d1fdafd8ae1c087ec7acd7))

### Unknown

* Merge remote-tracking branch 'origin/main' ([`2169725`](https://github.com/megalus/coraline/commit/2169725e04844cedf12c4336e60bf8061fc89ece))


## v0.1.0 (2023-08-30)

### Continuous Integration

* ci: add missing configuration ([`2a5f072`](https://github.com/megalus/coraline/commit/2a5f0720187d2e901bf35d7987f8acd3ecc03280))

### Documentation

* docs: fix typo ([`be9248b`](https://github.com/megalus/coraline/commit/be9248b6e6a32ae8671753656502dca98fd55e9e))

### Features

* feat: first public version ([`9acadaa`](https://github.com/megalus/coraline/commit/9acadaaa88d77229d58ad6171cb1fefd23015109))

### Unknown

* Initial commit ([`3d2be8d`](https://github.com/megalus/coraline/commit/3d2be8dd7a7b801aadebdb29d0584af5507bf68e))
