#!/usr/bin/env python

import sys

from tokenizer import tokenize

from parser import parse

from evaluator import evaluate

def main():
    environment = {}
    debug_config = {"watch": None} # Initialize debug config
    
    # Parse command-line arguments for debug options
    source_file = None
    for arg in sys.argv[1:]:
        if arg.startswith("watch="):
            debug_config["watch"] = arg.split("=", 1)[1]
        else:
            source_file = arg
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        # Filename provided, read and execute it
        with open(sys.argv[1], 'r') as f:
            source_code = f.read()
        try:
            tokens = tokenize(source_code)
            ast = parse(tokens)
            final_value, exit_status = evaluate(ast, environment)
            if exit_status == "exit":
                # print(f"Exiting with code: {final_value}") # Optional debug print
                sys.exit(final_value if isinstance(final_value, int) else 0)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1) # Indicate error to OS
    else:
        # REPL loop
        while True:
            try:
                # Read input
                source_code = input('>> ')

                # Exit condition for the REPL loop
                if source_code.strip() in ['exit', 'quit']:
                    break

                # Tokenize, parse, and execute the code
                tokens = tokenize(source_code)
                ast = parse(tokens)
                final_value, exit_status = evaluate(ast, environment)
                if exit_status == "exit":
                    print(f"Exiting with code: {final_value}") # REPL can print this
                    sys.exit(final_value if isinstance(final_value, int) else 0)
                elif final_value is not None: # Print result in REPL if not None
                    print(final_value)
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()
