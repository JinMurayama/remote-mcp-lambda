from aws_cdk import Stack
from constructs import Construct
from cdk_constructs.infra_construct import LambdaConstruct


class InfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda Construct を使用してLambda関数を作成
        self.lambda_construct = LambdaConstruct(
            self,
            "RemoteMcpLambdaConstructCode",
            function_name="mcp-server-code",
            handler="lambda_function.lambda_handler",
            timeout_seconds=30,
            memory_size=128
        )