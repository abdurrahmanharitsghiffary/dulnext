# Issue

- Show Load More button on List View when page_length already reached end:

  - If we set the page_length to 20 when accessing doctype list page, when items is 20 and start == 20 it still show Load More Button, which shouldn't be there because the items already reached end.

    **Possible cause**:
    - Frappe logic.
    - Our implementation.
