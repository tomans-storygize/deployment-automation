
# pulumi

open source version of hashicorp terraform

extended to support programmatic configs (java supported but this example shows python)

```sh

# internal deployment state is saved in s3 files
pulumi login 's3://tomans-test-bucket?region=us-west-2&awssdk=v2&profile=default'

cd ./web-example
pulumi stack ls
pulumi up # no passphrase on example stack
```
