import os
import unittest
import json
from app import create_app
from models import setup_db, Movie, Actor

EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1VUkdNVEExTWpsRlJUVkRPRFJCTWprMk1ERTRSVEUyUVVFeFFVTkJRVE5CTlRnMFF6STBNdyJ9.eyJpc3MiOiJodHRwczovL2JvbHRvbi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWUyMDZhMjIzNTVhOWUwZThiYWNlOTQ2IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU4MzU5ODk2MywiZXhwIjoxNTgzNjg1MzYzLCJhenAiOiJFTkFqOXZjT3dIRDI2OU1lWFVJNERQMjJDa1VHN01TTiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjdG9ycyIsImNyZWF0ZTptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImVkaXQ6YWN0b3JzIiwiZWRpdDptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.e8UfSTzN19jLKofJ7Hpy-7OypWVjEk-DU9pwjYHtqv7I6qek-W-RuD0Dv1fw83bQtLatOYkSMnbnj48q_XKW_LUbpvCjhf5h6k_NwVmYbxTmduY1gCYSNPUZPFjUMex6LhdtzmervIq3ArsjgzqUtNW_FfzJC8cmf6lmhMGlAhEKDquEsrL3LeNkZULHnC7XtMfY4ds3qooRyum7zXPqSGinrOQD18IT8PcwYEiiuGF4hdsDa4PuIz4vnyuNxxx-b2o78XrMjgoFfWpodN7V2T53edDdfrmH3_uOsxK0o4QphvpIhen1diVoB9ut4FPKI7bbpzqI_uHPicsDtOYzxw'
CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1VUkdNVEExTWpsRlJUVkRPRFJCTWprMk1ERTRSVEUyUVVFeFFVTkJRVE5CTlRnMFF6STBNdyJ9.eyJpc3MiOiJodHRwczovL2JvbHRvbi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWUxMWQxOTViODc2N2QwZTkzN2ZjOTQ3IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU4MzU5OTA4MCwiZXhwIjoxNTgzNjg1NDgwLCJhenAiOiJFTkFqOXZjT3dIRDI2OU1lWFVJNERQMjJDa1VHN01TTiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJlZGl0OmFjdG9ycyIsImVkaXQ6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.OSbfKesfOJ1aYq3kEVAaFY8s8lP6g8d-D-V2wZabiDqod-aZZdBfEbOLcuPsJArydDsF4JQ3EfKv5ytl4qowReE9-V3CFZB4ymRtpsqIpPfXT2t9nibyXAGSUs1wLde2EAZxskffax9wkw1caoyq-SuFQvovAOJhbnu4pwy2NBsPFtDUSU_uW-ImKoP9Q83R1Bm0DB9E-7eYw2HcY_ULrhW9cAlhL5eVgLyeIuRrciwvXbJ23-z1HTpbGMJmCODjJDw3H9Gn3MOua6yt8Lhqs02Xqz-QgP-XgnMuHD53ZqKgcxMyA61qpUqiam1bnhLrSNKGLuYSFSuL0LyahnOE6Q'
CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1VUkdNVEExTWpsRlJUVkRPRFJCTWprMk1ERTRSVEUyUVVFeFFVTkJRVE5CTlRnMFF6STBNdyJ9.eyJpc3MiOiJodHRwczovL2JvbHRvbi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU2M2IyMTZjNmRiYzkwZDNkZTE2NDY5IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU4MzU5OTE1NiwiZXhwIjoxNTgzNjg1NTU2LCJhenAiOiJFTkFqOXZjT3dIRDI2OU1lWFVJNERQMjJDa1VHN01TTiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.hxKkdNKjLdpQ9zxjxtcQJBs3osklikcNtmLFWSuMWJyI0JejAd3xX3pDSQS_7LVFci6NLNP4no1HNbM5TpfTXAq5YyfZnPdkHDKyxxRcNLe13xT7z3YTLFGnE4kumWhxQd9rs7DGZrTsLOgRQYdHnecZT4RAUNnKs_0mIWw4TMcenXeGvLSQvjBJo53bzJWHk2k-lfJyRJFfAdWfjQR5rrEIC-hP3Z-tpEHeQAcYmX5IQhhTYydM8rJ-zGU9S0d3xg406OV0dJLhXBDWHN-gBR3JX7AWv0KwfZcazJaw6lVpMpsHndZv5rA2FdmUTGIGwtKfZsA4U1Cdx2Fcf2yF4A'

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the movies-hub test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['TEST_DATABASE_URL']
        setup_db(self.app, self.database_path)

    def tearDown(self):
        """Executed after reach test"""
        pass

    #  GET /movies
    def test_get_movies(self):
        response = self.client().get(
            '/movies',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # POST /movies
    def test_post_movie(self):
        response = self.client().post(
            '/movies',
            json={'title': 'now you see me', 'releaseDate': "2010-10-12"},
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['title'], 'now you see me')

    def test_post_movie_400(self):
        response = self.client().post(
            '/movies',
            json={'title': '', 'releaseDate': ''},
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

    def test_post_movie_401(self):
        response = self.client().post(
            '/movies',
            json={'title': 'things fall apart', 'releaseDate': "2009-07-10"},
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message'], 'Unauthorized')

    # PATCH /movies
    def test_edit_movie(self):
        response = self.client().patch(
            '/movies/1',
            json={'title': 'the calling', 'releaseDate': "2001-04-01"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['title'], 'the calling')

    def test_edit_movie_400(self):
        response = self.client().patch(
            '/movies/1',
            json={'title': '', 'releaseDate': ''},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

    def test_edit_movie_404(self):
        response = self.client().patch(
            '/movies/10',
            json={'title': 'the gift', 'releaseDate': "2010-10-10"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # DELETE /movies/id
    def test_delete_movie(self):
        response = self.client().delete(
            '/movies/2',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 2)

    def test_delete_movie_404(self):
        response = self.client().delete(
            '/movies/10',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_movie_401(self):
        response = self.client().delete(
            '/movies/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message'], 'Unauthorized')

    #  GET /actors
    def test_get_actors(self):
        response = self.client().get(
            '/actors',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # POST /actors
    def test_post_actor(self):
        response = self.client().post(
            '/actors',
            json={'name': 'kyle walker', 'age': 27, "gender": "male"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], 'kyle walker')

    def test_post_actor_400(self):
        response = self.client().post(
            '/actors',
            json={'name': '', 'age': '', "gender":''},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

    def test_post_actor_401(self):
        response = self.client().post(
            '/actors',
            json={'name': 'George clooney', 'age': 74, "gender": "male"},
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message'], 'Unauthorized')

    # PATCH /actors
    def test_edit_actor(self):
        response = self.client().patch(
            '/actors/2',
            json={'name': 'Timothy harlan', 'age': 32, "gender": "male"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], 'Timothy harlan')

    def test_edit_actor_400(self):
        response = self.client().patch(
            '/actors/2',
            json={'name':'', 'age':''},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

    def test_edit_actor_404(self):
        response = self.client().patch(
            '/actors/1000',
            json={'name': 'morgan freeman', 'age': 77, "gender": "male"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # DELETE /actors/id
    def test_delete_actor(self):
        response = self.client().delete(
            '/actors/3',
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actor_404(self):
        response = self.client().delete(
            '/actors/10',
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_actor_401(self):
        response = self.client().delete(
            '/actors/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message'], 'Unauthorized')

if __name__ == "__main__":
    unittest.main()