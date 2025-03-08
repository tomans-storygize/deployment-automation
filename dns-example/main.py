import json
import os
from pathlib import Path
import mimetypes

import pulumi

from pulumi_aws import route53, ec2

# https://www.pulumi.com/registry/packages/aws/api-docs/route53/


class DNSEntry:
    """

    Just an example of registering a DNS entry using AWS

    """

    def __init__(self, instance_name: str):
        self.instance_name = instance_name

        config = pulumi.Config()
        self.tld = config.require("tld")
        self.env = config.require("vpc_name")

        assert self.env is not None, "vpc_name must be set"
        assert self.tld is not None, "tld must be set"

        self.data_vpc = ec2.get_vpc(
            filters=[
                dict(name="tag:Name", values=[self.env]),
            ]
        )

        self.data_tld_zone = route53.get_zone(
            name=self.tld,
        )

        self.data_ec2_instance = ec2.get_instance(
            filters=[
                dict(name="tag:Name", values=[instance_name]),
                dict(name="instance-state-name", values=["running"]),
            ]
        )

        assert (
            self.data_ec2_instance.id is not None
        ), "Cannot find required cloud instance!"
        assert self.data_tld_zone.id is not None, "Cannot find required cloud zone!"
        assert self.data_vpc.id is not None, "Cannot find required cloud vpc!"

    def deploy(self) -> None:

        env_zone = f"{self.env}.{self.tld}"

        # nb: this block of code is managing this route53 zone!
        private_zone = route53.Zone(
            f"route53-private-dns-zone-{env_zone}",
            name=env_zone,
            vpcs=[{"vpc_id": self.data_vpc.id}],
        )

        # nb: this block of code is managing this route53 NS record!
        zone_delegate_ns_record = route53.Record(
            f"route53-ns-{env_zone}",
            type="NS",
            ttl=300,
            name=env_zone,
            zone_id=self.data_tld_zone.id,
            records=private_zone.name_servers,
        )

        instance_dns = f"{self.instance_name}.{env_zone}"

        # nb: this block of code is managing this route53 A record!
        instance_a_record = route53.Record(
            f"route53-a-{instance_dns}",
            type="A",
            ttl=300,
            name=instance_dns,
            zone_id=private_zone.id,
            records=[self.data_ec2_instance.private_ip],
        )

        pulumi.export("instance_id", self.data_ec2_instance.id)
        pulumi.export("tld_zone_id", self.data_tld_zone.id)
        pulumi.export("vpc_id", self.data_vpc.id)
        pulumi.export("vpc_zone_id", private_zone.id)
        pulumi.export("zone_ns_id", zone_delegate_ns_record.id)
        pulumi.export("instance_a_id", instance_a_record.id)
        # raise NotImplementedError("Did you implement this function?")


if __name__ == "__main__":
    DNSEntry("tomans-playground-server").deploy()
