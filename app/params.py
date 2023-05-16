from dataclasses import dataclass, field, fields
from typing import Self

from app.parser.cmd import parse_params_from_args, parse_env_path_from_args
from app.parser.env import parse_params_from_env
from app.exceptions import CustomValueException, NotAllParamsException


@dataclass()
class Params:
    min: int = 0
    max: int = 0
    api_id: int = 0
    api_hash: str = ''
    chat_ids: list[int] = field(default_factory=lambda: [])
    channel_ids: list[int] = field(default_factory=lambda: [])

    @property
    def _unfilled_fields(self) -> list[str]:
        unfilled_fields = []
        for fld in fields(self):
            fld_value = getattr(self, fld.name)
            if not fld_value:
                unfilled_fields.append(fld.name)
        return unfilled_fields

    @property
    def _empty_fields(self) -> list[str]:
        empty_fields = self._unfilled_fields.copy()
        if 'min' in empty_fields:  # min can be set to default
            empty_fields.remove('min')
        if 'chat_ids' in empty_fields or 'channel_ids' in empty_fields:
            if 'chat_ids' in empty_fields: empty_fields.remove('chat_ids')
            if 'channel_ids' in empty_fields: empty_fields.remove('channel_ids')
        return empty_fields

    def update(self, other_params: Self) -> Self:
        for fld in fields(self):
            other_params_field = getattr(other_params, fld.name)
            if other_params_field:
                setattr(self, fld.name, other_params_field)
        return Self

    def validate(self) -> None:
        if self._empty_fields:
            msg = f'You have not provided: {self._empty_fields}'
            raise NotAllParamsException(msg)
        if self.max < self.min:
            msg = 'Provided max value is less than min value'
            raise CustomValueException(msg)

    def __str__(self) -> str:
        return (
            f'Params(min={self.min}, '
            f'max={self.max}, '
            f'api_id={self.api_id}, '
            f'api_hash={self.api_hash}, '
            f'chat_ids={self.chat_ids}), '
            f'channel_ids={self.channel_ids}), '
        )


def get_params() -> Params:
    env_path = parse_env_path_from_args()
    params = Params(**parse_params_from_env(env_path))
    args = Params(**parse_params_from_args())
    params.update(args)
    params.validate()
    return params
