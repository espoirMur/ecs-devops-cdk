from aws_cdk import (core, aws_ecs as ecs, aws_ecr as ecr, aws_ec2 as ec2, aws_iam as iam, aws_logs)


class EcsDevopsCdkStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        ecr_repository = ecr.Repository(self,  
                                        "ecs-devops-repository", 
                                         repository_name="ecs-devops-repository")


        vpc = ec2.Vpc(self,  "ecs-devops-vpc",  max_azs=3)

        cluster = ecs.Cluster(self,  
					  "ecs-devops-cluster", 
					  cluster_name="ecs-devops-cluster",
					  vpc=vpc)
        
        execution_role = iam.Role(self,  
                                  "ecs-devops-execution-role", 
                                  assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"), 
                                  role_name="ecs-devops-execution-role")

        execution_role.add_to_policy(iam.PolicyStatement( effect=iam.Effect.ALLOW, 
                                                            resources=["*"], 
                                                            actions=["ecr:GetAuthorizationToken",  
                                                                     "ecr:BatchCheckLayerAvailability",
                                                                     "ecr:GetDownloadUrlForLayer",  
                                                                     "ecr:BatchGetImage",  
                                                                     "logs:CreateLogStream",  
                                                                     "logs:PutLogEvents"  ]  ))
        task_definition = ecs.FargateTaskDefinition(self,  
                                                    "ecs-devops-task-definition", 
                                                    execution_role=execution_role, 
                                                    family="ecs-devops-task-definition")
        
        container = task_definition.add_container("ecs-devops-sandbox", 
                                                  image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"))
        service = ecs.FargateService(self,  
                                     "ecs-devops-service", 
                                     cluster=cluster, 
                                     task_definition=task_definition, 
                                     service_name="ecs-devops-service")
        
        log_group = aws_logs.LogGroup(self,
                                      "ecs-devops-service-logs-groups",
                                      log_group_name="ecs-devops-service-logs")

