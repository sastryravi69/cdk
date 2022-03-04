from aws_cdk import (
    Stack, Duration,
    aws_cloudwatch as cw
)
from constructs import Construct

# Global Vars. Change this later to a config file
CertificateNameSpace = 'AWS/CertificateManager'
DefaultDur = Duration.days(30)


class cwCert(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create dashboard to add details
        cdkDashBrd = cw.Dashboard(self, id='cdkCertID', dashboard_name='cdk_cert_dashboard', start='-P1W',
                                  period_override=cw.PeriodOverride.INHERIT)

        # crtArn = self.node.try_get_context('certArn')

        cdkDashBrd.add_widgets(cw.GraphWidget(title='Certificate Expiry', left=[cw.Metric(
            label='DaysToExpire',
            metric_name='DaysToExpiry',
            namespace=CertificateNameSpace,
            dimensions_map=dict(
                CertificateArn='arn:aws:acm:eu-west-1:891440700613:certificate/df410350-c706-4965-98ec-542fe8979dc6')
        )]))
