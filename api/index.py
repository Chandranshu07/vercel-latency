import json
import numpy as np

DATA = [
    {"region":"apac","latency_ms":153.82,"uptime_pct":99.226},
    {"region":"apac","latency_ms":182.74,"uptime_pct":99.194},
    {"region":"apac","latency_ms":171.75,"uptime_pct":98.045},
    {"region":"apac","latency_ms":164.65,"uptime_pct":98.403},
    {"region":"apac","latency_ms":106.9,"uptime_pct":99.077},
    {"region":"apac","latency_ms":210.96,"uptime_pct":98.473},
    {"region":"apac","latency_ms":206.64,"uptime_pct":99.328},
    {"region":"apac","latency_ms":173.26,"uptime_pct":98.468},
    {"region":"apac","latency_ms":158.55,"uptime_pct":97.572},
    {"region":"apac","latency_ms":148.86,"uptime_pct":97.451},
    {"region":"apac","latency_ms":141.56,"uptime_pct":97.177},
    {"region":"apac","latency_ms":163.15,"uptime_pct":97.546},

    {"region":"emea","latency_ms":130.3,"uptime_pct":99.362},
    {"region":"emea","latency_ms":214.35,"uptime_pct":97.982},
    {"region":"emea","latency_ms":205.36,"uptime_pct":97.41},
    {"region":"emea","latency_ms":140.22,"uptime_pct":98.866},
    {"region":"emea","latency_ms":112.49,"uptime_pct":99.434},
    {"region":"emea","latency_ms":119.32,"uptime_pct":97.611},
    {"region":"emea","latency_ms":149.16,"uptime_pct":98.576},
    {"region":"emea","latency_ms":123.02,"uptime_pct":97.782},
    {"region":"emea","latency_ms":177.21,"uptime_pct":97.277},
    {"region":"emea","latency_ms":197.97,"uptime_pct":98.764},
    {"region":"emea","latency_ms":220.15,"uptime_pct":98.258},
    {"region":"emea","latency_ms":222.22,"uptime_pct":98.477},

    {"region":"amer","latency_ms":137.03,"uptime_pct":97.222},
    {"region":"amer","latency_ms":178.33,"uptime_pct":97.127},
    {"region":"amer","latency_ms":184.93,"uptime_pct":98.911},
    {"region":"amer","latency_ms":145.58,"uptime_pct":98.743},
    {"region":"amer","latency_ms":125.34,"uptime_pct":97.36},
    {"region":"amer","latency_ms":203.81,"uptime_pct":98.204},
    {"region":"amer","latency_ms":129.66,"uptime_pct":97.643},
    {"region":"amer","latency_ms":108.08,"uptime_pct":97.931},
    {"region":"amer","latency_ms":206.82,"uptime_pct":99.154},
    {"region":"amer","latency_ms":179.24,"uptime_pct":97.429},
    {"region":"amer","latency_ms":174.48,"uptime_pct":98.643},
    {"region":"amer","latency_ms":110.03,"uptime_pct":97.583},
]

def handler(request, response):

    # CORS headers for every response
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"

    if request.method == "OPTIONS":
        response.status_code = 200
        return response.send("")

    try:
        body = request.get_json()
        regions = body.get("regions", [])
        threshold_ms = body.get("threshold_ms", 180)

        result = {}

        for region in regions:
            records = [r for r in DATA if r["region"] == region]

            if not records:
                result[region] = None
                continue

            latencies = [r["latency_ms"] for r in records]
            uptimes = [r["uptime_pct"] for r in records]

            result[region] = {
                "avg_latency": float(np.mean(latencies)),
                "p95_latency": float(np.percentile(latencies, 95)),
                "avg_uptime": float(np.mean(uptimes)),
                "breaches": int(sum(1 for l in latencies if l > threshold_ms))
            }

        response.status_code = 200
        return response.send(json.dumps(result))

    except Exception as e:
        response.status_code = 500
        return response.send(json.dumps({"error": str(e)}))
