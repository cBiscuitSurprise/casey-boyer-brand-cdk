/**
 * /api/* -> LambdaAPI
 * /* -> S3
 */
import { ArnFormat, Duration, Fn, Stack } from 'aws-cdk-lib';
import {
  AllowedMethods,
  CachePolicy,
  Distribution,
  CfnOriginAccessControl,
  OriginRequestPolicy,
  ResponseHeadersPolicy,
  ViewerProtocolPolicy,
  CfnDistribution,
} from 'aws-cdk-lib/aws-cloudfront';
import { HttpOrigin, S3Origin } from 'aws-cdk-lib/aws-cloudfront-origins';
import { Function, FunctionUrl, FunctionUrlAuthType } from 'aws-cdk-lib/aws-lambda';
import { Bucket, CfnBucketPolicy } from 'aws-cdk-lib/aws-s3';
import { StringParameter } from 'aws-cdk-lib/aws-ssm';
import { Construct } from 'constructs';

import { Certificate } from 'aws-cdk-lib/aws-certificatemanager';
import { config } from '../constants';

interface ICloudFrontProps {
  bucket: Bucket;
  apiFunction: Function;
}

export function createCaseyBoyerBrandWebsitetDistribution(scope: Construct, props: ICloudFrontProps) {
  const oac = new CfnOriginAccessControl(scope, 'CaseyBoyerBrandCloudFrontOAC', {
    originAccessControlConfig: {
      name: 'CaseyBoyerBrandOriginAccessControl',
      originAccessControlOriginType: 's3',
      signingBehavior: 'always',
      signingProtocol: 'sigv4',
      description: 'Access identity for the Casey Boyer Brand website',
    },
  });

  const certificateArn = StringParameter.valueForStringParameter(scope, config.certificateParameter);
  const distro = new Distribution(scope, 'CaseyBoyerBrandCloudFrontDistribution', {
    defaultBehavior: {
      origin: new S3Origin(props.bucket, {
        originId: 'CaseyBoyerBrand-S3',
      }),
    },
    certificate: Certificate.fromCertificateArn(scope, 'CaseyBoyerBrandWebsiteCertificate', certificateArn),
    domainNames: ['casey.boyer.consulting', 'www.casey.boyer.consulting'],
    defaultRootObject: 'index.html',
    enableLogging: true,
    logIncludesCookies: true,
    comment: 'Casey Boyer brand site',
  });

  _addAccessPolicyToS3(props.bucket, distro);

  _workaroundUpdateOriginAccessConfiguration(distro, oac);

  const functionUrl = new FunctionUrl(scope, 'LambdaApiUrl', {
    function: props.apiFunction,
    authType: FunctionUrlAuthType.NONE,
    // cors: {
    //   allowedOrigins: [
    //     "https://casey.boyer.consulting",
    //     "https://www.casey.boyer.consulting"],
    //   allowedMethods: [HttpMethod.GET, HttpMethod.POST],
    //   allowCredentials: true,
    //   maxAge: Duration.minutes(1)
    // }
  });

  const originUrl = Fn.select(2, Fn.split('/', functionUrl.url));

  const lambdaOrigin = new HttpOrigin(originUrl, { originId: 'CaseyBoyerBrand-API' });
  distro.addBehavior('/api/*', lambdaOrigin, {
    viewerProtocolPolicy: ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
    allowedMethods: AllowedMethods.ALLOW_ALL,
    cachePolicy: CachePolicy.CACHING_DISABLED,
    originRequestPolicy: OriginRequestPolicy.ALL_VIEWER_EXCEPT_HOST_HEADER,
    responseHeadersPolicy: new ResponseHeadersPolicy(distro, 'ResponseHeadersPolicy', {
      responseHeadersPolicyName: 'Allow-CORS-LocalHost',
      comment: 'Allows CORS from localhost',
      corsBehavior: {
        accessControlAllowCredentials: false,
        accessControlAllowHeaders: ['*'],
        accessControlAllowMethods: ['GET', 'POST', 'OPTIONS'],
        accessControlAllowOrigins: ['http://localhost:*'],
        accessControlExposeHeaders: [],
        accessControlMaxAge: Duration.minutes(10),
        originOverride: true,
      },
    }),
  });

  return {
    oac,
    distribution: distro,
    functionUrl: functionUrl,
  };
}

function _addAccessPolicyToS3(bucket: Bucket, distro: Distribution) {
  const comS3PolicyOverride = bucket.node.findChild('Policy').node.defaultChild as CfnBucketPolicy;
  const statement = comS3PolicyOverride.policyDocument.statements[1];
  if (statement['_principal'] && statement['_principal'].CanonicalUser) {
    delete statement['_principal'].CanonicalUser;
  }
  comS3PolicyOverride.addOverride('Properties.PolicyDocument.Statement.1.Principal', {
    Service: 'cloudfront.amazonaws.com',
  });
  comS3PolicyOverride.addOverride('Properties.PolicyDocument.Statement.1.Condition', {
    StringEquals: {
      'AWS:SourceArn': Stack.of(distro).formatArn({
        service: 'cloudfront',
        region: '',
        resource: 'distribution',
        resourceName: distro.distributionId,
        arnFormat: ArnFormat.SLASH_RESOURCE_NAME,
      }),
    },
  });
}

function _workaroundUpdateOriginAccessConfiguration(distro: Distribution, oac: CfnOriginAccessControl) {
  const cfnDistribution = distro.node.defaultChild as CfnDistribution;
  cfnDistribution.addOverride('Properties.DistributionConfig.Origins.0.S3OriginConfig.OriginAccessIdentity', '');
  cfnDistribution.addPropertyOverride('DistributionConfig.Origins.0.OriginAccessControlId', oac.getAtt('Id'));
  const s3OriginNode = distro.node.findAll().filter((child) => child.node.id === 'S3Origin');
  s3OriginNode[0].node.tryRemoveChild('Resource');
}
