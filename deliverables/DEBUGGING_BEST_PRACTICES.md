### Bug #1: Incorrect Total Page Count

issue: 
    the proposed value in the field "page_count" in the api response metadata, was actually off by one
    
analysis:
the issue is inside the logic which calculates the total page count for the api response
the actual division itself is right but the issue is incrementing the final value by 1 integer, removing that final
addition is going to solve the issue

existing logic:

    page_count=math.ceil(filtered.count() / per_page) +1,

proposed solution:

    page_count=math.ceil(filtered.count() / per_page),

bugfix commit: "bugfix Incorrect Total Page Count"


### Bug #2: Duplicate Part Data in Database

issue: 
    the scraping logic is not properly assigning values for the attributes "part_number" and "part_name", apparently some instances have duplicated values for part_number and some instances have truncated names for "part_name"

analysis:
    this bug is a little bit trickier to reproduce, the only way to be sure that there are no duplicates is to actually check all data
    there is the issue that I don't actually know how many possible unique model IDs there are
    so first of all I made a script "find_all_models.py" to actually navigate the APIs endpoints to explore the data hierarchy:
            1. Fetch all manufacturers.
            2. Iterate through each manufacturer to fetch their associated categories.
            3. Iterate through each category to fetch its associated models.
            4. Collect all the unique model IDs.
            5. Print a final list of all discovered model IDs.

    Found a total of 1230 unique model IDs.
    List of all discovered model IDs: [1, 2, 3, ..., 1230]

then we got to check for each model ID if we got any duplicate data on the fields "part_number"
to do that i made a script which actually analyzes data retrieved by interrogating the api endpoint "/models/{model_id}/parts" for each of the previously retrieved model_id values

the issue resides in the scraper.py logic
we can see that the actual issue is bad string parsing: the code splits part data by a hyphen. if a part name has more than one hyphen (like DOUBLE-ENDED WRENCH), it breaks.

existing logic row 88:
    
    elements = name.split("-")

proposed solution:

    elements = name.split("-", 1)

bugfix commit: "bugfix Incorrect Total Page Count"

this way we tell the split function to actually split the string at most once on the first hyphen

i dont actually know how to test if the names are now retrieved in full or if they are prematurely truncated

but thanks to the script "check_parts_duplicates.py" we actually know that there are no "part_number" duplicates in the db

    ============================================================
           DATA QUALITY AUDIT: FINAL REPORT
    ============================================================
    
    SUCCESS: No data quality issues found.
    - All part numbers are distinct within their models.
    - No suspiciously incomplete part names were detected.