
[packer](https://developer.hashicorp.com/packer/docs/intro) is a tool to define machine images

(usually that is meaning for the cloud hypervisor)

this example shows how to automatically create an AMI using AWS

```sh
REGION="us-west-2"
VPC_ID=$(find-vpc-id "staging")
SUBNET_ID=$(find-subnet-id "staging-priv-apps-b" $VPC_ID)

packer build \
  -var region=$REGION \
  -var vpc_id=$VPC_ID \
  -var subnet_id=$SUBNET_ID \
  aws-ubuntu.pkr.hcl
```
