from datetime import datetime
from datetime import timezone


def parse_landsat_datetime(
    date_str: str,
    time_str: str
) -> datetime:
    time_str = time_str.strip()

    if time_str.endswith("Z"):
        time_str = time_str[:-1]

    if "." in time_str:

        base, frac = time_str.split(".", 1)

        frac = frac[:6].ljust(6, "0")

        timestamp = (
            f"{date_str}T{base}.{frac}"
        )

        dt = datetime.strptime(
            timestamp,
            "%Y-%m-%dT%H:%M:%S.%f"
        )

    else:

        timestamp = (
            f"{date_str}T{time_str}"
        )

        dt = datetime.strptime(
            timestamp,
            "%Y-%m-%dT%H:%M:%S"
        )

    return dt.replace(
        tzinfo=timezone.utc
    )
