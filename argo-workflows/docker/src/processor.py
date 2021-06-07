import json
import argparse
import os

parser = argparse.ArgumentParser(description='Processor input parse.')
parser.add_argument('event', metavar='event', type=str, nargs='+', help='passed event')

def handler(event, context):
    json_event = None
    with open(event) as f:
        json_event = json.load(f)

    print(f"Processor received event: {json_event}")

    # record the job execution result into a file    
    with open('processor_event.json', 'w') as f:
        json.dump(json_event, f, ensure_ascii=False)

    return event

if __name__ == "__main__":
    args = parser.parse_args()
    event = args.event[0]
    handler(event, "context")
