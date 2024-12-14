# Honest and Very Serious Business' Premium Export-Quality Enterprise-Grade AI-Powered Cloud-Native Serverless-Architecture Business-Oriented Birthday Wishing Platform

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
  (remaining 14% requires AWS Lambda environment for integration testing, 
   as per AWS best practices for serverless applications)

### Business Value Drivers
- Synergy-optimised message delivery pipeline
- Stakeholder-aligned birthday communication protocols
- AI-driven customer engagement analytics
- Resource-optimised cloud infrastructure utilisation

### Compliance and Testing
Test coverage metrics exclude Lambda integration tests as these require 
cloud-native infrastructure for proper enterprise-grade validation. 
For complete enterprise validation, deploy to Lambda and execute in 
compliance verification mode:

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

### Enterprise Quality Architecture Diagram:

![Architecture Diagram](https://i.imgur.com/1YU2JSg.jpeg)

### Cloud Infrastructure Provisioning Protocol

Implementation of mission-critical greeting delivery infrastructure 
requires careful orchestration of cloud-native resources through 
a strategic deployment methodology aligned with enterprise 
best practices

1. **Mission-Critical AWS Infrastructure Requirements**:
   - Cloud-native S3 data lake implementation for customer relationship management: - S3 bucket with `birthdays.csv` file (required headers: name,email,day,month,sarcastic)
   - Strategic data architecture utilising enterprise-grade CSV paradigms: The 'sarcastic' header in the `birthdays.csv` file is a column that is either `true` or `false` and determines whether that customer is going to get a sarcastic birthday greeting or not.
   - SSM Parameters:

```
OPENAI_API_KEY / ANTHROPIC_API_KEY # Depending on what you set LLM_PROVIDER_SELECTION in constants.py to
SENDER_EMAIL
EMAIL_PASSWORD
```

2. **Serverless Compute Resource Optimisation**:
   - Enterprise-grade Python 3.12 runtime environment
   - Memory allocation optimised for business-critical operations: 256MB
   - Resource utilisation parameters aligned with corporate efficiency metrics
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

1. Run `create_deployment_package.py` to create a Lambda deployment package:


```
python create_deployment_package.py
```

2. Upload the generated `deployment-package.zip` to Lambda.

3. IAM Roles

**Set up IAM Role For your Lambda Function**:

- Create the Role
- Go to IAM > Roles
- Click "Create role"
- Under "Trusted entity type" select "AWS service"
- Under "Use case" select "Lambda"
- Click "Next"

**Add Permissions**

In the permissions search bar, search and select:
```
AmazonS3ReadOnlyAccess
AmazonSSMReadOnlyAccess
AWSLambdaBasicExecutionRole
```

- Click "Next"
- Name the Role
- Give it a name like "birthday-wisher-lambda-role" (because enterprise-grade systems need properly documented naming conventions)
- Add a description like "Enables our mission-critical birthday communication platform to access required AWS services"
- Click "Create role"

**Attaching the Role to Lambda**

- Go to Your Lambda Function
- Click on the "Configuration" tab
- Click on "Permissions" in the left sidebar
- Under "Execution role", click "Edit"
- Select your newly created role from the dropdown
- Click "Save"

**Lambda Environment Variable Setup**

- Click on the configuration tab of your Lambda function
- Click on Environment Variables
- Create environment variables of where you stored your super important customer database in S3 with the folliowing key-value pairs:

```
BUCKET_NAME=name_of_s3_bucket_with_customer_data
FILE_KEY=file_key_of_csv_containing_customer_data
```

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

## Strategic Contribution Framework

> This is actually a joke, please don't actually send me an essay, but if you want to send a PR with unnecessary code complication, it's definitely welcome.

### Mission-Critical Onboarding Protocol
At Honest Morgan's Premium Export-Quality Enterprise-Grade AI-Powered Cloud-Native 
Birthday Wishing Platform, we take our enterprise responsibilities seriously. 
All potential contributors must complete our rigorous onboarding process:

1. **Self-Reflection Phase**
   - Write a 2-word essay on "Why Enterprise-Grade Birthday Wishes Matter", the only correct answer is "because lol"
   - Complete personality assessment to ensure cultural alignment with our 
     mission-critical greeting delivery objectives

2. **Technical Alignment Phase**
   - Study our enterprise-grade architecture diagrams by producing them for interview number 25
   - Memorise all AWS service limits and write it in a digestible format because our engineers haven't bothered for interview number 41
   - Achieve enlightenment regarding the true meaning of "cloud-native" during interview number 57 when we get all 1,000 candidates to sit in a room together for chakra alignment

### Current Strategic Enhancement Opportunities

We are actively seeking enterprise-focused contributors for the following 
mission-critical initiatives:

1. **Exception Handling Optimisation**
   - Current Status: Multiple bare exceptions being caught (extremely non-enterprise)
   - Required Action: Implementation of proper exception handling paradigms
   - Business Impact: Enhanced operational visibility
   - Example of current non-enterprise pattern:

```
try: 
   do_something_mission_critical() 
except: # This hurts our enterprise credibility 
   logger.error("Something failed")
```

Expected enterprise-grade implementation (real implementation should be more complex than this though):

```
try: 
   do_something_mission_critical() 
except Exception as e: 
   logger.error(f"Mission-critical operation failed: {str(e)}") metrics.increment("birthday_wish_failure_count") 
   raise BirthdayWishingPlatformException( f"Enterprise-grade operation failed: {str(e)}" )
```

### Contribution Guidelines

1. All code must be:
   - Enterprise-grade
   - Cloud-native
   - AI-powered (where applicable)
   - Blockchain-compatible
   - Properly exception-handled

2. All PRs must include:
   - Impact analysis on birthday wish delivery SLAs
   - Enterprise buzzword density metrics
   - AI-generated code review comments

### Getting Started

1. Fork the repository (ensure your fork is enterprise-grade)
2. Create a feature branch (following enterprise naming conventions)
3. Implement enterprise-quality enhancements
4. Submit PR with required documentation
5. Await enterprise-grade review process

Remember: We're not just sending birthday wishes, we're revolutionising 
the enterprise birthday communication paradigm.