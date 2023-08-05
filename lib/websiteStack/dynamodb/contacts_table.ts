import {
  AttributeType,
  BillingMode,
  ProjectionType,
  Table,
  TableEncryption,
  TableProps,
} from 'aws-cdk-lib/aws-dynamodb';
import { Key } from 'aws-cdk-lib/aws-kms';
import { Construct } from 'constructs';

export class CustomerTable extends Table {
  constructor(scope: Construct, id: string, props?: Partial<TableProps>) {
    super(scope, id, {
      tableName: 'CaseyBoyerBrandCustomers',
      partitionKey: {
        name: 'Id',
        type: AttributeType.STRING,
      },
      billingMode: BillingMode.PAY_PER_REQUEST,
      encryption: TableEncryption.CUSTOMER_MANAGED,
      encryptionKey: new Key(scope, 'CaseyBoyerBrandCustomersEncryption', {
        alias: 'CaseyBoyerBrandCustomersTable',
        description: 'key for Casey Boyer Customers Table',
      }),

      ...props,
    });

    this.addGlobalSecondaryIndex({
      indexName: 'CustomerEmailIndex',
      partitionKey: {
        name: 'Email',
        type: AttributeType.STRING,
      },
      sortKey: {
        name: 'Phone',
        type: AttributeType.STRING,
      },
      projectionType: ProjectionType.ALL,
    });

    this.addGlobalSecondaryIndex({
      indexName: 'CustomerPhoneIndex',
      partitionKey: {
        name: 'Phone',
        type: AttributeType.STRING,
      },
      sortKey: {
        name: 'Email',
        type: AttributeType.STRING,
      },
      projectionType: ProjectionType.ALL,
    });
  }
}
