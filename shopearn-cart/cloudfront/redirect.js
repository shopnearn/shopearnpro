// eslint-disable-next-line import/no-extraneous-dependencies
import cf from 'cloudfront';

const kvs = cf.kvs();
// eslint-disable-next-line no-unused-vars
function handler(event) {
  var kv = kvs.get('redirect:/fr');
  if (event.request.uri === '/fr') {
    return {
      statusCode: 302,
      statusDescription: 'Found',
      headers: {
        location: { value: kv || '/default' },
      },
    };
  }
  return event.request;
}
