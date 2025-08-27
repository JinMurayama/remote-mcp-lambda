# Lambda MCP Server (Remote)

AWS LambdaでホストされるシンプルなRemote MCPサーバーです。

## 概要

このMCPサーバーは、基本的な挨拶機能と現在時刻取得機能を提供するシンプルなツールです。MCP (Model Context Protocol) を使用してClaudeと通信し、カスタムツールを提供します。

## アーキテクチャ

### 技術スタック
- **AWS Lambda**: サーバーレス実行環境
- **Lambda Layer**: Python依存関係の管理
- **MCP (Model Context Protocol)**: Claudeとの通信プロトコル
- **CDK**: インフラストラクチャ・アズ・コード

### ファイル構成
```
remote-mcp-lambda/
├── app/
│   ├── code/
│   │   ├── lambda_function.py    # メインのLambda関数
│   │   └── requirements.txt      # Python依存関係
│   └── layer/
│       └── python/               # Lambda Layer用Pythonパッケージ
├── infra/
│   ├── app.py                    # CDKアプリケーション
│   ├── cdk.json                  # CDK設定
│   ├── requirements.txt          # CDK依存関係
│   ├── infra/
│   │   └── infra_stack.py        # メインのインフラスタック
│   └── cdk_constructs/
│       └── infra_construct.py    # Lambda用の再利用可能なコンストラクト
```

## デプロイ

### 前提条件

- AWS CLI設定済み
- CDK CLI インストール済み
- Python 3.11+

### 1. Lambda Layerの準備

```bash
cd app && mkdir -p layer/python
cd layer/python

# 必要なライブラリをインストール
pip3 install -r ../../code/requirements.txt -t .

# 不要なパッケージを削除（オプション）
rm -rf boto3* botocore* s3transfer* python_dateutil* dateutil*
rm -rf bin/ __pycache__/

```

### 2. 依存関係のインストール

```bash
cd infra

# CDK依存関係のインストール
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. CDKブートストラップ（初回のみ）

```bash
# CDKブートストラップ
cdk bootstrap
```

### 4. デプロイ

```bash
# デプロイ実行
cdk deploy

# 特定のプロファイルを使用する場合
cdk deploy --profile your-profile-name
```

### 出力

デプロイ成功後、以下の情報が出力されます:
- `FunctionUrl`: Lambda Function URLエンドポイント
- `LambdaFunctionArn`: Lambda関数のARN
- `LambdaFunctionName`: Lambda関数名
- `LogGroupName`: CloudWatch Log Group名