from aws_cdk import (
    aws_ec2 as ec2,
    Stack, CfnOutput,
)
from constructs import Construct


class eipStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, eipId, **kwargs) -> None:
        super().__init__(scope, construct_id, eipId, **kwargs)
        self.__dict__.update(kwargs)

        # Reading Env vars from Context
        envId = self.node.try_get_context(key="config")
        envVars = self.node.try_get_context(key=envId)

        # Populating env variables
        eipAllocID = envVars["eipAllocId"]
        elacIP = envVars["elasticIP"]
        eipPrivateIp = envVars["eipPrivateIP"]

        # Allocating EIP based on EIP allocation to EC2 or VPC
        if kwargs.values() == 'EC2-VPC':
            ec2.CfnEIPAssociation(self, "EIPAllocation", allocation_id=eipAllocID, eip=elacIP,
                                  network_interface_id=eipId,
                                  private_ip_address=eipPrivateIp)
        elif kwargs.values() == 'EC2':
            ec2.CfnEIPAssociation(self, "EIPAllocation", allocation_id=eipAllocID,
                                  instance_id=eipId,
                                  private_ip_address=eipPrivateIp)
        else:
            raise Exception("CDK deploy missing values")

        CfnOutput(self, "EIPOutput", export_name=elacIP, value=elacIP)
