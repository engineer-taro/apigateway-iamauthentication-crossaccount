# apigateway-iamauthentication-crossaccount
[AWS]Try to create a configuration using SAM to call the APIGateway with IAM authentication from Lambda in another account.

# このリポジトリについて
IAM認証をかけたAPIGatewayを別アカウントのLambdaから呼び出す構成をSAMで作成してみました。  
詳細は[こちら](https://qiita.com/drafts/59bc66de255764748ae5)を参考にしてください。  

# デプロイ手順
※ AWSリソースを作成するので、いくらかお金がかかります
※ 検証にはAWSアカウントが二つ必要  
※ AWS SAMをインストールしていない場合インストールが必要  
※ Dockerをインストールしていない場合`sam build --use-container`の際にDockerが必要  
※ 今回利用する2つのAWSアカウント情報を.aws配下credentialsファイルに記述してある前提で書いてあります。  

## 1. Lambda Accuont側のデプロイ

__コマンド__

```
cd lambda_account
sam build --use-container
sam deploy --guided --profile <Lambda側のアカウント> --capabilities CAPABILITY_NAMED_IAM 

# いくつかのパラメータを設定する
  AnotherAccountID Lambda AccuontのアカウントID
  APIString: 後ほど再度設定するのでxxxxxxxxなどにしておく
  FunctionName デフォルトでもOK
  AnotherAccountRoleName 2で設定するロール名。デフォルトでもOK
  APIPath デフォルトでもOK

```

## 2. APIGateway Account側のデプロイ

__コマンド__

```
cd apigateway_account
sam build
sam deploy --guided --profile <APIGateway側のアカウント> --capabilities CAPABILITY_NAMED_IAM 

# いくつかのパラメータを設定する
  AnotherAccountID もう一つのアカウントのID
  RoleName デフォルトでもOK
```

## 3. 設定値を変更してLambad Account側のデプロイを再度行う
Lambdaアカウント側の環境変数APIStringに、APIGatewayのIDを入れる必要があります。  
APIGatewayのアカウントにて、APIGatewayのIDを確認してください。ここでAPIGatewayのIDと言っているのはエンドポイントの以下の部分です。

`https://{APIGatewayのID}.execute-api.ap-northeast-1.amazonaws.com/dev/apigateway/lambda_attached_apigateway`

__コマンド__
```
cd lambda_account
sam deploy --guided --profile <Lambda側のアカウント>

# いくつかのパラメータを設定する
  APIString: APIGatewayのID
  他は1のとき設定したものと同じでよい
```