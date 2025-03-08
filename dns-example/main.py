import json
import os
from pathlib import Path
import mimetypes

import pulumi

from pulumi_aws import route53, ec2, vpc

# https://www.pulumi.com/registry/packages/aws/api-docs/route53/


class PrivateDNSEntry:
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

        # nb: all this code runs within some an aws region!

        # read only access: predefined VPC by name
        self.data_vpc = ec2.get_vpc(
            filters=[
                dict(name="tag:Name", values=[self.env]),
            ]
        )

        # read only access: predefined zone by name
        self.data_tld_zone = route53.get_zone(
            name=self.tld,
        )

        # read only access: predefined ec2 instance by name
        self.data_ec2_instance = ec2.get_instance(
            filters=[
                dict(name="tag:Name", values=[instance_name]),
                dict(name="instance-state-name", values=["running"]),
            ]
        )

        # private DNS is also requiring an inbound DNS resolver for outsiders
        # in order to define an inbound DNS resolver we will need to show it some subnets
        self.data_private_subnets = ec2.get_subnets(
            filters=[
                dict(name="vpc-id", values=[self.data_vpc.id]),
                # using this attr as a proxy for 'Public/Private' tag
                dict(name="map-public-ip-on-launch", values=[False]),
            ]
        )

        assert (
            self.data_ec2_instance.id is not None
        ), "Cannot find required cloud instance!"
        assert self.data_tld_zone.id is not None, "Cannot find required cloud zone!"
        assert self.data_vpc.id is not None, "Cannot find required cloud vpc!"

    def deploy(self) -> None:

        env_zone = f"{self.env}.{self.tld}"
        zone_name = env_zone.replace(".", "-")

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

        vpn_resolver_group_sg_name = f"sec-group-resolver-{zone_name}"

        vpn_resolver_security_group = ec2.SecurityGroup(
            vpn_resolver_group_sg_name,
            name=vpn_resolver_group_sg_name,
            description=f"dns resolver security group for dns in {env_zone}",
            vpc_id=self.data_vpc.id,
            tags={
                "Name": vpn_resolver_group_sg_name,
            },
        )

        ingress_rules = [
            (53, 53, "tcp", "10.0.0.0/16", "dns-tcp"),
            (53, 53, "udp", "10.0.0.0/16", "dns-udp"),
            (443, 443, "tcp", "10.0.0.0/16", "dns-https"),
        ]

        for rule in ingress_rules:
            (from_port, to_port, protocol, cidr, name_part) = rule
            resolver_security_group_ingress_rule = vpc.SecurityGroupIngressRule(
                f"sec-rule-i-{zone_name}-{name_part}",
                security_group_id=vpn_resolver_security_group.id,
                cidr_ipv4=cidr,
                from_port=from_port,
                ip_protocol=protocol,
                to_port=to_port,
            )

        egress_rules = [
            (0, 0, "-1", "0.0.0.0/0", "egress-all"),
        ]

        for rule in egress_rules:
            (from_port, to_port, protocol, cidr, name_part) = rule
            resolver_security_group_egress_rule = vpc.SecurityGroupEgressRule(
                f"sec-rule-e-${zone_name}-{name_part}",
                security_group_id=vpn_resolver_security_group.id,
                cidr_ipv4=cidr,
                ip_protocol=protocol,
                from_port=from_port,
                to_port=to_port,
            )

        vpn_resolver_name = f"dns-resolver-{zone_name}"
        vpn_resolver = route53.ResolverEndpoint(
            vpn_resolver_name,
            name=vpn_resolver_name,
            direction="INBOUND",
            resolver_endpoint_type="IPV4",
            security_group_ids=[vpn_resolver_security_group.id],
            ip_addresses=[
                dict(subnet_id=sg_id) for sg_id in self.data_private_subnets.ids[:2]
            ],
            protocols=[
                "Do53",
                "DoH",
            ],
            tags={
                "Environment": self.env,
            },
        )

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
        pulumi.export("vpc_private_subnets", self.data_private_subnets.ids)
        pulumi.export("vpc_zone_id", private_zone.id)
        pulumi.export("zone_ns_id", zone_delegate_ns_record.id)
        pulumi.export("instance_a_id", instance_a_record.id)
        pulumi.export("resolver_id", vpn_resolver.ip_addresses)
        # raise NotImplementedError("Did you implement this function?")


if __name__ == "__main__":
    PrivateDNSEntry("tomans-playground-server").deploy()
