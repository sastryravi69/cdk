from constructs import Construct
from aws_cdk import (
    Stack, Duration,
    aws_cloudwatch as cw,
)

# Global Vars. Change this later to a config file
RDSNameSpace = 'AWS/RDS'
RDSName = 'testsonarrds'  # Test RDS
DefaultDur = Duration.minutes(5)


class cwDashbRDS(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create dashboard to add details
        cdkDashBrd = cw.Dashboard(self, id='cwRDSDashboardID', dashboard_name='cwRDSDashboard')

        # Create Metric & Widget for EC2 monitoring

        # CPUUtilization
        mtRDSCPUUtil = self.createMetric('CPUUtilization', RDSNameSpace, 'avg', DefaultDur)  # Metric
        widRDSCPUUtil = self.createWidget('CPU Utilization: Average', 'left', mtRDSCPUUtil)  # Widget

        # DatabaseConnections
        mtRDSConn = self.createMetric('DatabaseConnections', RDSNameSpace, 'sum', DefaultDur)  # Metric
        widRDSConn = self.createWidget('DatabaseConnections: Sum', 'right', mtRDSConn)  # Widget

        # FreeStorageSpace
        mtFreeStg = self.createMetric('FreeStorageSpace', RDSNameSpace, 'avg', DefaultDur)  # Metric
        widFreeStg = self.createWidget('FreeStorageSpace: Average', 'left', mtFreeStg)  # Widget

        # FreeableMemory
        mtFreeMem = self.createMetric('FreeableMemory', RDSNameSpace, 'avg', DefaultDur)  # Metric
        widFreeMem = self.createWidget('FreeableMemory: Average', 'right', mtFreeMem)  # Widget

        # ReadLatency
        mtRdLat = self.createMetric('ReadLatency', RDSNameSpace, 'avg', DefaultDur)  # Metric
        widRdLat = self.createWidget('ReadLatency: Average', 'left', mtRdLat)  # Widget

        # ReadThroughput
        mtRdThrput = self.createMetric('ReadThroughput', RDSNameSpace, 'avg', DefaultDur)  # Metric
        widRdThrput = self.createWidget('ReadThroughput: Average', 'left', mtRdThrput)  # Widget

        # ReadIOPS
        mtRdIOPS = self.createMetric('ReadIOPS', RDSNameSpace, 'avg', DefaultDur)  # Metric
        widRdIOPS = self.createWidget('ReadIOPS: Average', 'right', mtRdIOPS)  # Widget

        # WriteLatency
        mtWrtLat = self.createMetric('WriteLatency', RDSNameSpace, 'avg', DefaultDur)  # Metric
        widWrtLat = self.createWidget('WriteLatency: Average', 'left', mtWrtLat)  # Widget

        # WriteThroughput
        mtWrtThrput = self.createMetric('WriteThroughput', RDSNameSpace, 'avg', DefaultDur)  # Metric
        widWrtThrput = self.createWidget('WriteThroughput: Average', 'left', mtWrtThrput)  # Widget

        # WriteIOPS
        mtWrtIOPS = self.createMetric('WriteIOPS', RDSNameSpace, 'avg', DefaultDur)  # Metric
        widWrtIOPS = self.createWidget('WriteIOPS: Average', 'right', mtWrtIOPS)  # Widget

        # Add Widgets to dashboard
        cdkDashBrd.add_widgets(widRDSCPUUtil, widRDSConn, widFreeStg, widFreeMem, widRdLat,
                               widRdThrput, widRdIOPS, widWrtLat, widWrtThrput, widWrtIOPS)

    # Method for creating Metric
    def createMetric(self, mt_name, namespace, stats, duration):
        met = cw.Metric(
            metric_name=mt_name,
            namespace=namespace,
            statistic=stats,
            period=duration,
            dimensions_map=dict(DBInstanceIdentifier=RDSName)
        )
        return met

    # Method for creating widget
    def createWidget(self, title, direction, metric):
        if direction == 'left':
            widget = cw.GraphWidget(title=title, left=[metric])
        else:
            widget = cw.GraphWidget(title=title, right=[metric])

        return widget
