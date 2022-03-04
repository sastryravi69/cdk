from aws_cdk import (
    Stack, Duration,
    aws_cloudwatch as cw
)
from constructs import Construct
from alarmConfigs.cwCreateAlm import cwCreateAlm

# Global Vars. Change this later to a config file
EC2NameSpace = 'AWS/EC2'
# InsID = 'i-033c064ade62d83c1'  # LQA Nginx
InsID = ['i-033c064ade62d83c1', 'i-05d8b2da7df3c303e', 'i-07e6b5966a210cbbb', 'i-012bdac5624a41fa8',
         'i-0806b344637b3826f']  # LQA Stack
DefaultDur = Duration.minutes(5)


class cloudWatchMonStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        alm = cwCreateAlm()
        # Create dashboard to add details
        cdkDashBrd = cw.Dashboard(self, id='cdkTestDbID', dashboard_name='cdk_test_dashboard',
                                  period_override=cw.PeriodOverride.INHERIT)

        # Create Metric & Widget for EC2 monitoring

        # CPUUtilization
        mtEC2CPUUtil = self.createMetric('CPUUtilization', EC2NameSpace, 'avg', DefaultDur)  # Metric
        alm.createAlarm('CPU Utilization', mtEC2CPUUtil)  # Create Alarm
        widEC2CPUUtil = self.createWidget('CPU Utilization', 'left', mtEC2CPUUtil)  # Widget

        # DiskReadOps
        mtDkRdOp = self.createMetric('DiskReadOps', EC2NameSpace, 'avg', DefaultDur)  # Metric
        alm.createAlarm('DiskReadOps', mtDkRdOp)  # Create Alarm
        widDkRdOp = self.createWidget('Disk Read Ops', 'right', mtDkRdOp)  # Widget

        # DiskWriteOps
        mtDkWtOp = self.createMetric('DiskWriteOps', EC2NameSpace, 'avg', DefaultDur)  # Metric
        widDkWtOp = self.createWidget('Disk Write Ops', 'left', mtDkWtOp)  # Widget

        # StatusCheckFailed_Instance
        mtStCkF_Ins = self.createMetric('StatusCheckFailed_Instance', EC2NameSpace, 'avg', DefaultDur)  # Metric
        widStCkF_Ins = self.createWidget('Instance Check status', 'right', mtStCkF_Ins)  # Widget

        # StatusCheckFailed_System
        mtStCkF_Sys = self.createMetric('StatusCheckFailed_System', EC2NameSpace, 'avg', DefaultDur)  # Metric
        widStCkF_Sys = self.createWidget('System Check status', 'left', mtStCkF_Sys)  # Widget

        # NetworkPacketsIn
        mtNWPktIn = self.createMetric('NetworkPacketsIn', EC2NameSpace, 'avg', DefaultDur)  # Metric
        widNWPktIn = self.createWidget('Network Packet In', 'left', mtNWPktIn)  # Widget

        # NetworkPacketsOut
        mtNWPktOut = self.createMetric('NetworkPacketsIOut', EC2NameSpace, 'avg', DefaultDur)  # Metric
        widNWPktOut = self.createWidget('Network Packet Out', 'right', mtNWPktOut)  # Widget

        # StatusCheckFailed
        mtStCkFail = self.createMetric('StatusCheckFailed', EC2NameSpace, 'avg', DefaultDur)  # Metric
        widStCkFail = self.createWidget('Status Check Failed', 'left', mtStCkFail)  # Widget

        # Add Widgets to dashboard
        cdkDashBrd.add_widgets(widEC2CPUUtil, widDkRdOp, widDkWtOp, widStCkF_Ins, widStCkF_Sys,
                               widNWPktIn, widNWPktOut, widStCkFail)

    # Method for creating Metric
    def createMetric(self, mt_name, namespace, stats, duration):
        met = cw.Metric(
            label=InsID[0]+mt_name,
            metric_name=mt_name,
            namespace=namespace,
            statistic=stats,
            period=duration,
            dimensions_map=dict(InstanceId=InsID[0])
        )

        return met

    # Method for creating widget
    def createWidget(self, title, direction, metric):
        if direction == 'left':
            widget = cw.GraphWidget(title=title, left=[metric])
        else:
            widget = cw.GraphWidget(title=title, right=[metric])

        return widget
