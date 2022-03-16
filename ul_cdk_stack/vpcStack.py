from aws_cdk import (
    aws_ec2 as ec2,
    Stack, CfnOutput,
)
from constructs import Construct
from lib import config


class vpcStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Reading Env vars from Context
        envId = self.node.try_get_context(key="config")
        envVars = self.node.try_get_context(key=envId)

        # Populating env variables
        vpc_name = envVars["vpc_name"]
        vpc_cidr = envVars["vpc_cidr"]
        s3_bucket_arn = envVars["s3_arn"]

        # eipAllocID = envVars["eipAllocId"]
        # elacIP = envVars["elasticIP"]
        # eipNId = envVars["eipNetworkId"]
        # eipPrivateIp = envVars["eipPrivateIP"]

        # Create VPC with L1 constructs
        self.vpc = ec2.CfnVPC(
            self, "EKSVpc",
            cidr_block=vpc_cidr,
            enable_dns_support=True,
            enable_dns_hostnames=True,
        )

        # Create subnets with L1 constructs and attach to VPC
        self.subnet_id_to_subnet_map = {}
        self.create_subnets()

        ec2.CfnFlowLog(self, "EKSVpcFlowLog", resource_type="VPC",
                       traffic_type="ALL",
                       resource_id=self.vpc.ref,
                       log_destination_type="s3",
                       log_destination=s3_bucket_arn)

        # Output
        CfnOutput(self, "Output", export_name=vpc_name, value=self.vpc.ref)

    def create_subnets(self):
        """ Create subnets of the VPC """
        for subnet_id, subnet_config in config.SUBNET_CONFIGURATION.items():
            subnet = ec2.CfnSubnet(
                self, subnet_id, vpc_id=self.vpc.ref, cidr_block=subnet_config['cidr_block'],
                availability_zone=subnet_config['availability_zone'],
                map_public_ip_on_launch=subnet_config['map_public_ip_on_launch'],
            )
            self.subnet_id_to_subnet_map[subnet_id] = subnet
