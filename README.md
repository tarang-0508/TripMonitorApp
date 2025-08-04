#  Real-Time Trip Event Monitoring System

##  Project Summary

This solution provides real-time surveillance of taxi trip data using Azure's cloud-native services. Events are streamed via **Azure Event Hub**, processed with **Azure Functions**, and routed by a **Logic App** to deliver intelligent alerts directly into **Microsoft Teams** using Adaptive Cards. This helps operational teams track suspicious patterns like group rides or cash-based anomalies instantly.

---

## System Components

The system is composed of the following Azure services:

- **Event Hub**: Receives live JSON-based trip events (e.g., vendor, distance, payment type).
- **Azure Function**: Analyzes each trip using business logic to flag abnormal behavior.
- **Logic App**: Coordinates the event pipeline and posts notifications to Teams.
- **Microsoft Teams**: Displays detailed trip summaries through Adaptive Cards in a dedicated channel.

###  Workflow Overview

1. Events flow into Event Hub from a simulated data generator.
2. Logic App polls for new messages, parses them, and calls the Azure Function.
3. Function returns analysis and flags (e.g., suspicious vendor, long trip).
4. Logic App conditionally formats and pushes updates to Teams.

---

##  Trip Analysis Function 

This Python Azure Function accepts an HTTP request containing one or more taxi trips and applies rule-based logic to flag outliers.

```python
import azure.functions as func
import logging, json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="")
def analyze_trip(req: func.HttpRequest) -> func.HttpResponse:
    try:
        data = req.get_json()
        trips = data if isinstance(data, list) else [data]
        results = []

        for item in trips:
            t = item.get("ContentData", {})
            vendor = t.get("vendorID")
            distance = float(t.get("tripDistance", 0))
            passengers = int(t.get("passengerCount", 0))
            payment = str(t.get("paymentType"))
            tags = []

            if distance > 10: tags.append("LongTrip")
            if passengers > 4: tags.append("GroupRide")
            if payment == "2": tags.append("CashPayment")
            if payment == "2" and distance < 1:
                tags.append("SuspiciousVendorActivity")

            results.append({
                "vendorID": vendor,
                "tripDistance": distance,
                "passengerCount": passengers,
                "paymentType": payment,
                "insights": tags,
                "isInteresting": bool(tags),
                "summary": f"{len(tags)} issues: {', '.join(tags)}" if tags else "Trip appears normal"
            })

        return func.HttpResponse(json.dumps(results), status_code=200, mimetype="application/json")

    except Exception as ex:
        logging.error(f"Processing error: {ex}")
        return func.HttpResponse(f"Failed: {str(ex)}", status_code=400)
