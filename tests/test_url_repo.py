from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import Base
from app.main import app
from app.models.url import Url_Short
from app.repositoires.url_repo import UrlRepository


def test_redirect_url_uses_short_code_path():
    assert app.url_path_for("redirect_url", short_url="abc123") == "/short_url/abc123"


def test_click_count_url_increments_existing_record():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)

    with SessionLocal() as db:
        item = Url_Short(original_url="https://example.com", short_url="abc123")
        db.add(item)
        db.commit()
        db.refresh(item)

        repo = UrlRepository()
        updated = repo.click_count_url(db, item)

        assert updated.click_count == 1
