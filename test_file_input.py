#!/usr/bin/env python3
"""
Test script for MCP-Logic file input functionality
"""
import json
import subprocess
import time
import signal
import os

def test_file_input():
    # MCP request for the prove tool using file input
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "prove",
            "arguments": {
                "input_file": "/Volumes/External/Code/mcp-logic/test_syllogism.in"
            }
        }
    }

    # Convert to JSON
    request_json = json.dumps(request) + "\n"

    # Start the MCP server process
    server_cmd = [
        "uv", "run", "--directory", "src/mcp_logic", "mcp_logic",
        "--prover-path", "/Volumes/External/Code/mcp-logic/ladr/bin"
    ]

    try:
        # Start the server
        process = subprocess.Popen(
            server_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd="/Volumes/External/Code/mcp-logic"
        )

        # Give server time to start
        time.sleep(2)

        # Send the request
        process.stdin.write(request_json)
        process.stdin.flush()

        # Read response
        response = process.stdout.readline()
        if response:
            print("Response from MCP-Logic prove tool (file input):")
            try:
                parsed = json.loads(response)
                if "result" in parsed and parsed["result"] == "proved":
                    print("✅ SUCCESS: Theorem proved using file input!")
                    print("The syllogism 'All men are mortal, Socrates is a man, therefore Socrates is mortal' was successfully proved.")
                else:
                    print("❌ Result:", json.dumps(parsed, indent=2))
            except json.JSONDecodeError:
                print("Raw response:", response)
        else:
            print("No response received")

        # Clean up
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_file_input()
