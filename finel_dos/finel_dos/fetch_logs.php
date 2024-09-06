<?php
// fetch_logs.php

header('Content-Type: application/json');

$file = 'log.txt';

function parse_logs($file) {
    $logs = [];
    if (file_exists($file)) {
        $contents = file_get_contents($file);
        $entries = explode("\n\n", trim($contents));

        foreach ($entries as $entry) {
            preg_match('/Timestamp: (.+)/', $entry, $timestamp);
            preg_match('/Risk Level: (.+)/', $entry, $risk);
            preg_match('/IP: (.+)/', $entry, $ip);

            $headers = [];
            preg_match_all('/^([\w-]+): (.+)$/m', $entry, $matches, PREG_SET_ORDER);
            foreach ($matches as $match) {
                $headers[$match[1]] = $match[2];
            }

            if ($timestamp && $risk && $ip) {
                $logs[] = [
                    'timestamp' => $timestamp[1],
                    'risk' => $risk[1],
                    'ip' => $ip[1],
                    'headers' => $headers
                ];
            }
        }
    }
    return $logs;
}

echo json_encode(['logs' => parse_logs($file)]);
?>
