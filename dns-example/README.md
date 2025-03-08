Setting up DNS in AWS using pulumi

https://www.pulumi.com/registry/packages/aws/api-docs/route53/zone/

https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-working-with.html

```sh

VPC_ID=$(find-vpc-id "staging")

# pulumi config set k v [--secret]

pulumi stack init staging --secrets-provider "awskms://$DEFAULT_KMS_ALIAS" 

```

### TODO

we are needing an internal DNS resolver for vpn traffic:

- [security group](https://www.pulumi.com/registry/packages/aws/api-docs/ec2/securitygroup/)
  - ingress: (dns tcp/udp 53) only allows VPN: 10.0.0.0/16
  - egress: -2 from/to 0 cird 0.0.0.0/0
- [inbound resolver](https://www.pulumi.com/registry/packages/aws/api-docs/route53/resolverendpoint/)
  - link above security group, ip_addresses = private subnets in distinct region-zones
