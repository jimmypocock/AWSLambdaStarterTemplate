# Lambda Template

This template provides a foundation for building serverless applications using AWS Lambda, API Gateway, and Aurora Serverless v2.

## Prerequisites

- AWS CLI configured with appropriate credentials
- Python 3.9 or later
- Node.js 16 or later (for CDK)
- AWS CDK CLI (`npm install -g aws-cdk`)

## Project Structure

```
LambdaTemplate/
├── src/
│   ├── functions/
│   │   ├── goodbye_item/
│   │   │   ├── app.py
│   │   │   └── requirements.txt
│   │   └── hello_item/
│   │       ├── app.py
│   │       └── requirements.txt
├── tests/
│   └── functions/
│       ├── goodbye_item/
│       │   └── test_app.py
│       └── hello_item/
│           └── test_app.py
├── database.yaml
├── api.yaml
├── network.yaml
└── README.md
```

## Infrastructure Components

### Database (database.yaml)
- Aurora Serverless v2 MySQL cluster
- Engine version: 8.0.mysql_aurora.3.07.0
- Data API enabled for serverless access
- Automatic scaling from 0.5 to 1 ACU
- Encrypted storage
- VPC-based security
- Secrets Manager integration for credentials

### API (api.yaml)
- API Gateway REST API
- Lambda functions with RDS Data API integration
- Cognito User Pool for authentication
- IAM roles and policies for database access
- Environment-specific configurations

### Network (network.yaml)
- VPC with public and private subnets
- Security groups for Lambda and database access
- VPC endpoints for AWS services
- SSM instance for database access

## Deployment

1. Deploy the network stack:
```bash
aws cloudformation deploy \
    --template-file network.yaml \
    --stack-name your-network-stack \
    --parameter-overrides \
        Environment=dev \
        Stage=development
```

2. Deploy the database stack:
```bash
aws cloudformation deploy \
    --template-file database.yaml \
    --stack-name your-database-stack \
    --parameter-overrides \
        Environment=dev \
        Stage=development \
        VpcId=vpc-xxxxxxxx \
        DBUsername=your_db_username \
        DBPassword=your_db_password
```

3. Deploy the API stack:
```bash
aws cloudformation deploy \
    --template-file api.yaml \
    --stack-name your-api-stack \
    --parameter-overrides \
        Environment=dev \
        Stage=development \
        NetworkStackName=your-network-stack \
        DBClusterArn=arn:aws:rds:region:account:cluster:your-cluster \
        DBSecretArn=arn:aws:secretsmanager:region:account:secret:your-secret \
        DBName=rdsdb
```

## Testing

1. Unit tests:
```bash
python -m pytest tests/
```

2. API testing:
```bash
# Get API endpoint
API_ENDPOINT=$(aws cloudformation describe-stacks --stack-name your-api-stack --query "Stacks[0].Outputs[?OutputKey=='ApiEndpoint'].OutputValue" --output text)

# Test endpoints
curl -X GET $API_ENDPOINT/hello
curl -X GET $API_ENDPOINT/goodbye/1
```

## Database Access

The database is accessible through:
1. RDS Data API (recommended for Lambda functions)
2. Query editor in AWS Console
3. SSM instance in the VPC

To access the database via Query Editor:
1. Go to RDS Console
2. Select your Aurora cluster
3. Click "Query Editor"
4. Use credentials from Secrets Manager

## Security

- All sensitive data stored in AWS Secrets Manager
- Database access restricted to VPC
- IAM roles with least privilege
- Encrypted storage and network traffic
- Regular security updates through AWS managed services

## Monitoring

- CloudWatch Logs for Lambda functions
- RDS Performance Insights
- CloudWatch Metrics for database and API
- X-Ray tracing for API requests

## Cleanup

To delete all resources:
```bash
aws cloudformation delete-stack --stack-name your-api-stack
aws cloudformation delete-stack --stack-name your-database-stack
aws cloudformation delete-stack --stack-name your-network-stack
```