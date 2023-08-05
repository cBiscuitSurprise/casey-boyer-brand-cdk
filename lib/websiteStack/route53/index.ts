import { Distribution } from "aws-cdk-lib/aws-cloudfront";
import { ARecord, HostedZone, RecordTarget } from "aws-cdk-lib/aws-route53";
import { CloudFrontTarget } from "aws-cdk-lib/aws-route53-targets";
import { StringParameter } from "aws-cdk-lib/aws-ssm";
import { Construct } from "constructs";

import { config } from '../constants';


interface CaseyBoyerBrandDnsProps {
  cloudfront: Distribution;
}

export function createDns(scope: Construct, props: CaseyBoyerBrandDnsProps) {
  const zoneId = StringParameter.valueForStringParameter(scope, config.zoneIdParameter);
  const zone = HostedZone.fromHostedZoneAttributes(scope, "CaseyBoyerBrandDnsHostedZone", {
      hostedZoneId: zoneId,
      zoneName: "boyer.consulting",
  });

  return {
    hostedZone: zone,
    primary: new ARecord(scope, "CaseyBoyerBrandDnsMainRecord", {
      recordName: "casey.boyer.consulting.",
      comment: "main Casey Boyer Brand web-page",
      zone: zone,
      target: RecordTarget.fromAlias(new CloudFrontTarget(props.cloudfront)),
    }),
  }
}