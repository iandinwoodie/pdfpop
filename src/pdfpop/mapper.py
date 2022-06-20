"""Module for pdfpop mapping."""


def _wrap_logic(logic: str) -> str:
    """Returns a function wrapping the given logic."""
    if "return" in logic:
        return f"def fn(data):\n    {logic}\nrv = fn(data)\n"
    return f"rv = {logic}\n"


def map_fields(fields: dict[str, str], data: dict[str, str]) -> dict[str, str]:
    """Build a dictionary of field keys to interpreted values."""
    mapped_fields = {}
    print("\nEvent Log:")
    ignore_list = []
    for key, value in fields.items():
        if value is None:
            ignore_list.append(key)
            continue
        elif value in data:
            mapped_fields[key] = data[value]
        elif isinstance(value, int) or isinstance(value, float):
            mapped_fields[key] = value
        else:
            global_env = {}
            local_env = {"data": data}
            expr = _wrap_logic(value)
            exec(expr, global_env, local_env)
            rv = local_env["rv"]
            mapped_fields[key] = rv if rv is not None else value
        print(f'Set field "{key}" to "{mapped_fields[key]}"')
    for key in ignore_list:
        print(f'Ignored field "{key}"')
    return mapped_fields
