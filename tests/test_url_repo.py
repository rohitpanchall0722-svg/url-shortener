from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.database.database import Base
from app.database.connection import get_db
from app.main import app
from app.models.url import Url_Short
from app.repositoires.url_repo import UrlRepository


def test_redirect_url_uses_short_code_path():
    assert app.url_path_for(
        "redirect_url",
        short_url="abc123"
    ) == "/short_url/url/abc123"


def test_click_count_url_increments_existing_record():
    engine = create_engine("sqlite:///:memory:")

    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(bind=engine)

    with SessionLocal() as db:
        item = Url_Short(
            original_url="https://example.com",
            short_url="abc123"
        )

        db.add(item)
        db.commit()
        db.refresh(item)

        repo = UrlRepository()

        updated = repo.click_count_url(db, item)

        assert updated.click_count == 1


def test_get_all_url_returns_all_records():
    engine = create_engine("sqlite:///:memory:")

    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(bind=engine)

    with SessionLocal() as db:
        db.add_all([
            Url_Short(original_url="https://example.com/1", short_url="first1"),
            Url_Short(original_url="https://example.com/2", short_url="second2"),
        ])
        db.commit()

        repo = UrlRepository()

        urls = repo.get_all_url(db)

        assert [url.short_url for url in urls] == ["first1", "second2"]
        assert app.url_path_for("get_all_url") == "/short_url/all"


def test_get_all_url_endpoint_returns_records():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)

    def override_get_db():
        with SessionLocal() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db
    try:
        with SessionLocal() as db:
            db.add(Url_Short(
                original_url="https://example.com",
                short_url="abc123",
            ))
            db.commit()

        with TestClient(app, base_url="http://localhost") as client:
            response = client.get("/short_url/all")
    finally:
        app.dependency_overrides.clear()
        engine.dispose()

    assert response.status_code == 200
    assert response.json()[0]["short_url"] == "abc123"


def test_delete_url_endpoint_deletes_record_by_id():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)

    def override_get_db():
        with SessionLocal() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db
    try:
        with SessionLocal() as db:
            item = Url_Short(
                original_url="https://example.com",
                short_url="abc123",
            )
            db.add(item)
            db.commit()
            url_id = item.id

        with TestClient(app, base_url="http://localhost") as client:
            response = client.delete(f"/short_url/delete/{url_id}")
            remaining_response = client.get("/short_url/all")
            missing_response = client.delete(f"/short_url/delete/{url_id}")
    finally:
        app.dependency_overrides.clear()
        engine.dispose()

    assert response.status_code == 200
    assert response.json()["message"] == "URL deleted successfully"
    assert response.json()["deleted_url"]["id"] == url_id
    assert response.json()["deleted_url"]["original_url"] == "https://example.com"
    assert response.json()["deleted_url"]["short_url"] == "abc123"
    assert remaining_response.status_code == 200
    assert remaining_response.json() == []
    assert missing_response.status_code == 404
