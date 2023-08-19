import { Construct } from 'constructs';
import { CaseyBoyerBrandApiLambda } from './casey_boyer_brand_api';

export function createLambdas(scope: Construct) {
  return {
    caseyBoyerBrandApi: new CaseyBoyerBrandApiLambda(scope, 'CaseyBoyerBrandApiLambda'),
  };
}
