import os
import subprocess
from asyncio.subprocess import PIPE, STDOUT
from subprocess import CompletedProcess


def command(cmd: str) -> CompletedProcess:
    """
    Run a terminal command in a subprocess and return the output
    :param cmd: The command to run
    """
    return subprocess.run(
        cmd,
        stdout=PIPE,
        stderr=STDOUT,
        shell=True,
        cwd=(os.environ.get("ROOT_DIR_PATH")),
    )

def start() -> CompletedProcess:
    print("starting server")
    return command(os.environ.get("CMD_SERVER_START"))

def quit() -> CompletedProcess:
    return command(os.environ.get("CMD_SERVER_END"))

def server_and_db_are_running() -> bool:
    check = command(os.environ.get("CMD_SERVER_CHECK"))
    if "docker daemon is not running" in str(check.stdout):
        raise BaseException("turn docker on dummy")
    return all(
        [
            os.environ.get("NAME_REST_SERVER") in str(check.stdout),
            os.environ.get("NAME_DB") in str(check.stdout),
        ]
    )

def volume_exists() -> bool:
    check = command(os.environ.get("CMD_VOLUME_CHECK"))
    return os.environ.get("NAME_VOLUME") in str(check.stdout)

def volume_delete() -> CompletedProcess:
    return command(os.environ.get("CMD_VOLUME_RM"))


def start_up() -> bool:
    if not server_and_db_are_running():
        start()
        assert server_and_db_are_running()

def tear_down() -> bool:
    if not server_and_db_are_running():
        print("skipping teardown due to server not running")
        return
    print("stopping server..")
    quit()
    print("server stopped successfully")
    if volume_exists():
        print("deleting volume..")
        volume_delete()
        assert not volume_exists()
        print("deleted")
    return not all(
        [server_and_db_are_running(), volume_exists()]
    )