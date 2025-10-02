import requests
import time

# --- Configuration ---
BASE_URL = "http://127.0.0.1:8000"


def fetch_all_paginated_data(api_path: str, data_key: str) -> list:
    """
    A generic function to fetch all items from a paginated endpoint.

    Args:
        api_path: The API path to call (e.g., "/manufacturers").
        data_key: The key in the JSON response that holds the list of items
                  (e.g., "manufacturers", "categories", "models").
    """
    all_items = []
    current_page = 1
    total_pages = 1  # Will be updated after the first API call

    while current_page <= total_pages:
        # We use a large per_page value to reduce the number of API calls
        url = f"{BASE_URL}{api_path}?page={current_page}&per_page=100"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            items_on_page = data.get(data_key, [])
            if not items_on_page and current_page > 1:
                break  # Stop if we get an empty page

            all_items.extend(items_on_page)

            if current_page == 1:
                total_pages = data.get("meta", {}).get("page_count", 1)

            current_page += 1
            # A small delay to avoid overwhelming the server
            time.sleep(0.1)

        except requests.exceptions.RequestException as e:
            print(f"\nError fetching data from {url}: {e}")
            # Decide if you want to stop or continue
            return []  # Returning empty list on error

    return all_items


def discover_all_model_ids():
    """
    Traverses the API hierarchy to find all model IDs.
    """
    print("--- Starting Model ID Discovery ---")
    all_model_ids = set()  # Use a set to automatically handle duplicates

    # 1. Fetch all manufacturers
    print("\n[Step 1/3] Fetching all manufacturers...")
    manufacturers = fetch_all_paginated_data("/manufacturers", "manufacturers")
    if not manufacturers:
        print("Could not fetch manufacturers. Aborting.")
        return
    print(f"Found {len(manufacturers)} manufacturers.")

    # 2. For each manufacturer, fetch its categories
    print("\n[Step 2/3] Fetching categories for each manufacturer...")
    all_categories = []
    for i, manu in enumerate(manufacturers):
        manu_id = manu['id']
        manu_name = manu.get('name', f'ID {manu_id}')
        print(f"  - ({i + 1}/{len(manufacturers)}) Fetching categories for '{manu_name}'...")

        categories = fetch_all_paginated_data(
            f"/manufacturers/{manu_id}/categories", "categories"
        )
        all_categories.extend(categories)
    print(f"Found a total of {len(all_categories)} categories.")

    # 3. For each category, fetch its models and collect their IDs
    print("\n[Step 3/3] Fetching models for each category...")
    for i, cat in enumerate(all_categories):
        cat_id = cat['id']
        cat_name = cat.get('name', f'ID {cat_id}')
        print(f"  - ({i + 1}/{len(all_categories)}) Fetching models for category '{cat_name}'...")

        models = fetch_all_paginated_data(
            f"/categories/{cat_id}/models", "models"
        )

        # Add the IDs of the found models to our set
        for model in models:
            all_model_ids.add(model['id'])

    print("\n--- Discovery Complete ---")

    if not all_model_ids:
        print("No model IDs were found.")
        return

    # Convert set to a sorted list for clean display
    sorted_ids = sorted(list(all_model_ids))

    print(f"Found a total of {len(sorted_ids)} unique model IDs.")
    print("List of all discovered model IDs:")
    print(sorted_ids)


if __name__ == "__main__":
    discover_all_model_ids()