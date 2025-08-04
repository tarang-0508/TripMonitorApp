from azure.eventhub import EventHubProducerClient, EventData
import json
import time

# ✅ Your Event Hub connection string and name
CONNECTION_STR = "Endpoint=sb://tripmonnamespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=XVtxC7ZtZau3OrK95CdSTl8MpN0j0U2wz+AEhByRi3g="
EVENTHUB_NAME = "trip-events"

# Sample taxi trip events
events = [
    {"ContentData": {"vendorID": "V001", "tripDistance": "2", "passengerCount": "2", "paymentType": "1"}},
    {"ContentData": {"vendorID": "V002", "tripDistance": "15.2", "passengerCount": "6", "paymentType": "1"}},
    {"ContentData": {"vendorID": "V003", "tripDistance": "0.4", "passengerCount": "1", "paymentType": "2"}}
]

# Create the Event Hub producer client
producer = EventHubProducerClient.from_connection_string(
    conn_str=CONNECTION_STR,
    eventhub_name=EVENTHUB_NAME
)

try:
    for i, evt in enumerate(events):
        batch = producer.create_batch()
        batch.add(EventData(json.dumps(evt)))
        producer.send_batch(batch)
        print(f"✅ Sent message {i+1}:\n{json.dumps(evt, indent=2)}")
        if i < len(events) - 1:
            time.sleep(3)  # Delay between messages

    print("✅ All messages sent successfully.")
except Exception as e:
    print("❌ Failed to send messages:", str(e))
finally:
    producer.close()
