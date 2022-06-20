"""Module for pdfpop mapping."""


def map_fields(fields: dict[str, str], data: dict[str, str]) -> dict[str, str]:
    """Build a dictionary of field keys to interpreted values."""

    def get_code_template() -> str:
        return "def fn(data):\n    %s\nrv = fn(data)\n"

    mapped_fields = {}
    print("\nEvent Log:")
    ignore_list = []
    for key, value in fields.items():
        if value is None:
            ignore_list.append(key)
        elif value in data:
            print(f'Set field "{key}" to "{data[value]}"')
            mapped_fields[key] = data[value]
        else:
            global_env = {}
            local_env = {"data": data}
            full_expr = get_code_template() % value
            exec(full_expr, global_env, local_env)
            print(f'Set field "{key}" to "{local_env["rv"]}"')
            mapped_fields[key] = local_env["rv"]
    for key in ignore_list:
        print(f'Ignored field "{key}"')
    return mapped_fields
