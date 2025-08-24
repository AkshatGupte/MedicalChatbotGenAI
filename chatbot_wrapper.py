import sys
import json
import os
from dotenv import load_dotenv

# Import your existing chain logic
from chain_logic import process_medical_query

load_dotenv()

def main():
    # Initialize the chatbot (this loads your chain.ipynb logic)
    print("Initializing medical chatbot...")
    print("ready")  # Signal that we're ready to receive queries
    
    try:
        # Keep the process alive and listen for queries
        while True:
            # Read query from stdin
            query = input().strip()
            
            if not query:
                continue
                
            try:
                # Process the query using your existing chain.ipynb logic
                response = process_medical_query(query)
                
                # Send response back
                print(json.dumps({
                    "response": response,
                    "status": "success"
                }))
                
            except Exception as e:
                print(json.dumps({
                    "error": str(e),
                    "status": "error"
                }))
                
    except KeyboardInterrupt:
        print("Shutting down...")
    except EOFError:
        print("Input stream closed")

if __name__ == "__main__":
    main()
