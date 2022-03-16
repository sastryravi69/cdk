#!/usr/bin/env python3
import aws_cdk as cdk

# from ul_cdk_stack.ul_cdk_stack_stack import UlCdkStackStack
from ul_cdk_stack.vpcStack import vpcStack
from ul_cdk_stack.ec2Stack import ec2Stack
from ul_cdk_stack.ecsStack import AutoScalingFargateService
from ul_cdk_stack.eipStack import eipStack

app = cdk.App()
envId = app.node.try_get_context(key="config")
envVars = app.node.try_get_context(key=envId)

# Populating env variables
region = envVars["region"]
owner = envVars["account_id"]

env_eu = cdk.Environment(account=owner, region=region)
env_us = cdk.Environment(account=owner, region="us-east-1")
# UlCdkStackStack(app, "UlCdkStackStack")
vpcStack = vpcStack(app, "vpcStack", env=env_us)
if envVars["eipNetworkId"]:
    eipId = envVars["eipNetworkId"]
    eipStack = eipStack(app, "eipAllocation", eipId, env=env_us, allocType="EC2-VPC")
elif envVars["eipInstanceId"]:
    eipId = envVars["eipInstanceId"]
    eipStack = eipStack(app, "eipAllocation", eipId, env=env_us, allocType="EC2")
# ec2 = ec2Stack(app, "ec2Stack", env=env_eu, vpc=vpcStack.vpc)
# ecs = AutoScalingFargateService(app, "AutoScalingFargateService", env=env_eu, vpc=vpcStack.vpc)
app.synth()
