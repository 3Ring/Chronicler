from flask_login import current_user
from project.classes import Users

url_logins = ["http://localhost/login", "http://localhost/auth.login", "auth.login", "/login"]
url_indexs = ["http://localhost/", "http://localhost/main.index", "/main.index", "/"]
url_logouts = ["http://localhost/logout", "http://localhost/auth.logout", "/auth.logout", "/logout"]

test_name = "test_user"
test_email = "register_test_email@chronicler.gg"
test_password = "test123"

def make_user(name=test_name, email=test_email, hashed_password=test_password):
    return Users(name=name, email=email, hashed_password=hashed_password)

def follow_redirects(request):
    keys = []
    for key, _ in request.headers:
        keys.append(key)
    if "Location" in keys:
        return [request.headers["Location"]]
    else:
        redirects = []
        for redirect in request.history:
            redirects.append(redirect.headers["Location"])
        return redirects

def login_failure(responses):
    if not current_user.is_anonymous == True:
        return False
    for response in responses:
        if response in url_logins:
            return True
    return False

def login_success(responses):
    if current_user.is_anonymous == True:
        return False
    for response in responses:
        if response in url_indexs:
            return True
    return False

def register_failure(responses, email=None):
    if email == None:
        email = test_email
    if current_user.is_authenticated == True:
        return False
    elif Users.query.filter_by(email=email).first() != None:
        return False
    for response in responses:
        if response in url_logins:
            return False
    return True

def register_success(responses, email=None):
    if email == None:
        email = test_email
    if not current_user.is_anonymous == True:
        return False
    elif Users.query.filter_by(email=email).first() == None:
        return False
    elif len(Users.query.filer_by(email=email).all()) > 1:
        return False
    for response in responses:
        if response in url_logins:
            return True
    return False


def test_login_logout(client, auth):
    """Using admin account: Make sure login and logout works."""

    with client:

        # route exists and current_user isn't logged in
        assert client.get('/login').status_code == 200
        assert current_user.is_anonymous == True

        # user redirected to login if anonymous
        assert client.get('/').headers["Location"] in url_logins


        # incorrect pw or email redirects back to login page
        # login_wrong_pw = auth.login(form, auth.email_admin, f"{auth.password_admin}x")
        login_wrong_pw = auth.login(auth.email_admin, f"{auth.password_admin}x")
        assert login_failure(follow_redirects(login_wrong_pw))
        login_missing_pw = auth.login(auth.email_admin, "")
        assert login_failure(follow_redirects(login_missing_pw))
        login_wrong_email = auth.login(f"{auth.email_admin}x", auth.password_admin)
        assert login_failure(follow_redirects(login_wrong_email))
        login_missing_email = auth.login("", auth.password_admin)
        assert login_failure(follow_redirects(login_missing_email))
        login_missing_both = auth.login("", "")
        assert login_failure(follow_redirects(login_missing_both))

        # correct login redirects to index
        login_correct = auth.login(auth.email_admin, auth.password_admin)
        assert login_success(follow_redirects(login_correct))

        # user is redirected to index if attempting to go to login page
        assert client.get('/login').headers["Location"] in url_indexs

        # correct user logged in
        client.get("/")
        _id = Users.query.filter_by(email=auth.email_admin).first().id
        assert current_user.is_active == True
        assert current_user.id == _id

        # log out redirects to login and user is logged out
        logout = auth.logout()
        assert logout.headers["Location"] in url_logins
        assert current_user.is_anonymous == True
        
def test_register_story(client, auth):
    """Test creation of new User and new game"""
    
    with client:
        # route exists and current_user isn't logged in
        assert client.get('/register').status_code == 200
        assert current_user.is_anonymous == True

        # incorrect registrations
        user_missing_all = make_user(name="", email="", hashed_password="")
        register_missing_all = auth.register(user_missing_all)
        assert register_failure(follow_redirects(register_missing_all), email=user_missing_all.email)

        user_missing_email = make_user(email="")
        register_missing_email = auth.register(user_missing_email)
        assert register_failure(follow_redirects(register_missing_email), email=user_missing_email.email)

        user_missing_password = make_user(hashed_password="")
        register_missing_password = auth.register(user_missing_password)
        assert register_failure(follow_redirects(register_missing_password))

        user_missing_confirm = make_user()
        register_missing_confirm = auth.register(user_missing_confirm, confirm="")
        assert register_failure(follow_redirects(register_missing_confirm))

        user_passwords_do_not_match_1 = make_user(hashed_password="doesntmatch")
        register_passwords_do_not_match_1 = auth.register(user_passwords_do_not_match_1, confirm="wrong")
        assert register_failure(follow_redirects(register_passwords_do_not_match_1))

        user_passwords_do_not_match_2 = make_user()
        register_passwords_do_not_match_2 = auth.register(user_passwords_do_not_match_2, confirm="this_doesn't_match")
        assert register_failure(follow_redirects(register_passwords_do_not_match_2))

        user_email_not_unique = make_user(email="app@chronicler.gg")
        register_email_not_unique = auth.register(user_email_not_unique)
        assert register_failure(follow_redirects(register_email_not_unique))
        
        # correct registration
        user_correct = make_user()
        register_correct = auth.register(user_correct)
        assert register_success(follow_redirects(register_correct))


        # user logs in
        locations = auth.login(model=user_correct)
        assert login_success(follow_redirects(locations))
        #     print(dir(item))
        #     print(f"type = {type(item)}")
        # for item in story_login.history:
        #     for thing in dir(item):
        #         print(f"new {thing}")
        #         print(f"{thing} == {story_login.history[thing]}")
        #     print(item["Location"])
        # assert story_login.headers["Location"] == url_index
        # assert url_index in story_login.history
        # story_logout = auth.logout()
        # assert story_logout.headers["Location"] == url_login
















        
    #     response = client.post(url_for('auth.login'), data=dict(
    #     username=email,
    #     password=password,
    #     remember=True
    # ), follow_redirects=True)


        # assert _id == current_user.id
    # assert b'Welcome!' in rv.data

    # rv = logout(client)
    # assert b'Successfully logged out' in rv.data

    # rv = login(client, f"{email}x", password)
    # assert b'Invalid username' in rv.data

    # rv = login(client, email, f'{password}x')
    # assert b'Invalid password' in rv.data

# def test_login_logout(client):
#     """Make sure login and logout works."""

#     # username = "app@chronicler.gg"
#     # password = os.environ.get("ADMIN_PASS")
#     # login
#     # rv = login(client, username, password)
#     # assert b'Welcome!' in rv.data
#     assert True


#     # logout
#     rv = logout(client)
#     assert b'Successfully logged out' in rv.data

#     # incorrect username
#     rv = login(client, f"{username}x", password)
#     assert b'Please check your login details and try again' in rv.data

#     # incorrect password
#     rv = login(client, username, "password")
#     assert b'Please check your login details and try again' in rv.data