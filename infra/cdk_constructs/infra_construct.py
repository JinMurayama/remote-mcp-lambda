"""
Lambdaコンストラクト

Lambda + IAM + CloudWatch Logs の構成を提供するコンストラクト
"""

from aws_cdk import (
    Duration,
    RemovalPolicy,
    CfnOutput,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_logs as logs,
)
from constructs import Construct
from typing import Optional


class LambdaConstruct(Construct):
    """
    Lambda関数のコンストラクト
    
    Lambda + IAM Role + CloudWatch Logs の構成を提供
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        function_name: str,
        handler: str = "lambda_function.lambda_handler",
        runtime: _lambda.Runtime = _lambda.Runtime.PYTHON_3_11,
        code_path: str = "../app/code",
        timeout_seconds: int = 30,
        memory_size: int = 128,
        log_retention_days: logs.RetentionDays = logs.RetentionDays.ONE_WEEK,
        environment_variables: Optional[dict] = None,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # デフォルトの環境変数を設定
        if environment_variables is None:
            environment_variables = {"LOG_LEVEL": "INFO"}

        # Lambda Layer for dependencies (コードベースの場合のみ)
        self.lambda_layer = _lambda.LayerVersion(
            self,
            "McpLambdaLayer",
            code=_lambda.Code.from_asset("../app/layer"),
            compatible_runtimes=[runtime],
            description="MCP Lambda Handler and dependencies",
            layer_version_name=f"{function_name}-dependencies"
        )

        # CloudWatch Logs Group for Lambda
        self.log_group = logs.LogGroup(
            self,
            "LambdaLogGroup",
            log_group_name=f"/aws/lambda/{function_name}",
            retention=log_retention_days,
            removal_policy=RemovalPolicy.DESTROY
        )

        # IAM Role for Lambda
        self.lambda_role = iam.Role(
            self,
            "LambdaExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            description=f"IAM role for {function_name} Lambda function"
        )

        # IAM Policy for Lambda (basic execution + CloudWatch Logs)
        self.lambda_policy = iam.Policy(
            self,
            "LambdaExecutionPolicy",
            statements=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "logs:CreateLogGroup",
                        "logs:CreateLogStream",
                        "logs:PutLogEvents"
                    ],
                    resources=[self.log_group.log_group_arn + ":*"]
                )
            ]
        )

        # Attach policy to role
        self.lambda_role.attach_inline_policy(self.lambda_policy)

        # Lambda Function
        layers = [self.lambda_layer] if self.lambda_layer else []
        self.lambda_function = _lambda.Function(
            self,
            "LambdaFunction",
            runtime=runtime,
            handler=handler,
            code=_lambda.Code.from_asset(code_path),
            role=self.lambda_role,
            function_name=function_name,
            timeout=Duration.seconds(timeout_seconds),
            memory_size=memory_size,
            environment=environment_variables,
            log_group=self.log_group,
            layers=layers
        )

        # Lambda Function URL (HTTPSエンドポイント)
        self.function_url = self.lambda_function.add_function_url(
            auth_type=_lambda.FunctionUrlAuthType.NONE,
            cors=_lambda.FunctionUrlCorsOptions(
                allowed_origins=["*"],
                allowed_methods=[_lambda.HttpMethod.ALL],
                allowed_headers=["*"]
            )
        )

        # 出力値の定義
        CfnOutput(
            self,
            "LambdaFunctionName",
            value=self.lambda_function.function_name,
            description="Lambda function name"
        )

        CfnOutput(
            self,
            "LambdaFunctionArn",
            value=self.lambda_function.function_arn,
            description="Lambda function ARN"
        )

        CfnOutput(
            self,
            "LogGroupName",
            value=self.log_group.log_group_name,
            description="CloudWatch Log Group name"
        )

        CfnOutput(
            self,
            "FunctionUrl",
            value=self.function_url.url,
            description="Lambda Function URL endpoint"
        ) 