import { Key } from 'aws-cdk-lib/aws-kms';
import { Subscription, SubscriptionProtocol, Topic, TopicProps } from 'aws-cdk-lib/aws-sns';
import { Construct } from 'constructs';

export class ContactUsTopic extends Topic {
  readonly encryptionKey: Key;

  constructor(scope: Construct, id: string, props: TopicProps = {}) {
    const encryptionKey = new Key(scope, 'CaseyBoyerBrandContactUsTopicEncryption', {
      alias: 'CaseyBoyerBrandContactUsTopic',
      description: 'key for Casey Boyer Contact Us Topic',
    });
    super(scope, id, {
      displayName: 'Casey Boyer Consulting - Contact Us - Topic',
      topicName: 'casey-boyer-brand-contact-us',
      masterKey: encryptionKey,
      fifo: false,

      ...props,
    });

    this.encryptionKey = encryptionKey;

    new Subscription(this, 'Subscription', {
      topic: this,
      protocol: SubscriptionProtocol.EMAIL,
      endpoint: 'contact+casey-boyer-brand-contactus@boyer.consulting',
    });
  }
}
