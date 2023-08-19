import { Construct } from 'constructs';
import { CaseyBoyerBrandWebsiteBucket } from './websiteBucket';

export function createS3Buckets(scope: Construct) {
  return {
    caseyBoyerBrandBucket: new CaseyBoyerBrandWebsiteBucket(scope, 'CaseyBoyerBrandWebsiteBucket'),
  };
}
