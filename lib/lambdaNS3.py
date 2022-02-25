from aws_cdk import (
    Stack,
    aws_lambda,
)
from constructs import Construct


class cdkLambdaHandler(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        cdkLambdaFunction = aws_lambda.Function(self, 'cdkLambdaFn',
                                                handler='lambda.handler',
                                                runtime=aws_lambda.Runtime.PYTHON_3_6,
                                                code=aws_lambda.Code.from_asset('./lambda'))
