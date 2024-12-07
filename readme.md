# Birthday Wisher Lambda

[![codecov](https://codecov.io/github/Shredmetal/Enterprise-grade-birthday-wisher-bot-AWS-lambda/graph/badge.svg?token=U7HDVH41PA)](https://codecov.io/github/Shredmetal/Enterprise-grade-birthday-wisher-bot-AWS-lambda)

I was studying for AWS Cloud Practitioner and uhhh, got bored. So naturally, I built an enterprise-grade birthday wishing system because who needs to remember birthdays when you can spend 8 hours automating it? 🎂

Automatically sends personalised birthday wishes using OpenAI/Anthropic, because apparently "Happy Birthday!" isn't complex enough anymore. 

Features:
- Reads birthdays from a csv in S3 (why engineer when you can overengineer)
- Generates messages via OpenAI/Anthropic (because we needed AI to say "Happy Birthday")
- Sends emails (the old-fashioned part)
- Has 86% test coverage (the remaining 14% (or maybe 10% more coverage, honestly, no idea) is running in AWS wondering why it exists)

It's 86% coverage because it can't run the lambda integration test locally because that needs a live lambda environment. To run that, shove it on Lambda and run it in test mode.

Run it in test mode by sticking this in the Event JSON in lambda:

```
{
  "test_mode": true
}
```

## Setup

1. **AWS Resources Required**:
   - S3 bucket with `birthdays.csv` file (required headers: name,email,day,month,sarcastic)
   - The 'sarcastic' header in the `birthdays.csv` file is a column that is either `true` or `false` and determines whether that friend is going to get a sarcastic birthday greeting or not.
   - SSM Parameters:

```
OPENAI_API_KEY / ANTHROPIC_API_KEY # Depending on what you set LLM_PROVIDER_SELECTION in constants.py to
SENDER_EMAIL
EMAIL_PASSWORD
```

2. **Lambda Configuration**:
   - Runtime: Python 3.12
   - Handler: `src.birthday_wisher.birthday_wisher.lambda_handler` (Scroll down to runtime settings in the new UI, it's not in Configuration)
   - Memory: 256MB
   - Timeout: 5 minutes
   - Environment Variables:

```
BUCKET_NAME=your-bucket-name
FILE_KEY=birthdays.csv
```


## AWS Setup Steps

1. **Create S3 Bucket**:
   - Go to S3 in AWS Console
   - Click "Create bucket"
   - Choose a unique name
   - Keep default settings
   - Create a CSV file with headers: `name,email,day,month,sarcastic`
   - Upload to bucket as `birthdays.csv`

2. **Create SSM Parameters**:
   - Go to AWS Systems Manager → Parameter Store
   - Click "Create parameter" for each:

```
Name: OPENAI_API_KEY 
Type: SecureString 
Value: your-openai-key

# Alternatively, depending on what you set in constants.py:

Name: ANTHROPIC_API_KEY 
Type: SecureString 
Value: your-anthropic-key

Name: SENDER_EMAIL 
Type: SecureString 
Value: your-email-address

Name: EMAIL_PASSWORD 
Type: SecureString 
Value: your-app-password

// OBVIOUSLY - you will need to set up an email account that you can access programatically
```

3. **Set up EventBridge**:
   - Go to Amazon EventBridge
   - Click "Create rule"
   - Name it (e.g., "birthday-wisher-daily")
   - For Schedule pattern, use cron: `0 0 * * ? *` (runs daily at midnight UTC)
   - Target: Select your Lambda function
   - Create rule

## Deployment

Run `create_deployment_package.py` to create a Lambda deployment package:

## Deployment

Run `create_deployment_package.py` to create a Lambda deployment package:

```
python create_deployment_package.py
```

Upload the generated `deployment-package.zip` to Lambda.

## Testing

### Local Tests
Requires `.env` file with:

```
OPENAI_API_KEY=your-key / or ANTHROPIC_API_KEY, depending on constants
SENDER_EMAIL=your-email
EMAIL_PASSWORD=your-password
BUCKET_NAME=your-bucket
FILE_KEY=birthdays.csv
```

Run local tests:

```
python -m src.test.test_runner
```


### Lambda Integration Tests
Test AWS integration in Lambda by creating a test event:

```
{
    "test_mode": true
}
```


## Normal Operation
Lambda runs daily via EventBridge schedule to check for and send birthday wishes.
