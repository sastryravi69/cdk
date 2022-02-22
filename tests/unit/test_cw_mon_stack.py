import aws_cdk as core
import aws_cdk.assertions as assertions

from cw_mon.cw_mon_stack import CwMonStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cw_mon/cw_mon_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CwMonStack(app, "cw-mon")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
