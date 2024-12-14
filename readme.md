# Honest Morgan's Premium Export-Quality Enterprise-Grade AI-Powered Cloud-Native Serverless-Architecture Business-Oriented Birthday Wishing Platform

[![codecov](https://codecov.io/github/Shredmetal/Enterprise-grade-birthday-wisher-bot-AWS-lambda/graph/badge.svg?token=U7HDVH41PA)](https://codecov.io/github/Shredmetal/Enterprise-grade-birthday-wisher-bot-AWS-lambda)

> Disclaimer: This is a satirical look at enterprise software development. 
All opinions are my own and do not reflect those of my employer.
While this project is satirical, I take professionalism and inclusivity seriously. The humour is directed at the ridiculous overengineering that I decided to do when I was bored, not at any individuals or specific organisations.

This piece of software automatically sends personalised birthday wishes using OpenAI/Anthropic. 

I mean serious business and serious business in 2024 means AI. 

## Enterprise-Grade Feature Implementation

### Core Functionality
- Cloud-native customer data ingestion via S3-based data lake architecture 
  (because traditional databases are for companies stuck in 2023)
- AI-powered personalised message generation leveraging industry-leading LLM providers 
  (transformational implementation of turning "Happy Birthday" into a mission-critical AI use case)
- Legacy communication protocol support via SMTP 
  (because email still exists, unfortunately. This business believes in Web3 communications where our interactions are securely persisted on a blockchain, but we have not implemented it due to compatibility issues with legacy communications protocols)

### Quality Assurance Metrics
- Industry-leading 86% test coverage with comprehensive validation suites
  (the remaining 14% exists in a quantum state within AWS Lambda, 
   simultaneously tested and untested until observed, or the assigned junior dev runs it in `test_mode`)

### Business Value Drivers
- Synergy-optimised message delivery pipeline
- Stakeholder-aligned birthday communication protocols
- AI-driven customer engagement analytics
- Resource-optimised cloud infrastructure utilisation

### Compliance and Testing
Test coverage metrics exclude Lambda integration tests due to cloud-native infrastructure requirements. For complete enterprise 
validation, deploy to Lambda and execute in compliance verification mode:

```
{
  "test_mode": true
}
```

## Strategic Mission Alignment

This enterprise-grade solution revolutionises the 
birthday-greeting paradigm through cutting-edge AI integration, 
enabling synergistic customer engagement while maintaining 
optimal cost-efficiency metrics in a cloud-native environment.

## Enterprise Risk Mitigation Protocols

- Cake-Protocol Compliance (CPC) validation
- Birthday Greeting Delivery SLA: 99.9999% (Because 69 LOL)
- AI-powered sentiment analysis behavioural testing for greeting optimisation

## Key Performance Indicators

- Birthday Wish Delivery Success Rate (BWDSR)
- Mean Time Between Greetings (MTBG)
- AI Response Sentiment Score (AIRSS)
- Customer Birthday Recognition Index (CBRI)

## Enterprise Resource Provisioning

### Cloud Infrastructure Provisioning Protocol

Implementation of mission-critical greeting delivery infrastructure 
requires careful orchestration of cloud-native resources through 
a strategic deployment methodology aligned with enterprise 
best practices

1. **Mission-Critical AWS Infrastructure Requirements**:
   - Cloud-native S3 data lake implementation for customer relationship management: - S3 bucket with `birthdays.csv` file (required headers: name,email,day,month,sarcastic)
   - Strategic data architecture utilizing enterprise-grade CSV paradigms: The 'sarcastic' header in the `birthdays.csv` file is a column that is either `true` or `false` and determines whether that customer is going to get a sarcastic birthday greeting or not.
   - SSM Parameters:

```
OPENAI_API_KEY / ANTHROPIC_API_KEY # Depending on what you set LLM_PROVIDER_SELECTION in constants.py to
SENDER_EMAIL
EMAIL_PASSWORD
```

2. **Serverless Compute Resource Optimization**:
   - Enterprise-grade Python 3.12 runtime environment
   - Memory allocation optimized for business-critical operations: 256MB
   - Resource utilization parameters aligned with corporate efficiency metrics
   - Handler: `src.birthday_wisher.birthday_wisher.lambda_handler` (Scroll down to runtime settings in the new UI, it's not in Configuration)
   - Timeout: 5 minutes
   - Environment Variables:

```
BUCKET_NAME=your-bucket-name
FILE_KEY=birthdays.csv
```

3. **Code Configuration**
   - You will need to configure `src/birthday_wisher/constants/constants.py`
   - `YOUR_NAME` should be your name, the bot will say you instructed it to send birthday wishes
   - `YOUR_EMAIL` should be your email, which the bot will send an email to when it does something so you know when it is doing something because serious businesses keep proper enterprise records.


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


```
python create_deployment_package.py
```

Upload the generated `deployment-package.zip` to Lambda.

## Quality Assurance and Compliance Validation

### Development Environment Validation Protocol

Requires enterprise-grade environment configuration manifest (`.env`):

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


## Production Deployment Operations

The mission-critical serverless infrastructure executes according to 
enterprise-defined temporal parameters via cloud-native EventBridge 
orchestration, ensuring optimal resource utilisation and maintaining 
strict SLA compliance.
