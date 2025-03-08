Setting up DNS in AWS using pulumi

https://www.pulumi.com/registry/packages/aws/api-docs/route53/zone/

https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-working-with.html

this example creates a private vpc domain zone and a vpn resolver

- registers a private DNS name for a private EC2 instance

```sh

VPC_ID=$(find-vpc-id "staging")

# pulumi config set k v [--secret]

pulumi stack init staging --secrets-provider "awskms://$DEFAULT_KMS_ALIAS" 

pulumi up

```
