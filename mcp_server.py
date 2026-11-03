"""
MCP Server for Dual-Sensor Pulse Arrival Time (PAT) / Pulse Transit Time (PTT) Skill.
Exposes JSON-RPC Model Context Protocol tools for assessing arterial elasticity and pulse wave velocity.
"""

import sys
import json
from typing import Dict, Any
from client import PulseArrivalTimeClient


def get_tools_manifest() -> Dict[str, Any]:
    return {
        "tools": [
            {
                "name": "evaluate_pulse_transit",
                "description": "Calculates Pulse Transit Time (PTT), Pulse Wave Velocity (PWV in m/s), and arterial vascular compliance score.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "pat_ms": {
                            "type": "number",
                            "description": "ECG R-peak to peripheral PPG arrival latency in milliseconds (e.g. 210.0 ms)."
                        },
                        "pre_ejection_period_ms": {
                            "type": "number",
                            "description": "Cardiac electromechanical Pre-Ejection Period in milliseconds (e.g. 85.0 ms).",
                            "default": 85.0
                        },
                        "arterial_path_length_m": {
                            "type": "number",
                            "description": "Vascular distance from aortic root to peripheral sensor site in meters (e.g. 0.82 m).",
                            "default": 0.82
                        }
                    },
                    "required": ["pat_ms"]
                }
            }
        ]
    }


def handle_request(client: PulseArrivalTimeClient, req: Dict[str, Any]) -> Dict[str, Any]:
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": get_tools_manifest()
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})

        if name == "evaluate_pulse_transit":
            res = client.evaluate_pulse_transit(
                pat_ms=float(args.get("pat_ms", 210.0)),
                pre_ejection_period_ms=float(args.get("pre_ejection_period_ms", 85.0)),
                arterial_path_length_m=float(args.get("arterial_path_length_m", 0.82))
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(res, indent=2)
                        }
                    ]
                }
            }
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": f"Method {name} not found"
                }
            }
    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {
                "code": -32600,
                "message": "Invalid request"
            }
        }


def main():
    client = PulseArrivalTimeClient()
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(client, req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": str(e)}
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
