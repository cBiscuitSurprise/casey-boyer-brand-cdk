import { Certificate, CertificateValidation } from "aws-cdk-lib/aws-certificatemanager";
import { IHostedZone } from "aws-cdk-lib/aws-route53";
import { Construct } from "constructs";

interface CertificateProps {
  hostedZone: IHostedZone;
  domainName: string;
  alternateNames: Array<string>;
}

export function createCaseyBoyerBrandCertificate(scope: Construct, props: CertificateProps) {
  return {
    certificate: new Certificate(scope, 'Certificate', {
      certificateName: 'CaseyBoyerBrandWebsite',
      domainName: props.domainName,
      validation: CertificateValidation.fromDns(props.hostedZone),
      subjectAlternativeNames: props.alternateNames,
    }),
  };
}
