import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_build_stack.cdk_build_stack_stack import CdkBuildStackStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_build_stack/cdk_build_stack_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkBuildStackStack(app, "cdk-build-stack")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
