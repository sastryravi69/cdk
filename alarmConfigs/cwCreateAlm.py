from constructs import Construct
from aws_cdk import (
    Stack, aws_cloudwatch as cw,
)

# Global Vars. Change this later to a config file

defTh = 100
defEvalPd = 3
defDP2Alm = 2

class cwCreateAlm(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

    # Method for creating Alarm
    def createAlarm(self, alm_name, mt_name) -> None:
        cw.Alarm(self,
                 metric=mt_name,
                 id=alm_name,
                 comparison_operator=cw.ComparisonOperator.LESS_THAN_OR_EQUAL_TO_THRESHOLD,
                 threshold=defTh,
                 evaluation_periods=defEvalPd,
                 datapoints_to_alarm=defDP2Alm
                 )
