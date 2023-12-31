import pytest
from app import schemas

def test_unauthorized_user_create_post(client):
    res = client.post(
        "/posts/",json={"title":"test title","content":"test content"}
    )
    assert res.status_code == 401

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, res.json())
    posts = list(posts_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
    
def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/404")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content

@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post(
        "/posts/",json = {"title": title, "content": content, "published": published})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']

def test_created_post_default_published_true(authorized_client, test_user, test_posts):

    title, content = "Test Title", "Test Content"
    res = authorized_client.post(
        "/posts/",json = {"title": title, "content": content})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']

def test_unauthorized_user_create_posts(client, test_posts):
    title, content = "Test Title", "Test Content"
    res = client.post(
        "/posts/",json = {"title": title, "content": content})
    assert res.status_code == 401

def test_unauthorized_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 204

def test_delete_post_not_exist(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/404")

    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_posts):
    # print(test_posts)
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")

    assert res.status_code == 403


def test_update_post(authorized_client, test_posts):
    data = {
        "title" : "new title",
        "content" : "new content",
        "id": test_posts[0].id
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)

    assert res.status_code == 201

def test_other_user_post(authorized_client, test_user2, test_posts):
    data = {
        "title" : "new title",
        "content" : "new content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403

def test_unauthorized_update_post(client, test_user, test_posts):
    data = {
        "title" : "new title",
        "content" : "new content",
        "id": test_posts[3].id
    }
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_update_post_not_exist(authorized_client, test_posts):
    data = {
        "title" : "new title",
        "content" : "new content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/404", json = data)

    assert res.status_code == 404