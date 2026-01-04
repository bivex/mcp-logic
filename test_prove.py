#!/usr/bin/env python3
import json
import subprocess
import sys

def test_prove_tool():
    # MCP request for the prove tool
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "prove",
            "arguments": {
                "premises": ["all x (man(x) -> mortal(x))", "man(socrates)"],
                "conclusion": "mortal(socrates)"
            }
        }
    }

    # Convert to JSON and add newline
    request_json = json.dumps(request) + "\n"

    # Start the MCP server process
    server_cmd = [
        "uv", "--directory", "src/mcp_logic", "run", "mcp_logic",
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

        # Send the request
        process.stdin.write(request_json)
        process.stdin.flush()

        # Read response
        response = process.stdout.readline()
        if response:
            print("Response from MCP-Logic prove tool:")
            print(json.dumps(json.loads(response), indent=2))

        # Clean up
        process.terminate()
        process.wait(timeout=5)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_prove_tool()
