from argparse import ArgumentParser, ArgumentTypeError
from typing import Callable


def int_range(min_: int, max_: int) -> Callable:
    def int_range_checker(arg) -> int:
        try:
            value = int(arg)
        except ValueError:
            raise ArgumentTypeError('Must be an integer')
        if value < min_ or value > max_:
            raise ArgumentTypeError(f'Must be in range [{min_}, {max_}]')
        return value
    return int_range_checker


class CustomParser(ArgumentParser):
    def __init__(self) -> None:
        super().__init__()
        self.parse_auth_group()
        self.parse_tuning_group()
        self.parse_targets_group()
        self.parse_env_group()
        self.validate_mutually_incisive_group('api_id', 'api_hash')

    def validate_mutually_incisive_group(self, *args_keys: str) -> None:
        args = vars(self.parse_known_args()[0])
        if all([args[key] is None for key in args_keys]):
            return
        for key in args_keys:
            if args[key] is None:
                self.error(f'The following argument is required: --{key}')

    def parse_auth_group(self) -> None:
        auth = self.add_argument_group('auth')
        auth.add_argument(
            '-i', '--api_id', type=int, help='Provides telegram api id')
        auth.add_argument(
            '-s', '--api_hash', type=str, help='Provides telegram api hash')

    def parse_tuning_group(self) -> None:
        tuning = self.add_argument_group('tuning')
        tuning.add_argument(
            '-f', '--min', type=int_range(0, 73), default=2,
            help='Provides a minimum quantity of chosen reactions')
        tuning.add_argument(
            '-t', '--max', type=int_range(0, 73), default=42,
            help='Provides a maximum quantity of chosen reactions')

    def parse_targets_group(self):
        targets = self.add_argument_group('targets')
        targets.add_argument(
            '-c', '--chat_ids', type=int, nargs='+',
            help='Provides a list of chat ids')
        targets.add_argument(
            '-v', '--channel_ids', type=int, nargs='+',
            help='Provides a list of channel ids')

    def parse_env_group(self):
        env_path = self.add_argument_group('env_path')
        env_path.add_argument(
            '-e', '--env', type=str,
            help='Provides a path to an .env file')


parser = CustomParser()


def parse_params_from_args() -> dict[str, str | list[str] | None]:
    params = vars(parser.parse_args())
    params.pop('env')
    return params


def parse_env_path_from_args() -> str | None:
    return parser.parse_args().env
