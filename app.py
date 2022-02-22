#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cw_mon.cw_mon_stack import CwMonStack  # Default app. DO NOT USE
from lib.cloudWatchMonStack import cloudWatchMonStack
from lib.cwDashBRDS import cwDashbRDS
from lib.cwdashboardLB import cwdashboardLB


app = cdk.App()
cloudWatchMonStack(app, "cloudWatchMonStack")
cwDashbRDS(app, "cwDashbRDS")
cwdashboardLB(app, "cwdashboardLB")
app.synth()
