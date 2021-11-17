import unittest
import requests
import os
from project.models import *
from project.__init__ import db
from tests.test_helpers import make_string_testset
from werkzeug.security import generate_password_hash

from project.settings import app

class TestHelpers(unittest.TestCase):
    # priv_convert
    from project.helpers import priv_convert
    def test_priv_convert_one(self):
        one = self.priv_convert("False")
        assert one == False
    def test_priv_convert_two(self):
        two = self.priv_convert("True")
        assert two == True
    def test_priv_convert_three(self):
        three = self.priv_convert(True)
        assert three == True
    def test_priv_convert_four(self):
        four = self.priv_convert(False)
        assert four == False
    def test_priv_convert_five(self):
        five = self.priv_convert("p")
        assert five == False
    def test_priv_convert_six(self):
        six = self.priv_convert("")
        assert six == False

    # images
    from project.helpers import upload
    from tests.test_items import images

    def test_upload_one(self):
        jpeg = self.upload(self.images.jpeg)


# class ApiTest(unittest.TestCase):

#     API_URL = "http://127.0.0.1:5000/"
#     def test_1_setup(self):
#         db_password = os.environ.get('DB_PASS')
#         assert db_password is not None
#         assert app.config
#         assert app.config['SQLALCHEMY_DATABASE_URI']
#         assert app.config['SECRET_KEY'] == db_password
#         assert app.config['POSTGRES_PASSWORD'] == db_password

#         r = requests.get(ApiTest.API_URL)
#     def test_2_is_db_inited(self):
#         tutorial = Users.query.filter_by(email='app@chronicler.gg').first()
#         assert tutorial.name == "Chronicler"

# class DB_Test(unittest.TestCase):

#     lengths = [ 1, 10, 100]
#     type_dict = {
#         "lower": "random.choice(string.ascii_lowercase)"
#         , "upper": "random.choice(string.ascii_uppercase)"
#         , "print": "random.choice(string.printable)"
#         , "punct": "random.choice(string.punctuation)"
#     }
#     strings = make_string_testset(type_dict, short=lengths[0], long=lengths[1], super=lengths[2])
#     test_user_id = Users.query.filter_by(email="app@chronicler.gg").first().id
#     # users
#     def test_1_users(self):
#         # db variables

#         # add user to db
#         new_user = Users(name=self.strings['lower_short'], email=self.strings['lower_long'], hash=generate_password_hash(self.strings['upper_super']))
#         db.session.add(new_user)
#         db.session.commit()
#         assert new_user.id
#         db.session.remove()

#         # pw cannot be null
#         with self.assertRaises(Exception):
#             no_password = self.Users(name=self.strings['lower_short'], email=self.strings['lower_long'])
#             db.session.add(no_password)
#             db.session.commit()
#         db.session.remove()

#         # email must be unique
#         with self.assertRaises(Exception):
#             not_unique = Users(name=self.strings['lower_short'], email=self.strings['lower_long'], hash=self.generate_password_hash(self.strings['upper_super']))
#             db.session.add(not_unique)
#             db.session.commit()
#         db.session.remove()

#         # remove user from db
#         delete_user = Users.query.filter_by(email=self.strings['lower_long']).first()
#         db.session.delete(delete_user)
#         db.session.commit()
#         deleted = Users.query.filter_by(email=self.strings['lower_long']).first()
#         db.session.remove()
#         self.assertIsNone(deleted)

#     # images
#     def test_2_images(self):
#         # db exists
#         fake_image=Images(img=self.strings['lower_super'], name=self.strings['upper_long'], mimetype=self.strings['lower_long'])
#         db.session.add(fake_image)
#         db.session.commit()
#         db.session.remove()
#         fake_image = Images.query.filter_by(name=self.strings['upper_long']).first()
#         self.assertIsNotNone(fake_image)

#         db.session.delete(fake_image)
#         db.session.commit()
#         db.session.remove()

#         self.assertIsNone(Images.query.filter_by(name=self.strings['upper_long']).first())
#         db.session.remove()
#         # test image paramaters in helpers function

#     # Games
#     def test_3_games(self):
#         # db exists
#         fake_game=Games(name=self.strings["upper_long"], published=True, dm_id=self.test_user_id)
#         db.session.add(fake_game)
#         db.session.commit()
#         _id = fake_game.id
#         db.session.remove()
#         fake_game = Games.query.filter_by(id = _id).first()
#         self.assertIsNotNone(fake_game)

#         # name accepts all characters
#         fake_game1=Games(name=self.strings["print_long"], published=True, dm_id=self.test_user_id)
#         fake_game2=Games(name=self.strings["punct_long"], published=True, dm_id=self.test_user_id)
#         db.session.add(fake_game1)
#         db.session.add(fake_game2)
#         db.session.commit()
#         _id1 = fake_game1.id
#         _id2 = fake_game2.id
#         db.session.remove()

#         assert Games.query.filter_by(id = _id1).first()
#         assert Games.query.filter_by(id = _id2).first()
#         db.session.remove()

#         # # name cannot be null
#         with self.assertRaises(Exception):
#             fake_game=Games(published=1, dm_id=self.test_user_id)
#             db.session.add(fake_game)
#             db.session.commit()
#         db.session.remove()
        
#         # dm_id cannot be null
#         with self.assertRaises(Exception):
#             fake_game3=Games(name=self.strings["print_long"], published=True)
#             db.session.add(fake_game3)
#             db.session.commit()
#         db.session.remove()

#         # games can be removed
#         remove_1 = Games.query.filter_by( id = _id ).first()
#         remove_2 = Games.query.filter_by( id = _id1 ).first()
#         remove_3 = Games.query.filter_by( id = _id2 ).first()

#         db.session.delete(remove_1)
#         db.session.delete(remove_2)
#         db.session.delete(remove_3)

#         db.session.commit()
#         db.session.remove()

#         self.assertIsNone(Games.query.filter_by( id = _id ).first())
#         self.assertIsNone(Games.query.filter_by( id = _id1 ).first()) 
#         self.assertIsNone(Games.query.filter_by( id = _id2 ).first()) 

#         db.session.remove()

#     # Players
#     def test_4_players(self):
#         # db exists
#         # users_id cannot be null
#         # games_id cannot be null
#         pass

#     # Characters
#     def test_5_characters(self):
#         # db exists
#         # name cannot be null
#         # userid cannot be null
#         # game_id cannot be null
#         pass

#     # Places
#     def test_7_places(self):
#         # db exists
#         # name cannot be null
#         # game_id cannot be null
#         pass

#     # NPCs
#     def test_6_NPCs(self):
#         # db exists
#         # name cannot be null
#         # game_id cannot be null
#         pass

#     # Loot
#     def test_8_loot(self):
#         # db exists
#         # name cannot be null
#         # owner_id cannot be null
#         pass

#     # Sessions
#     def test_9_sessions(self):
#         # db exists
#         # number cannot be null
#         # title cannot be null
#         # games_id cannot be null
#         pass


if __name__ == '__main__':
    unittest.main()