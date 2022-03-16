from aws_cdk import (
    aws_autoscaling as autoscaling,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    CfnOutput, Stack
)
from constructs import Construct


class ec2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Reading Env vars from Context
        envId = self.node.try_get_context(key="config")
        envVars = self.node.try_get_context(key=envId)

        # Populating env variables
        ec2_type = envVars["vpc_name"]
        linux_ami_name = envVars["linux_ami_name"]
        key_name = envVars["key_name"]
        owner = envVars["account_id"]

        # Create ALB
        alb = elbv2.ApplicationLoadBalancer(self, "myALB",
                                            vpc=vpc,
                                            internet_facing=True,
                                            load_balancer_name="myALB"
                                            )
        alb.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80), "Internet access ALB 80")
        listener = alb.add_listener("my80",
                                    port=80,
                                    open=True)

        # Create Autoscaling Group with fixed 2*EC2 hosts
        self.asg = autoscaling.AutoScalingGroup(self, "myASG",
                                                vpc=vpc,
                                                vpc_subnets=ec2.SubnetSelection(
                                                    subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT),
                                                instance_type=ec2.InstanceType(instance_type_identifier=ec2_type),
                                                machine_image=ec2.LookupMachineImage(name=linux_ami_name,
                                                                                     owners=[owner]),
                                                key_name=key_name,
                                                desired_capacity=1,
                                                min_capacity=1,
                                                max_capacity=1,
                                                block_devices=[
                                                    autoscaling.BlockDevice(
                                                        device_name="/dev/xvda",
                                                        volume=autoscaling.BlockDeviceVolume.ebs(
                                                            volume_type=autoscaling.EbsDeviceVolumeType.GP2,
                                                            volume_size=12,
                                                            delete_on_termination=True
                                                        )),
                                                    autoscaling.BlockDevice(
                                                        device_name="/dev/sdb",
                                                        volume=autoscaling.BlockDeviceVolume.ebs(
                                                            volume_size=20)
                                                        # 20GB, with default volume_type gp2
                                                    )
                                                ]
                                                )

        self.asg.connections.allow_from(alb, ec2.Port.tcp(80), "ALB access 80 port of EC2 in Autoscaling Group")
        listener.add_targets("addTargetGroup",
                             port=80,
                             targets=[self.asg])

        CfnOutput(self, "Output",
                  value=alb.load_balancer_dns_name)
