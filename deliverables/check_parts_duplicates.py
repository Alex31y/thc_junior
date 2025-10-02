import requests
from collections import defaultdict

# --- Configuration ---
BASE_URL = "http://127.0.0.1:8000"
START_MODEL_ID = 1
END_MODEL_ID = 1230  # Based on previous discovery


def fetch_all_parts(model_id: int) -> list | None:
    """
    Fetches all parts for a given model_id, handling pagination.
    Returns the list of parts, or None if the model doesn't exist or an error occurs.
    """
    all_parts = []
    current_page = 1
    total_pages = 1

    while current_page <= total_pages:
        api_url = f"{BASE_URL}/models/{model_id}/parts?page={current_page}&per_page=100"
        try:
            response = requests.get(api_url, timeout=10)
            if response.status_code == 404:
                return None  # Model does not exist, signal to skip

            response.raise_for_status()  # Raise an exception for other bad statuses
            data = response.json()
            parts_on_page = data.get("parts", [])

            if not parts_on_page and current_page > 1:
                break

            all_parts.extend(parts_on_page)

            if current_page == 1:
                total_pages = data.get("meta", {}).get("page_count", 1)

            current_page += 1

        except requests.exceptions.RequestException as e:
            print(f"\n[ERROR] API request failed for model {model_id}: {e}")
            return None  # Signal error

    return all_parts


def find_duplicate_numbers(parts_list: list) -> dict:
    """
    Identifies part numbers that are used by more than one part.
    Returns a dictionary mapping the duplicate number to the list of part IDs that share it.
    """
    groups = defaultdict(list)
    for part in parts_list:
        if part_number := part.get("number"):   #  this if block will only run if a part number exists and is not empty
            groups[part_number].append(part['id'])

    # Filter for numbers that appear more than once
    return {number: ids for number, ids in groups.items() if len(ids) > 1}


def print_summary_report(models_with_issues: dict):
    """Prints a final, clean summary of all issues found."""
    print("\n" + "=" * 60)
    print("           DATA QUALITY AUDIT: FINAL REPORT")
    print("=" * 60)

    if not models_with_issues:
        print("\n   SUCCESS: No data quality issues found.")
        print("   - All part numbers are distinct within their models.")
        print("   - No suspiciously incomplete part names were detected.")
        return

    print(f"\n  ATTENTION: Found issues in {len(models_with_issues)} model(s).\n")

    for model_id, issues in models_with_issues.items():
        print(f"--- Model ID: {model_id} ---")
        if 'duplicate_numbers' in issues:
            print("  [Issue] Duplicate Part Numbers:")
            for number, ids in issues['duplicate_numbers'].items():
                print(f"    - Number '{number}' is used by part IDs: {ids}")

        if 'incomplete_names' in issues:
            print("  [Issue] Potentially Incomplete Names (single word):")
            for part in issues['incomplete_names']:
                print(f"    - Part ID {part['id']}: Name is '{part['name']}'")
        print("")  # Blank line for readability


def main():
    """
    Main function to run the full data quality test.
    """
    models_with_issues = {}
    total_models = END_MODEL_ID - START_MODEL_ID + 1

    print(f"--- Starting Data Quality Test for Models {START_MODEL_ID} to {END_MODEL_ID} ---")

    for i, model_id in enumerate(range(START_MODEL_ID, END_MODEL_ID + 1)):
        print(f"[Progress: {i + 1}/{total_models}] Checking Model ID: {model_id}...")

        parts = fetch_all_parts(model_id)
        if parts is None:
            continue  # Skip non-existent models or models with fetch errors

        # Run the two specific checks from the bug report
        duplicate_nums = find_duplicate_numbers(parts)

        if duplicate_nums:
            models_with_issues[model_id] = {}
            if duplicate_nums:
                models_with_issues[model_id]['duplicate_numbers'] = duplicate_nums

    # After checking all models, print the final report
    print_summary_report(models_with_issues)


if __name__ == "__main__":
    main()