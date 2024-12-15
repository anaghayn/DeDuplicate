import json
from datetime import datetime
import argparse

from datetime import timezone

def parse_date(date_str):
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except ValueError:
        # Fix malformed timezone if necessary
        if date_str.endswith("+00:0"):
            date_str = date_str[:-4] + "+00:00"
        return datetime.fromisoformat(date_str)


# Load JSON data
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Save JSON data
def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# De-duplicate leads
def deduplicate_leads(leads):
    unique_by_id = {}
    unique_by_email = {}
    logs = []

    for lead in leads:
        existing_lead = unique_by_id.get(lead["_id"]) or unique_by_email.get(lead["email"])

        if existing_lead:
            # Resolve conflicts
            current_date = parse_date(lead["entryDate"])
            existing_date = parse_date(existing_lead["entryDate"])
            
            if current_date > existing_date or (
                current_date == existing_date and lead not in unique_by_id.values()
            ):
                log_entry = {
                    "source_record": existing_lead,
                    "output_record": lead,
                    "field_changes": {
                        key: {"from": existing_lead[key], "to": lead[key]} 
                        for key in lead.keys() 
                        if lead[key] != existing_lead[key]
                    },
                }
                logs.append(log_entry)
                unique_by_id[lead["_id"]] = lead
                unique_by_email[lead["email"]] = lead
        else:
            unique_by_id[lead["_id"]] = lead
            unique_by_email[lead["email"]] = lead

    # Consolidate unique records
    deduplicated = list({id: lead for id, lead in unique_by_id.items()}.values())
    return deduplicated, logs

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="De-duplicate leads in JSON file.")
    parser.add_argument("input_file", help="Path to the input JSON file.")
    parser.add_argument("output_file", help="Path to save the deduplicated JSON file.")
    parser.add_argument("log_file", help="Path to save the change log.")

    args = parser.parse_args()

    # Load leads from file
    data = load_json(args.input_file)
    leads = data.get("leads", [])

    # Deduplicate leads
    deduplicated_leads, change_logs = deduplicate_leads(leads)

    # Save deduplicated leads
    save_json({"leads": deduplicated_leads}, args.output_file)

    # Save logs
    save_json(change_logs, args.log_file)

    print(f"Deduplication complete. Output saved to {args.output_file} and logs to {args.log_file}.")
