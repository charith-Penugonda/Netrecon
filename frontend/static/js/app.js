function startScan() {
    var target = document.getElementById('target').value.trim();
    var scan_type = document.getElementById('scan_type').value;

    if (!target) {
        alert('Please enter a target');
        return;
    }

    document.getElementById('scan-btn').disabled = true;
    document.getElementById('scan-btn').innerText = 'Scanning...';
    document.getElementById('status-box').style.display = 'block';
    document.getElementById('status-msg').innerText = 'Scanning ' + target + ' please wait...';
    document.getElementById('results-box').style.display = 'none';

    fetch('/api/scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target: target, scan_type: scan_type })
    })
    .then(function(res) { return res.json(); })
    .then(function(data) {
        document.getElementById('scan-btn').disabled = false;
        document.getElementById('scan-btn').innerText = 'Start Scan';
        document.getElementById('status-box').style.display = 'none';
        showResults(data);
    })
    .catch(function(err) {
        document.getElementById('scan-btn').disabled = false;
        document.getElementById('scan-btn').innerText = 'Start Scan';
        document.getElementById('status-box').style.display = 'none';
        alert('Error: ' + err.message);
    });
}

function showResults(data) {
    document.getElementById('results-box').style.display = 'block';

    var s = data.summary;
    var summaryHtml = '<div class="summary">';
    summaryHtml += '<p>Target: ' + s.target + '</p>';
    summaryHtml += '<p>Scan Type: ' + s.scan_type + '</p>';
    summaryHtml += '<p>Timestamp: ' + s.timestamp + '</p>';
    summaryHtml += '<p>Total Hosts: ' + s.total_hosts + '</p>';
    summaryHtml += '<p>Open Ports: ' + s.open_ports_count + '</p>';
    summaryHtml += '</div>';
    document.getElementById('summary').innerHTML = summaryHtml;

    var hostsHtml = '';
    data.hosts.forEach(function(host) {
        hostsHtml += '<div class="host-card">';
        hostsHtml += '<h3>' + host.ip + ' (' + host.hostname + ')</h3>';
        hostsHtml += '<p>State: ' + host.state + '</p>';
        hostsHtml += '<table class="port-table">';
        hostsHtml += '<tr><th>Port</th><th>Protocol</th><th>State</th><th>Service</th></tr>';

        host.open_ports.forEach(function(port) {
            var stateClass = port.state === 'open' ? 'open' : 'closed';
            hostsHtml += '<tr>';
            hostsHtml += '<td>' + port.port + '</td>';
            hostsHtml += '<td>' + port.protocol + '</td>';
            hostsHtml += '<td class="' + stateClass + '">' + port.state + '</td>';
            hostsHtml += '<td>' + port.service + '</td>';
            hostsHtml += '</tr>';
        });

        hostsHtml += '</table></div>';
    });

    document.getElementById('hosts').innerHTML = hostsHtml;
    loadHistory();
}

function loadHistory() {
    fetch('/api/scans')
    .then(function(res) { return res.json(); })
    .then(function(scans) {
        var html = '';
        scans.forEach(function(scan) {
            html += '<div class="history-item">';
            html += '<p>Target: ' + scan.target + '</p>';
            html += '<p>Type: ' + scan.scan_type + '</p>';
            html += '<p>Date: ' + scan.created_at + '</p>';
            html += '</div>';
        });
        document.getElementById('history').innerHTML = html || '<p>No scans yet</p>';
    });
}

window.onload = function() {
    loadHistory();
};
