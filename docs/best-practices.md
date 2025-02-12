# Best Practices

All `RestController` and `DatabaseController` implementations should inherit from the `VirtualController`, which is the base controller for Virtual Doctypes. By following these conventions, you won't have to manually map every field from the API response yourself.

## RestController Usage

Consider a REST API response in the following format:

```json
{
  "name": {
    "first_name": "Jamal",
    "last_name": "Boolean"
  },
  "age": 10,
  "friend_names": [
    {
      "name": {
        "first_name": "Juki",
        "last_name": "Boolean"
      }
    }
  ],
  "list_of_family_names": ["Jimmy", "Aimu", "Hatsune", "Miku"]
}
```

## Creating Virtual Doctypes

For the above response, you should create two Virtual Doctypes:

1. **Person**: This doctype contains all the user information.
2. **Person Friends**: This is an editable grid table that contains the names of the user's friends.

## Naming Conventions for Docfields

When designing the `Person` doctype, follow these naming conventions for your Docfields:

- **Field Prefix**:
All field names should begin with the prefix `df`.

- **Nested Fields**:
For nested fields (e.g., `name.first_name`), replace the dot (.) with the string dot since Frappe will remove the actual dot.
**Example**:

- `name.first_name` becomes `dfnamedotifirst_name`
- `name.last_name` becomes `dfnamedotlast_name`

- Array Fields:
For fields that are arrays of strings (e.g., `list_of_family_names`), use the prefix `idxdf` to mark them as such.
**Example**:

- `list_of_family_names` becomes `idxdflist_of_family_names`
The values in these fields will be displayed as comma-separated strings (e.g., `"sample, sampletwo, sample3"`).
While a multi-select table might be a more robust solution for handling arrays, this simple naming convention works well for basic scenarios.
- Simple Fields:
For standard fields (e.g., `age`), simply prefix with `df`.
Example:

- `age` becomes `dfage`

## Adding Custom Field Names in the Doctype

While it is generally recommended to follow the established naming conventions, there may be situations where you need to use a custom field name that doesn't conform. Please note: deviating from the conventions requires you to manually map and implement additional methods, which can become cumbersome over time.

## Example: Overriding the Mapper Method

To handle a custom field name (e.g., `custom_name`), you can override the `mapper` method in your Virtual Doctype class. For instance:

```python
class CustomVirtualDoctype(RestController):
    def mapper(self, response):
        # First, perform the standard mapping for convention-based fields.
        super().mapper(response)

        # Manually map the custom field that does not follow the naming conventions.
        self.custom_name = response.custom_name
```

---

By adhering to these conventions, you ensure that your Virtual Doctypes are structured consistently, making them easier to manage and ensuring Frappe processes them correctly.
