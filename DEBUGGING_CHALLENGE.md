# Debugging Challenge for Junior Developer

## Overview
This project contains **two intentionally introduced bugs** that you need to find and fix. This exercise will test your debugging skills and your ability to document your process for other developers.

## Bug Reports

You have been assigned two bug tickets from the support team:

### Bug #1: Incorrect Total Page Count
- **Priority:** Medium
- **Reporter:** Frontend Team
- **Description:** The API pagination metadata is showing incorrect total page counts. When there are 16 manufacturers with per_page=5, the response shows `page_count: 5`. When accessing page 1 to 4, they show data correctly. When accessing page 5, it's empty. Other endpoints seem to have the same issue.

- **Expected:** All pages show items.
- **Actual:** All pages except the last one show items.

### Bug #2: Duplicate Part Data in Database
- **Priority:** High
- **Reporter:** Data Quality Team
- **Description:** After running the scraper, some parts in the database have identical values for both `part_number` and `part_name` fields, when they should contain different information. The part names appear to be missing the descriptive portion.

- **Expected:** Parts should have distinct part numbers and complete names
- **Actual:** Some parts have duplicated `number`, example `CH62A`
- **Actual:** Some parts have a cut-off `name`, example "DOUBLE" (should be something like "DOUBLE-ENDED WRENCH")

## Your Task

For each bug ticket:
1. Reproduce the reported issue
2. Identify the root cause in the code
3. Implement a fix
4. Verify the fix resolves the issue

### 2. Documentation Requirements
After fixing each bug, create a section titled "Debugging Best Practices" that includes:
- General debugging methodology you used
- Useful tools and techniques for this type of project

## Getting Started

1. **Setup the environment:**
   ```bash
   docker compose pull
   docker compose down --volumes
   docker compose up --build
   ```

2. **Test the API endpoints:**
   - Visit http://localhost:8000/docs for interactive API documentation
   - Try different API calls with various parameters
   - Pay attention to error responses and unexpected behavior

## Deliverables

1. **Fixed Code**: Your bug fixes committed to a repository (create one on GitHub, add your fixes as separate commits)
2. **Debugging Best Practices**: A markdown file `[DEBUGGING_BEST_PRACTICES.md` with debugging methodology, useful tools and techniques.

## Evaluation Criteria

- **Problem Solving**: Did you find and fix both bugs correctly?
- **Debugging Process**: Did you use a systematic approach?
- **Documentation Quality**: Is your debugging process clearly documented?
- **Code Quality**: Are your fixes clean and well-reasoned?

Good luck! Remember, the goal is not just to fix the bugs, but to demonstrate your debugging methodology and ability to help other developers.