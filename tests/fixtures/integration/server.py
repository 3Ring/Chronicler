import pytest
from project.helpers.misc import bool_convert
from tests.helpers import command

VOLUME = "chronicler_volume_test"
DB = "chronicler_host_test"
REST = "rest-server_test"



@pytest.fixture(scope="session")
def server(request):
    no_tear_down = request.config.getoption("--no-tear-down")
    if not check_if_server_is_up():
        launch_server()
    yield
    if not bool_convert(no_tear_down):
        stop_server()
        delete_volume()
    else:
        print(f'skipping tear down..')

def launch_server():
    up = command("docker-compose -f docker-compose_testing.yml -p chronicler_testing up -d")
    assert up.returncode == 0
    assert check_if_server_is_up()
    # assert "Creating chronicler_host_test" in str(up.stdout) or "Starting chronicler_host_test" in str(up.stdout) or 'chronicler_host_test is up-to-date' in str(up.stdout)
    # assert "Creating rest-server_test" in str(up.stdout) or "Starting rest-server_test" in str(up.stdout) or 'rest-server_test is up-to-date' in str(up.stdout)

def stop_server():
    down = command("docker-compose -f docker-compose_testing.yml -p chronicler_testing down")
    assert down.returncode == 0
    assert not check_if_server_is_up()
    # assert "Removing rest-server_test" in str(down.stdout)
    # assert "Removing network chronicler_back_test" in str(down.stdout)
    # assert "Removing chronicler_host_test" in str(down.stdout)

def delete_volume():
    delete = command("docker volume rm chronicler_volume_test")
    assert delete.returncode == 0
    assert not check_if_volume_exists()

def check_if_volume_exists():
    check = command("docker volume ls")
    return VOLUME in str(check.stdout)

def check_if_server_is_up():
    check = command("docker ps")
    return all([_db_is_up(check), _rest_is_up(check)])

def _db_is_up(check):
    return DB in str(check.stdout) 

def _rest_is_up(check):
    return REST in str(check.stdout)




