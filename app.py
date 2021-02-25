#!/usr/bin/env python3

from aws_cdk import core

from ecs_devops_cdk.ecs_devops_cdk_stack import EcsDevopsCdkStack


app = core.App()
EcsDevopsCdkStack(app, "ecs-devops-cdk",  env={
    'account': "**********",
    'region': "us-east-2"
  })

app.synth()
