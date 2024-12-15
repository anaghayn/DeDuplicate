### Deduplicate Data
This project implements a command-line program to de-duplicate JSON records according to the following rules:

1. The data from the newest date is preferred.
2. Duplicate IDs and emails count as duplicates and must be unique.
3. If dates are identical, the last record in the list is preferred.

### File Descriptions

- **`deduplicate.py`**: Script that removes duplicate records from a JSON dataset. Duplicate records are determined by `_id` or `email`, and the newest `entryDate` is preferred.
- **`leads.json`**: Input JSON file containing the dataset to be deduplicated.
- **`deduplicated_leads.json`**: Output JSON file with duplicates resolved and only unique records remaining.
- **`change_log.json`**: Log file documenting all changes made during deduplication, including original records, resolved records, and field-level updates.
 
