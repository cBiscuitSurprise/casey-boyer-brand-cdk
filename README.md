# This project holds the AWS resources required to run the Casey Boyer Brand site

```bash
npm run synth -- --profile casey-dev
npm run deploy -- --profile casey-dev
```

## Development

Create a file at the root of this project named, `cdk.context.json`, and add the following contents:

```json
{
  "strateGoServerUrl": "gprc://STRATE-GO-SERVER-URL:12345"
}
```
