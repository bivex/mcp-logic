#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, 'src')

from mcp_logic.server import LogicEngine

def test_prove_directly():
    # Initialize the logic engine
    engine = LogicEngine("/Volumes/External/Code/mcp-logic/ladr/bin")

    # Create input file for the syllogism
    premises = ["all x (man(x) -> mortal(x))", "man(socrates)"]
    conclusion = "mortal(socrates)"

    # Create the input file
    input_file = engine._create_input_file(premises, conclusion)

    print("Testing the famous syllogism:")
    print("Premises:")
    for premise in premises:
        print(f"  {premise}")
    print(f"Conclusion: {conclusion}")
    print()

    # Run the proof
    result = engine._run_prover(input_file)

    print("Result:")
    print(f"Status: {result['result']}")
    if 'proof' in result:
        print("Proof found!")
        print("Proof details:")
        print(result['proof'][:500] + "..." if len(result['proof']) > 500 else result['proof'])

    return result

if __name__ == "__main__":
    test_prove_directly()
