from aws_cdk import (
    Stack, Duration,
    aws_lambda as _lambda,
    aws_sns as sns,
    aws_sqs as sqs,
    aws_sns_subscriptions as sns_subs,
)
from constructs import Construct


class cdkLambdaHandler(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        upload_queue = sqs.Queue(
            self,
            id="sample_queue_id",
            visibility_timeout=Duration.seconds(30),
        )

        sqs_subscription = sns_subs.SqsSubscription(
            upload_queue,
            raw_message_delivery=True
        )

        upload_event_topic = sns.Topic(
            self,
            id="sample_sns_topic_id"
        )
        # This binds the SNS Topic to the SQS Queue
        upload_event_topic.add_subscription(sqs_subscription)

        # cdkLambdaFunction = _lambda.Function(self, 'cdkLambdaFn',
        #                                      runtime=_lambda.Runtime.PYTHON_3_6,
        #                                      handler='lambda.handler',
        #                                      code=_lambda.Code.from_asset('./lambda'))

