from constructs import Construct
from aws_cdk import (
    Stack, Duration,
    aws_cloudwatch as cw,
)

# Global Vars. Change this later to a config file
NetworkELBNameSpace = 'AWS/NetworkELB'
AppELBNameSpace = 'AWS/ApplicationELB'
DefaultDur = Duration.minutes(5)
LB = 'app/k8s-jenkins-ingress-c2bc5bda47/8858ffa1bb1cbf34'
TG = 'k8s-jenkins-jenkins-8607bbba66'


class cwdashboardLB(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create dashboard to add details
        cdkAppELBDashBrd = cw.Dashboard(self, id='cdkAppELBDbID', dashboard_name='AppELB_Dashboard')

        # Create Metric & Widget for ALB monitoring

        # RequestCountPerTarget
        mtReqCtPerTg = self.createMetric('RequestCountPerTarget', AppELBNameSpace, 'avg', DefaultDur)  # Metric
        widReqCtPerTg = self.createWidget('RequestCountPerTarget : Avg', 'left', mtReqCtPerTg)  # Widget

        # RequestCount
        mtReqCt = self.createMetric('RequestCount', AppELBNameSpace, 'avg', DefaultDur)  # Metric
        widReqCt = self.createWidget('RequestCount : Avg', 'right', mtReqCt)  # Widget

        # TargetResponseTime
        mtTargetResTime = self.createMetric('TargetResponseTime', AppELBNameSpace, 'avg', DefaultDur)  # Metric
        widTargetResTime = self.createWidget('TargetResponseTime : Avg', 'right', mtTargetResTime)  # Widget

        # UnHealthyHostCount
        mtUnHealthyHostCt = self.createMetric('UnHealthyHostCount', AppELBNameSpace, 'avg', DefaultDur)  # Metric
        widUnHealthyHostCt = self.createWidget('UnHealthyHostCount : Avg', 'left', mtUnHealthyHostCt)  # Widget

        # Add Widgets to App ELB dashboard
        cdkAppELBDashBrd.add_widgets(widReqCtPerTg, widReqCt, widTargetResTime, widUnHealthyHostCt)

        # Create dashboard to add details
        cdkNwLBDashBrd = cw.Dashboard(self, id='cdkNwLBDbID', dashboard_name='NwLB_Dashboard')

        # Create Metric & Widget for NW monitoring

        # NewFlowCount_TCP
        mtNewFlowCount_TCP = self.createMetric('NewFlowCount_TCP', NetworkELBNameSpace, 'avg', DefaultDur)  # Metric
        widNewFlowCount_TCP = self.createWidget('NewFlowCount_TCP : Avg', 'left', mtNewFlowCount_TCP)  # Widget

        # ActiveFlowCount_TCP
        mtActiveFlowCount_TCP = self.createMetric('ActiveFlowCount_TCP', NetworkELBNameSpace, 'avg', DefaultDur)  # Metric
        widActiveFlowCount_TCP = self.createWidget('ActiveFlowCount_TCP : Avg', 'right', mtActiveFlowCount_TCP)  # Widget

        # PeakPacketsPerSecond
        mtPeakPacketsPerSecond = self.createMetric('PeakPacketsPerSecond', NetworkELBNameSpace, 'avg', DefaultDur)  # Metric
        widPeakPacketsPerSecond = self.createWidget('PeakPacketsPerSecond : Avg', 'right', mtPeakPacketsPerSecond)  # Widget

        # UnHealthyHostCount
        mtNWLBUnHealthyHostCt = self.createMetric('UnHealthyHostCount', NetworkELBNameSpace, 'avg', DefaultDur)  # Metric
        widNWLBUnHealthyHostCt = self.createWidget('UnHealthyHostCount : Avg', 'left', mtNWLBUnHealthyHostCt)  # Widget

        # HealthyHostCount
        mtNWLBHealthyHostCt = self.createMetric('HealthyHostCount', NetworkELBNameSpace, 'avg', DefaultDur)  # Metric
        widNWLBHealthyHostCt = self.createWidget('HealthyHostCount : Avg', 'left', mtNWLBHealthyHostCt)  # Widget

        # Add Widgets to App ELB dashboard
        cdkNwLBDashBrd.add_widgets(widActiveFlowCount_TCP, widPeakPacketsPerSecond, widNewFlowCount_TCP,
                                   widNWLBHealthyHostCt, widNWLBUnHealthyHostCt)

    # Method for creating Metric
    def createMetric(self, mt_name, namespace, stats, duration):
        met = cw.Metric(
            metric_name=mt_name,
            namespace=namespace,
            statistic=stats,
            period=duration,
            dimensions_map=dict(LoadBalancer=LB, TargetGroup=TG)
        )
        return met

    # Method for creating widget
    def createWidget(self, title, direction, metric):
        if direction == 'left':
            widget = cw.GraphWidget(title=title, left=[metric])
        else:
            widget = cw.GraphWidget(title=title, right=[metric])

        return widget
