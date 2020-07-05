# ライセンスコード配布用アプリケーション

トレーニング実施中のライセンスコード配布用のアプリケーションです。

# Backend のDeploy 方法

事前にSAM CLI をインストールしておいてください。
[Linux への AWS SAM CLI のインストール - AWS サーバーレスアプリケーションモデル](https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/serverless-sam-cli-install-linux.html)

```
cd backend
sam deploy --guided
```

Configure SAM Daploy のプロンプトで適当に入力してください。（2回目からは単位　`sam deploy` でデプロイできます。)


デプロイが終了したら以下のコマンドで作成されたリソースを確認します。

```
aws cloudformation describe-stacks --stack-name aws-training-app --query 'Stacks[*].Outputs' --output table

```

以下のように表示されます。

```
---------------------------------------------------------------------------------------
|                                   DescribeStacks                                    |
+---------------+---------------------------------------------------------------------+
|   OutputKey   |                             OutputValue                             |
+---------------+---------------------------------------------------------------------+
|  BucketName   |  aws-training-app-licensecodescsvbucket-xxxxxxxxx                   |
|  ApiUri       |  https://xxxxxxx.execute-api.ap-northeast-1.amazonaws.com/prod      |
|  DynamoDBTable|  aws-training-app-LicenseCodesAssignment-xxxxxxx                    |
+---------------+---------------------------------------------------------------------+
```

# データの登録

上記の作成されたバケットにライセンスコードを記述したcsv ファイルをアップロードします。
以下のフォルダにサンプルcsv を用意していますので、参考にしてください。

backend/sampledata/sample.csv

フォーマットは以下のようになっています。

```
コース名,ライセンスコード,受講者のemail
```

sample.csv の内容
```
Dummy Course,ABCDEFGHGJK12345678901,test01@example.com
Dummy Course,ABCDEFGHGJK12345678902,test02@example.com
```

以下のようにS3 にcsv ファイルをアップロードしてください。

```
aws s3 cp sample.csv s3://your_backet_name
```

DyanmoDB テーブルにデータが格納されていることを確認します。


# FrontEnd の確認

## API Gateway のURL をconfig.js に設定する

forntend/src/config.js 内の"replace_your_api_url" をCloudFormation のOutput にて取得した、ApiUri に書き換えます。

## ローカル実行

以下のコマンドでFront アプリをローカル実行します。

```
npm install
yarn start
```

ローカル実行して問題なければ、以下のようにビルドします。
```
yarn build
```

frontend/build にビルドされたArtifact が出力されるので、S3 などにアップロードして受講者がアクセスできるように公開してください。
もしくは、AWS Amplify を利用して公開することも可能です。
