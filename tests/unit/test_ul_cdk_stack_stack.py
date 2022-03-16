import aws_cdk as core
import aws_cdk.assertions as assertions

from ul_cdk_stack.ul_cdk_stack_stack import UlCdkStackStack

# example tests. To run these tests, uncomment this file along with the example
# resource in ul_cdk_stack/ul_cdk_stack_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = UlCdkStackStack(app, "ul-cdk-stack")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
