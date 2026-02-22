import json
import numpy as np

with open("data/latency.json") as f:
    RAW_DATA = json.load(f)

def handler(request):
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "Content-Type": "application/json"
    }

    if request.method == "OPTIONS":
        return Response("", 200, headers)

    if request.method != "POST":
        return Response("Method not allowed", 405, headers)

    body = request.json()
    regions = body.get("regions", [])
    threshold_ms = body.get("threshold_ms", 180)

    result = {}
    for region in regions:
        records = [r for r in RAW_DATA if r["region"] == region]
        if not records:
            result[region] = None
            continue
        latencies = [r["latency_ms"] for r in records]
        uptimes = [r["uptime_pct"] for r in records]
        result[region] = {
            "avg_latency": round(float(np.mean(latencies)), 4),
            "p95_latency": round(float(np.percentile(latencies, 95)), 4),
            "avg_uptime": round(float(np.mean(uptimes)), 4),
            "breaches": int(sum(1 for l in latencies if l > threshold_ms))
        }

    return Response(json.dumps(result), 200, headers)
