import queue
import pytest
from tests.integration.browser import Browsers
from tests.integration.auth_actions import register, login, logout
from tests.helpers import chron_url, generate_user, generate_game, get_and_increment
from tests.integration.views.create_actions import create_game, create_dm

# @pytest.fixture(scope="module", params=["chrome", "firefox", "edge"])
# @pytest.fixture(scope="module", params=["chrome"])
# def browsers(server, request, amount=1):
#     browsers = [None] * amount
#     for i in range(amount):
#         browsers[i] = create_browser(request.param)
#     yield browsers
#     [b.driver.quit() for b in browsers]


@pytest.fixture()
def logged_ins(inc, browsers):
    users = [None] * len(browsers)
    for i, browser in enumerate(browsers):
        users[i] = generate_user(inc)
        register(browser, users[i])
        login(browser, users[i])
    yield {"browsers": browsers, "users": users}
    [logout(browser) for browser in browsers]

# class CustomSelectorLoop(asyncio.SelectorEventLoop):
#     """A subclass with no overrides, just to test for presence."""

@pytest.fixture()
def relogs(logged_ins):
    [browser.driver.delete_cookie("session") for browser in logged_ins["browsers"]]
    yield logged_ins


import asyncio
import pytest_asyncio
import concurrent.futures
import threading
from concurrent.futures import ThreadPoolExecutor
# @pytest.fixture(scope="module")
# def event_loop(inc):
#     loop = asyncio.SelectorEventLoop()
#     yield loop
#     loop.close()



    
# thread_local = threading.local()
# def pytest_addoption(parser):
    # parser.addoption("--workers", action="store")




from concurrent.futures import ThreadPoolExecutor
from queue import Queue
@pytest.fixture(scope="module")
def browsers(brand, inc, request, threads: ThreadPoolExecutor):
#     # my_q = Queue(maxsize=0)
    # workers = threads.map(get_browser, range(3))
    print(f'inc: {inc}')
    workers = [i for i in threads.map(get_browser, ([brand] * 3))]
    print(f'done: {workers}')
    ids = make_ids(inc, len(workers))
    print(f'its: {ids}')
    populate = [threads.submit(new_user_with_game, ids[i], workers[i]) for i in range(len(workers))]
    test = concurrent.futures.wait(populate, timeout=60, return_when="ALL_COMPLETED")
    print(f'test: {test}')
    yield workers
#     # [my_q.put(threads.submit(get_browser(brand)))] * 3
#     # done = concurrent.futures.wait(runners, timeout=10, return_when="ALL_COMPLETED")
#     # print(my_q.get())
#     # print(f'type(done): {type(done)}')
#     # print(f'type(runners): {type(runners.result)} || runners: {runners.result}')
#     # browsers = [run for run in done[0]]
#     # print(f'browsers: {browsers}')
    # threads.map()
    #     tasks = []
    #     runner = [brand] * amount
    #     print(f'browsers: {brands}')
    #     for i, browser in zip(ids, brands):
    #         task = asyncio.ensure_future(worker(i, browser))
    #         tasks.append(task)
    #     drones = await asyncio.gather(*tasks, return_exceptions=True)
    #     print(f'drones: {drones}')
    # return drones
# @pytest.fixture(scope="module")
# def browsers(brand, inc, request):
#     b = get_browser(brand)
#     yield new_user_with_game(1, b)

@pytest.fixture(scope="module")
def populate(browsers, threads: ThreadPoolExecutor, inc):
    ids = make_ids(inc, 3)
    # for browser in browsers:
    threads.map(new_user_with_game, ids, browsers)

def new_user_with_game(_id, browser):
    try:
        # await asyncio.sleep(5)\
        print(f"1", _id)
        user = generate_user(_id)
        print(f'user: {user}')
        print(f"2", _id)
        register(browser, user)
        print(f"3", _id)
        login(browser, user)
        print(f"4", _id)
        game = generate_game(_id)
        print(f'5', _id)
        create_game(browser, game)
        print(f'6', _id)
        return browser

    except Exception as e:
        print(f'e: {e}')
        raise e


def make_ids(fp, amount: int):
    nums = [None] * amount
    for i in range(amount):
        nums[i] = get_and_increment(fp)

    return nums
def get_browser(brand):
    # if not hasattr(thread_local, "session"):
    #     thread_local.session = requests.Session()
    # return thread_local.session
    print(f'get1')
    print(f'brand: {brand}')
    browser_maker = getattr(Browsers, brand)
    print(f'get2')

    browser = browser_maker()
    print(f'get3')
    assert browser.browser_type == brand
    print(f'get4')
    return browser

# def get_brands(brand:str, amount:int):
#     supported = ["chrome", "firefox", "edge"]
#     if brand == "all":
#         brands = [None] * amount
#         return [supported[i % 3] for i in range(amount)]
#     assert brand in supported
#     return [brand] * amount


# # @pytest_asyncio.fixture(scope="module")
# @pytest_asyncio.fixture(scope="module")
# async def populate(server, event_loop, inc, amount=3):
#     drones = event_loop.run_until_complete(test(inc, amount))
#     print(f'drones: {drones}')
    # ids = make_ids(inc, amount)
    # tasks = []
    # for i in ids:
    #     task = asyncio.ensure_future(worker(i, "chrome"))
    #     tasks.append(task)
    # drones = await asyncio.gather(*tasks, return_exceptions=True)
    # print(f'drones: {drones}')
    # return drones
# @pytest.fixture(scope="module", params=["chrome", "firefox", "edge"])
# # @pytest.fixture(scope="module", params=["chrome"])
# def brands(server, request, amount=1):
#     browsers = [None] * amount
#     for i in range(amount):
#         browsers[i] = create_browser(request.param)
#     yield browsers
#     [b.driver.quit() for b in browsers]







# def create_browser(brand):
#     browser = getattr(Browsers, brand)()
#     assert browser.browser_type == brand
#     return browser
