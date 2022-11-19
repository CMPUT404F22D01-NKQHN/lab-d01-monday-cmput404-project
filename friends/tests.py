from django.test import TestCase
from authors.serializers import AuthorSerializer
from posts.tests.utils import *


class FriendsTestCase(TestCase):
    def test_send_friend_request(self):
        # Create two authors
        author1 = create_author("test", "test", "test", "test")
        author2 = create_author("test2", "test2", "test2", "test2")
        self.client.force_login(author2)
        # Send a friend request
        res = self.client.post(
            f"/authors/{author1.id}/inbox",
            data={
                "type": "follow",
                "summary": "Friend request",
                "author": AuthorSerializer(author2).data,
                "object": AuthorSerializer(author1).data,
            },
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)
        # # Check that the friend request was sent
        self.client.force_login(author1)
        response = self.client.get(f"/authors/{author1.id}/inbox")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['items']), 1)
        self.assertEqual(response.json()['items'][0]["type"], "follow")
        # Accept the friend request
        res = self.client.put(
            f"/authors/{author1.id}/followers/{author2.id}",
            data={"type": "accept"},
            content_type="application/json",
        )
        
        self.assertEqual(res.status_code, 200)
        
        # Check that author 2 is now following author 1
        response = self.client.get(f"/authors/{author1.id}/followers")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["items"]), 1)
        
        # check on author 2's id 
        res = self.client.get(f"/authors/{author1.id}/followers/{author2.id}")
        self.assertEqual(res.status_code, 200)
            