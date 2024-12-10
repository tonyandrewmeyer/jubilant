"""Jubilant is a Pythonic wrapper around the Juju CLI for integration testing."""

import json
import subprocess
import time
import typing

from ._types import Status

__all__ = [
    'Juju',
    'Status',
]

__version__ = '0.0.0a1'


class Juju:
    """TODO."""

    def __init__(self, *, model: str | None = None):
        self.model = model

    def __repr__(self):
        args = []
        if self.model is not None:
            args.append(f'model={self.model!r}')
        return f'Juju({", ".join(args)})'

    def cli(self, *args: str) -> str:
        """TODO."""
        # TODO: good error handling and include stderr in exception
        process = subprocess.run(
            ['juju', *args], check=True, capture_output=True, encoding='UTF-8'
        )
        return process.stdout

    def add_model(
        self,
        model_name: str,  # TODO: should this use self.model if set, and set it if not?
        *,
        controller: str | None = None,
        config: dict[str, typing.Any] | None = None,  # TODO: is Any correct here?
    ) -> None:
        """TODO."""
        args = ['add-model', model_name]

        if controller is not None:
            args.extend(['--controller', controller])
        if config is not None:
            for k, v in config.items():
                args.extend(['--config', f'{k}={v}'])

        self.cli(*args)

    def destroy_model(
        self,
        model_name: str,
        *,
        force=False,
    ):
        """TODO."""
        args = ['destroy-model', model_name, '--no-prompt']
        if force:
            args.append('--force')
        self.cli(*args)

    def deploy(
        self,
        charm_name: str,
        application_name: str | None = None,
        *,
        model: str | None = None,
        config: dict[str, typing.Any] | None = None,  # TODO: is Any correct here?
        num_units: int = 1,
        resources: dict[str, str] | None = None,
        trust: bool = False,
        # TODO: include all the arguments we think people we use
    ) -> None:
        """TODO."""
        args = ['deploy', charm_name]
        if application_name is not None:
            args.append(application_name)

        if model is None:
            model = self.model
        if model is not None:
            args.extend(['--model', model])
        if config is not None:
            for k, v in config.items():
                args.extend(['--config', f'{k}={v}'])
        if num_units != 1:
            args.extend(['--num-units', str(num_units)])
        if resources is not None:
            for k, v in resources.items():
                args.extend(['--resource', f'{k}={v}'])
        if trust:
            args.append('--trust')

        self.cli(*args)

    def status(
        self,
        *,
        model: str | None = None,
    ) -> Status:
        """TODO."""
        args = ['status', '--format', 'json']

        if model is None:
            model = self.model
        if model is not None:
            args.extend(['--model', model])

        stdout = self.cli(*args)
        result = json.loads(stdout)
        return Status.from_dict(result)

    def wait_status(
        self,
        ready_func: typing.Callable[[Status], bool],
        *,
        model: str | None = None,
        timeout: float = 10 * 60,
        delay: float = 1,
        successes: int = 3,
    ) -> Status:
        """TODO."""
        start = time.time()
        success_count = 0
        this_status = None
        while time.time() - start < timeout:
            this_status = self.status(model=model)
            #        logger.info('wait_status: %s', this_status)  # TODO: ensure better debugging
            print('TODO wait_status', this_status)
            if ready_func(this_status):
                success_count += 1
                if success_count >= successes:
                    return this_status
            else:
                success_count = 0
            time.sleep(delay)
        raise Exception(f'timed out after {timeout}, last status:\n{this_status}')
