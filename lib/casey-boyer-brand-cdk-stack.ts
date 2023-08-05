import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { createWebsiteStack } from './websiteStack';
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class CaseyBoyerBrandCdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    createWebsiteStack(this);
  }
}
