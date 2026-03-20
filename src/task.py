from typing import Any

import attrs


@attrs.frozen
class Task:
    id: str = attrs.field(
        validator=[
            attrs.validators.instance_of(str),
            attrs.validators.min_len(1),
        ]
    )
    payload: dict[str, Any] = attrs.field(
        factory=dict,
        validator=attrs.validators.instance_of(dict),
    )
