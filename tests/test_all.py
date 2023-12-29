import pytest, os
from flask import session
from main import app, get_db

@pytest.fixture(scope="module")
def client():
    app.config["TESTING"] = True
    app.config.update(dict(DATABASE = os.path.join(app.root_path, "coments_test.db")))
    client = app.test_client()

    with app.app_context():
        db = get_db()
        yield client
        db.execute("DELETE FROM users")
        db.execute("DELETE FROM comments")
        db.commit()

class TestRegisterLogin:
    def test_resume_unauthenticated(self, client):
        response = client.get('/resume/')
        assert response.status_code == 401

    def test_registration(self, client):
        response = client.get('/registration')
        assert response.status_code == 200

        response = client.post('/registration', data={
            'NickName': 'test_user',
            'password': 'test_password',
            'Rang': 'test_rang'
        })
        assert response.status_code == 302

        with client.session_transaction() as sess:
            assert sess["userLogged"] == "test_user"

        assert response.headers["Location"] == "/resume/"

    def test_login(self, client):
        with client.session_transaction() as sess:
            sess.pop("userLogged", None)

        response = client.get('/login')
        assert response.status_code == 200

        # Assuming you've registered a user in the previous test
        response = client.post('/login', data={
            'NickName': 'test_user',
            'password': 'test_password'
        })
        with client.session_transaction() as sess:
            assert sess["userLogged"] == "test_user"

        assert response.status_code == 302
        assert response.headers["Location"] == "/resume/"

    def test_resume_route_authenticated(self, client):
        response = client.get('/resume/')
        assert response.status_code == 200

@pytest.mark.parametrize("commentar", ["; DELETE FROM comments;", " DELETE FROM comments;", "<style>body {transform: rotate(180deg);transform-origin: center center;}</style>"])
def test_add_post_SQL_injections(client, commentar):
    response = client.post("/resume/", data={'commentar': commentar})
    assert response.status_code == 302
    assert response.headers["Location"] == "/resume/"

    with app.app_context():
        db = get_db()
        count = db.execute("SELECT COUNT(*) FROM comments").fetchone()[0]
        assert count >= 1
