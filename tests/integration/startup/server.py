import subprocess
from asyncio.subprocess import PIPE, STDOUT
from tests.helpers.all import get_root
import asyncio


class Server:
    def __init__(self, skip) -> None:
        self.skip = skip

    async def start_server(self) -> None:
        print(f"in server")
        if not await self._check_if_server_is_up():
            await self.launch_server()

    async def launch_server(self):
        cmd = "docker-compose -f docker-compose_testing.yml -p chronicler_testing up -d"
        up = await self.command(cmd)
        assert up.returncode == 0
        assert await self._check_if_server_is_up()

    async def teardown_server(self) -> None:
        if self.skip is not False and await self._check_if_server_is_up() is True:
            await self.stop_server()
            await self.delete_volume()
        else:
            print(f"skipping tear down..")

    async def stop_server(self):
        down = await self.command(
            "docker-compose -f docker-compose_testing.yml -p chronicler_testing down"
        )
        assert down.returncode == 0
        assert not await self._check_if_server_is_up()

    async def delete_volume(self):
        delete = await self.command("docker volume rm chronicler_volume_test")
        assert delete.returncode == 0
        assert not await self._check_if_volume_exists()

    async def _check_if_volume_exists(self):
        check = await self.command("docker volume ls")
        return "chronicler_volume_test" in str(check.stdout)

    async def _check_if_server_is_up(self):
        check = await self.command("docker ps")
        return all([self._db_is_up(check), self._rest_is_up(check)])

    def _db_is_up(self, check):
        return "chronicler_host_test" in str(check.stdout)

    def _rest_is_up(self, check):
        return "rest-server_test" in str(check.stdout)

    async def command(self, cmd: str) -> str:
        """
        Run a terminal command in a subprocess and return the output

        :param cmd: The command to run
        """

        return await asyncio.to_thread(
            subprocess.run,
            cmd,
            stdout=PIPE,
            stderr=STDOUT,
            shell=True,
            cwd=(get_root(__file__)),
        )
