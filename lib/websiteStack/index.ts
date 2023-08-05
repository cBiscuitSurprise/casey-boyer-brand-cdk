/**
 * Certificate
 * Route53 records
 * CodePipeline
 */

import { Construct } from 'constructs';
import { createCaseyBoyerBrandWebsitetDistribution } from './cloudfront';
import { createLambdas } from './lambda';
import { createDns } from './route53';
import { createS3Buckets } from './s3';
import { CustomerTable } from './dynamodb/contacts_table';
import { Effect, PolicyStatement } from 'aws-cdk-lib/aws-iam';
import { ContactUsTopic } from './sns/contactUsSns';

export function createWebsiteStack(scope: Construct) {
  const lambdas = createLambdas(scope);
  const buckets = createS3Buckets(scope);

  const cloudfront = createCaseyBoyerBrandWebsitetDistribution(scope, {
    apiFunction: lambdas.caseyBoyerBrandApi,
    bucket: buckets.caseyBoyerBrandBucket,
  });

  const dns = createDns(scope, {
    cloudfront: cloudfront.distribution,
  });

  const customerTable = new CustomerTable(scope, 'CaseyBoyerBrandCustomerTable');

  lambdas.caseyBoyerBrandApi.addToRolePolicy(
    new PolicyStatement({
      effect: Effect.ALLOW,
      actions: ['kms:Encrypt', 'kms:Decrypt', 'kms:GenerateDataKey'],
      resources: [customerTable.encryptionKey!.keyArn],
    })
  );
  lambdas.caseyBoyerBrandApi.addToRolePolicy(
    new PolicyStatement({
      effect: Effect.ALLOW,
      actions: [
        'dynamodb:BatchGetItem',
        'dynamodb:BatchWriteItem',
        'dynamodb:PutItem',
        'dynamodb:DeleteItem',
        'dynamodb:GetItem',
        'dynamodb:Query',
        'dynamodb:UpdateItem',
      ],
      resources: [customerTable.tableArn, `${customerTable.tableArn}/index/*`],
    })
  );

  const contactUsTopic = new ContactUsTopic(scope, 'CaseyBoyerBrandContactUsTopic');
  lambdas.caseyBoyerBrandApi.addEnvironment('CONTACT_US_TOPIC_ARN', contactUsTopic.topicArn);
  lambdas.caseyBoyerBrandApi.addToRolePolicy(
    new PolicyStatement({
      effect: Effect.ALLOW,
      actions: ['sns:Publish'],
      resources: [contactUsTopic.topicArn],
    })
  );
  lambdas.caseyBoyerBrandApi.addToRolePolicy(
    new PolicyStatement({
      effect: Effect.ALLOW,
      actions: ['kms:Encrypt', 'kms:Decrypt', 'kms:GenerateDataKey'],
      resources: [contactUsTopic.encryptionKey.keyArn],
    })
  );
}
