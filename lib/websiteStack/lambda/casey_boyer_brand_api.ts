import { PythonFunction } from "@aws-cdk/aws-lambda-python-alpha";
import { Duration } from "aws-cdk-lib";
import { Runtime } from "aws-cdk-lib/aws-lambda";
import { Construct } from "constructs";

export class CaseyBoyerBrandApiLambda extends PythonFunction {
  constructor(scope: Construct, id: string) {
    super(scope, id, {
      functionName: "CaseyBoyerBrandApi",
      description: "api for casey-boyer-brand",
      entry: "src/casey_boyer_brand_api",
      runtime: Runtime.PYTHON_3_9,
      index: "handler.py",
      handler: "handler",
      timeout: Duration.seconds(30),
    });
  }
}
