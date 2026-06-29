import json

def parse_scan_result(result):

    if result.get("error"):
        return {
            "success": False,
            "error": result["error"],
            "summary": None,
            "hosts": []
        }

    hosts = result.get("hosts", [])
    total_hosts = len(hosts)
    open_ports_count = 0
    host_summaries = []

    for host in hosts:
        open_ports = [p for p in host["ports"] if p["state"] == "open"]
        open_ports_count += len(open_ports)

        host_summaries.append({
            "ip":         host["ip"],
            "hostname":   host["hostname"],
            "state":      host["state"],
            "open_ports": open_ports,
            "total_ports_scanned": len(host["ports"]),
        })

    return {
        "success": True,
        "error":   None,
        "summary": {
            "target":           result["target"],
            "scan_type":        result["scan_type"],
            "timestamp":        result["timestamp"],
            "total_hosts":      total_hosts,
            "open_ports_count": open_ports_count,
        },
        "hosts": host_summaries
    }

if __name__ == "__main__":
    sample = {
        "target": "scanme.nmap.org",
        "scan_type": "basic",
        "timestamp": "2026-01-01T00:00:00",
        "error": None,
        "hosts": [
            {
                "ip": "45.33.32.156",
                "hostname": "scanme.nmap.org",
                "state": "up",
                "ports": [
                    {"port": 22, "protocol": "tcp", "state": "open", "service": "ssh", "product": "", "version": ""},
                    {"port": 80, "protocol": "tcp", "state": "open", "service": "http", "product": "", "version": ""},
                    {"port": 443, "protocol": "tcp", "state": "closed", "service": "https", "product": "", "version": ""},
                ]
            }
        ]
    }
    parsed = parse_scan_result(sample)
    print(json.dumps(parsed, indent=2))
