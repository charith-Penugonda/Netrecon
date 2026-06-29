import subprocess
import xml.etree.ElementTree as ET
import datetime
import json

def run_scan(target, scan_type="basic"):

    scan_profiles = {
        "basic": ["-sT", "-p", "22,80,443,8080,3306,5432", "-T4"],
        "full":  ["-sT", "-p", "1-1000", "-T4"],
        "ping":  ["-sT", "-p", "80,443", "-T4"],
    }

    args = scan_profiles.get(scan_type, scan_profiles["basic"])

    cmd = ["nmap", "-oX", "-"] + args + [target]

    result = {
        "target":    target,
        "scan_type": scan_type,
        "timestamp": datetime.datetime.now().isoformat(),
        "hosts":     [],
        "error":     None
    }

    try:
        output = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )

        if output.returncode != 0:
            result["error"] = output.stderr
            return result

        root = ET.fromstring(output.stdout)

        for host in root.findall("host"):
            addr = host.find("address")
            if addr is None:
                continue

            ip = addr.get("addr", "")
            state_el = host.find("status")
            state = state_el.get("state", "") if state_el is not None else ""

            hostname = ""
            hn = host.find("hostnames/hostname")
            if hn is not None:
                hostname = hn.get("name", "")

            ports_list = []
            ports_el = host.find("ports")
            if ports_el is not None:
                for port in ports_el.findall("port"):
                    state_p = port.find("state")
                    service = port.find("service")
                    ports_list.append({
                        "port":     int(port.get("portid", 0)),
                        "protocol": port.get("protocol", ""),
                        "state":    state_p.get("state", "") if state_p is not None else "",
                        "service":  service.get("name", "") if service is not None else "",
                        "product":  service.get("product", "") if service is not None else "",
                        "version":  service.get("version", "") if service is not None else "",
                    })

            result["hosts"].append({
                "ip":       ip,
                "hostname": hostname,
                "state":    state,
                "ports":    ports_list,
            })

    except subprocess.TimeoutExpired:
        result["error"] = "Scan timed out"
    except ET.ParseError as e:
        result["error"] = "XML parse error: " + str(e)
    except Exception as e:
        result["error"] = "Error: " + str(e)

    return result

if __name__ == "__main__":
    r = run_scan("scanme.nmap.org", "basic")
    print(json.dumps(r, indent=2))

