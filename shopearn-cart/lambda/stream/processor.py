from ddb import from_ddb, ddb_dumps
from log import AppLogger

log = AppLogger(service="stream")


def handler(event, context):
    for record in event['Records']:
        event_name = record['eventName']  # INSERT, MODIFY, REMOVE
        dynamodb_record = record['dynamodb']
        log.info(f"Event: {event_name}")
        if event_name == 'INSERT':
            new_image = dynamodb_record.get('NewImage', {})
            log.info("New item added:" + ddb_dumps(from_ddb(new_image)))
        elif event_name == 'MODIFY':
            old_image = dynamodb_record.get('OldImage', {})
            new_image = dynamodb_record.get('NewImage', {})
            log.info("Item modified:")
            log.info("Old:" + ddb_dumps(from_ddb(old_image)))
            log.info("New:" + ddb_dumps(from_ddb(new_image)))
        elif event_name == 'REMOVE':
            old_image = dynamodb_record.get('OldImage', {})
            log.info("Item removed:" + from_ddb(old_image))
        else:
            log.warning(f"Unknown event type: {event_name}")
    return {"statusCode": 200}
