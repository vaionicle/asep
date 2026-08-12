
def parse_int(input):
    return int(parse_float(input))

def parse_float(value):
    if value is None or value == "":
        return 0.0

    if isinstance(value, (int, float)):
        return float(value)

    return float(str(value).strip().replace(",", "."))