from authors.serializers import AuthorSerializer
from posts.tests.utils import *
from nodes.models import Node
import requests_mock


class NodesTests(TestCase):
    """
    Test the behaviour of having multiple nodes
    """

    def setUp(self):
        remote_team: Author = create_author(
            "remote_author", "remote_author", "remote_pass", "remote_author_user"
        )
        remote_team.is_another_server = True
        remote_team.save()
        local_author = create_author(
            "local_author", "local_author", "local_author", "local_author"
        )
        self.remote_team = remote_team
        self.local_author = local_author
        node = Node.objects.create(
            team_account=remote_team,
            api_url="http://remote_author.com",
            username="my_username_for_remote",
            password="my_password_for_remote",
        )
        node.save()
        self.node = node

    def test_remote_author_can_follow_local_author(self):
        """
        Test that a remote author can follow a local author
        """
        remote_author_json = {
            "id": "http://remote_author.com/author/something",
            "host": "http://remote_author.com",
            "display_name": "this_other_author",
        }

        follow_req = {
            "type": "follow",
            "summary": "Friend request",
            "author": remote_author_json,
            "object": AuthorSerializer(self.local_author).data,
        }

        # Create a follow request
        self.client.force_login(self.remote_team)
        response = self.client.post(
            path=f"/authors/{self.local_author.id}/inbox",
            data=json.dumps(follow_req),
            content_type="application/json",
        )

        # Check that the proxy user was created
        res = self.client.get(path=f"/nodes/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["nodes"][0]["proxy_users"]), 1)
        self.assertEqual(response.status_code, 201)

        # Check that the follow request was sent
        self.client.force_login(self.local_author)
        response = self.client.get(f"/authors/{self.local_author.id}/inbox")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["items"]), 1)
        self.assertEqual(response.json()["items"][0]["type"], "follow")

        # Accept the follow request
        res = self.client.put(
            f"/authors/{self.local_author.id}/followers/{remote_author_json['id'].split('/')[-1]}",
            data={"type": "accept"},
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200)

        # Create a post and catch any requests that are sent
        with requests_mock.Mocker() as m:
            # Set up the mock
            m.post(
                f"{self.node.api_url}/authors/{remote_author_json['id'].split('/')[-1]}/inbox",
            )
            self.client.force_login(self.local_author)
            response = self.client.post(
                path=f"/authors/{self.local_author.id}/posts",
                data=json.dumps(POST_DATA),
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(m.call_count, 1)
            # print(m.request_history[0].json())

    def test_remote_author_can_like_local_post(self):
        """
        Test that a remote author can like a local post
        """
        remote_author_json = {
            "id": "http://remote_author.com/author/something",
            "host": "http://remote_author.com",
            "display_name": "this_other_author",
        }

        # Create a post
        self.client.force_login(self.local_author)
        response = self.client.post(
            path=f"/authors/{self.local_author.id}/posts",
            data=json.dumps(POST_DATA),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        post_id = response.json()["id"].split("/")[-1]

        # Send a like request from the remote author
        self.client.force_login(self.remote_team)
        payload = {
            "summary": "Lara Croft Likes your post",
            "type": "like",
            "author": remote_author_json,
            "object": response.json()["id"],
        }

        response = self.client.post(
            path=f"/authors/{self.local_author.id}/inbox",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.client.force_login(self.local_author)
        response = self.client.get(
            f"/authors/{self.local_author.id}/posts/{post_id}/likes"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["author"]["id"], remote_author_json["id"])

    def test_remote_author_can_comment_on_local_post(self):
        """
        Test that a remote author can comment on a local post
        """
        remote_author_json = {
            "id": "http://remote_author.com/author/something",
            "host": "http://remote_author.com",
            "display_name": "this_other_author",
        }

        # Create a post
        self.client.force_login(self.local_author)
        response = self.client.post(
            path=f"/authors/{self.local_author.id}/posts",
            data=json.dumps(POST_DATA),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        post_id = response.json()["id"].split("/")[-1]

        # Send a comment request from the remote author
        self.client.force_login(self.remote_team)
        payload = {
            "type": "comment",
            "author": remote_author_json,
            "comment": "This is a comment",
            "post_id": post_id,
        }
        self.client.force_login(self.remote_team)
        response = self.client.post(
            path=f"/authors/{self.local_author.id}/inbox",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.client.force_login(self.local_author)
        response = self.client.get(
            f"/authors/{self.local_author.id}/posts/{post_id}/comments"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
