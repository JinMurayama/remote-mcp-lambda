import json
import logging
from awslabs.mcp_lambda_handler import MCPLambdaHandler
import pytz
from datetime import datetime

# ログレベルの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MCPハンドラーの初期化
mcp = MCPLambdaHandler(name="custom-connector", version="1.0.0")

@mcp.tool()
def hello_world(name: str = "World") -> str:
    """挨拶を返すシンプルなツール"""
    return f"Hello, {name}! これはカスタムコネクトからのメッセージです。"

@mcp.tool()
def get_current_time() -> str:
    """現在時刻を取得するツール"""
    jst = pytz.timezone('Asia/Tokyo')
    now = datetime.now(jst)
    return f"現在時刻: {now.strftime('%Y年%m月%d日 %H:%M:%S')}"

def lambda_handler(event, context):
    """AWS Lambda handler function."""
    return mcp.handle_request(event, context)