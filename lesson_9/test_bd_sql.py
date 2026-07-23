import pytest
import uuid
from bd import (
    engine,
    Base,
    SubjectRepository,
    Subject,
)
from sqlalchemy.orm import sessionmaker, close_all_sessions
from sqlalchemy import text

close_all_sessions()


with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS subject CASCADE;"))
    conn.commit()

    conn.execute(text("""
        CREATE TABLE subject (
            subject_id SERIAL PRIMARY KEY,
            subject_title VARCHAR(100) NOT NULL UNIQUE
        );
    """))
    conn.commit()


@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()

    SessionTesting = sessionmaker(bind=connection, expire_on_commit=False, future=True)
    session = SessionTesting()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def repo(db_session):
    r = SubjectRepository(db_session=db_session)
    return r


def test_add_subject(repo):
    """Добавление нового предмета"""
    unique_id = str(uuid.uuid4())[:8]
    title = f"Арифметика {unique_id}"

    next_id = repo.session.execute(
        text("SELECT nextval(pg_get_serial_sequence('subject', 'subject_id'));")
    ).scalar_one()

    new_subject = Subject(subject_id=next_id, subject_title=title)
    repo.session.add(new_subject)

    try:
        repo.session.commit()
    except Exception:
        repo.session.rollback()
        raise

    assert new_subject.subject_id is not None

    subject = repo.get_subject_by_id(new_subject.subject_id)
    assert subject is not None
    assert subject.subject_title == title

    repo.delete_subject(subject.subject_id)
    assert repo.get_subject_by_id(subject.subject_id) is None


def test_update_subject(repo):
    """Обновление предмета"""
    unique_id = str(uuid.uuid4())[:8]
    original_title = f"Физика {unique_id}"
    new_title = f"Астрофизика {unique_id}"

    next_id = repo.session.execute(
        text("SELECT nextval(pg_get_serial_sequence('subject', 'subject_id'));")
    ).scalar_one()

    subject = Subject(subject_id=next_id, subject_title=original_title)
    repo.session.add(subject)
    repo.session.commit()

    repo.update_subject(subject.subject_id, new_title)

    updated_subject = repo.get_subject_by_id(subject.subject_id)
    assert updated_subject is not None
    assert updated_subject.subject_title == new_title

    repo.delete_subject(updated_subject.subject_id)
    assert repo.get_subject_by_id(updated_subject.subject_id) is None


def test_delete_subject(repo):
    """Удаление предмета"""
    unique_id = str(uuid.uuid4())[:8]
    title = f"Химия {unique_id}"

    next_id = repo.session.execute(
        text("SELECT nextval(pg_get_serial_sequence('subject', 'subject_id'));")
    ).scalar_one()

    subject = Subject(subject_id=next_id, subject_title=title)
    repo.session.add(subject)
    repo.session.commit()

    repo.delete_subject(subject.subject_id)

    deleted_subject = repo.get_subject_by_id(subject.subject_id)
    assert deleted_subject is None
