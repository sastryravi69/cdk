from aws_cdk import (
    aws_ec2 as ec2,)

# basic VPC configs
VPC = 'custom-vpc'

INTERNET_GATEWAY = 'internet-gateway'

KEY_PAIR_NAME = 'us-east-1-key'

REGION = 'us-east-1'

# route tables
PUBLIC_ROUTE_TABLE = 'public-route-table'

ROUTE_TABLES_ID_TO_ROUTES_MAP = {
    PUBLIC_ROUTE_TABLE: [
        {
            'destination_cidr_block': '0.0.0.0/0',
            'gateway_id': INTERNET_GATEWAY,
            'router_type': ec2.RouterType.GATEWAY
        }
    ],
}

# security groups
SECURITY_GROUP = 'wordpress'

SECURITY_GROUP_ID_TO_CONFIG = {
    SECURITY_GROUP: {
        'group_description': 'SG of the Wordpress servers',
        'group_name': SECURITY_GROUP,
        'security_group_ingress': [
            ec2.CfnSecurityGroup.IngressProperty(
                ip_protocol='TCP', cidr_ip='0.0.0.0/0', from_port=80, to_port=80
            ),
            ec2.CfnSecurityGroup.IngressProperty(
                ip_protocol='TCP', cidr_ipv6='::/0', from_port=80, to_port=80
            ),
            ec2.CfnSecurityGroup.IngressProperty(
                ip_protocol='TCP', cidr_ip='0.0.0.0/0', from_port=443, to_port=443
            ),
            ec2.CfnSecurityGroup.IngressProperty(
                ip_protocol='TCP', cidr_ipv6='::/0', from_port=443, to_port=443
            ),
            ec2.CfnSecurityGroup.IngressProperty(
                ip_protocol='TCP', cidr_ip='0.0.0.0/0', from_port=22, to_port=22
            ),
            ec2.CfnSecurityGroup.IngressProperty(
                ip_protocol='TCP', cidr_ipv6='::/0', from_port=22, to_port=22
            ),
        ],
        'tags': [{'key': 'Name', 'value': SECURITY_GROUP}]
    },
}

# subnets and instances
PUBLIC_SUBNET_EUWEST1A = 'public-subnet-eu-west-1a'
PUBLIC_SUBNET_EUWEST1B = 'public-subnet-eu-west-1b'
PUBLIC_SUBNET_EUWEST1C = 'public-subnet-eu-west-1c'

PRIVATE_SUBNET_EUWEST1A = 'private-subnet-eu-west-1a'
PRIVATE_SUBNET_EUWEST1B = 'private-subnet-eu-west-1b'
PRIVATE_SUBNET_EUWEST1C = 'private-subnet-eu-west-1c'

PUBLIC_INSTANCE = 'public-instance'
PRIVATE_INSTANCE = 'private-instance'

# AMI ID of the WordPress by Bitnami
AMI = 'ami-0c00935023a833df1'

SUBNET_CONFIGURATION = {
    PUBLIC_SUBNET_EUWEST1A: {
        'availability_zone': 'us-east-1a', 'cidr_block': '172.168.1.0/24', 'map_public_ip_on_launch': True,
    },
    PUBLIC_SUBNET_EUWEST1B: {
        'availability_zone': 'us-east-1b', 'cidr_block': '172.168.2.0/24', 'map_public_ip_on_launch': True,
    },
    PUBLIC_SUBNET_EUWEST1C: {
        'availability_zone': 'us-east-1b', 'cidr_block': '172.168.3.0/24', 'map_public_ip_on_launch': True,
    },
    PRIVATE_SUBNET_EUWEST1A: {
        'availability_zone': 'us-east-1a', 'cidr_block': '172.168.4.0/24', 'map_public_ip_on_launch': False,
    },
    PRIVATE_SUBNET_EUWEST1B: {
        'availability_zone': 'us-east-1b', 'cidr_block': '172.168.5.0/24', 'map_public_ip_on_launch': False,
    },
    PRIVATE_SUBNET_EUWEST1C: {
        'availability_zone': 'us-east-1c', 'cidr_block': '172.168.6.0/24', 'map_public_ip_on_launch': False,
    },
}
