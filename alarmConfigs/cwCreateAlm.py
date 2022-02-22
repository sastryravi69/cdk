from aws_cdk import (
    Stack, aws_cloudwatch as cw,
    aws_cloudwatch_actions as cwa,
    aws_sns as sns
)

# Global Vars. Change this later to a config file
defTh = 100
defEvalPd = 3
defDP2Alm = 2
topicArn = "arn:aws:sns:us-east-1:891440700613:myTestTopic"


class cwCreateAlm(Stack):

    # Method for creating alarm
    def createAlarm(self, alm_name, mt_name) -> None:
        alarm = cw.Alarm(self,
                         metric=mt_name,
                         id=alm_name,
                         comparison_operator=cw.ComparisonOperator.LESS_THAN_OR_EQUAL_TO_THRESHOLD,
                         threshold=defTh,
                         evaluation_periods=defEvalPd,
                         datapoints_to_alarm=defDP2Alm
                         )

        # topic = sns.Topic(self, id="MyTestTopic"+alm_name)
        #
        # alarm.add_alarm_action(
        #     cwa.SnsAction(
        #         topic=topic.from_topic_arn(self, id, topic_arn=topicArn)
        #     )
        # )
