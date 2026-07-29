from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import declarative_base, sessionmaker

db_connection_string = "postgresql://postgres:Das241Q1@localhost:5432/QA"


engine = create_engine(
    db_connection_string, echo=False, pool_pre_ping=True, future=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

Base = declarative_base()


class Subject(Base):
    __tablename__ = "subject"

    subject_id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval(pg_get_serial_sequence('subject', 'subject_id'))"),
    )
    subject_title = Column(String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<Subject(id={self.subject_id}, title='{self.subject_title}')>"


def init_db(bind_engine):
    Base.metadata.drop_all(bind=bind_engine)
    Base.metadata.create_all(bind=bind_engine)


class SubjectRepository:
    def __init__(self, db_session=None):
        self.session = db_session or SessionLocal()
        self._external_session = db_session is not None

    def get_all_subjects(self):
        return self.session.query(Subject).all()

    def get_subject_by_id(self, subject_id):
        return (
            self.session.query(Subject).filter(Subject.subject_id == subject_id).first()
        )

    def add_subject(self, title):
        new_subject = Subject(subject_title=title)
        try:
            self.session.add(new_subject)
            self.session.flush()

            if new_subject.subject_id is None:
                raise Exception("База данных не вернула ID.")

            self.session.commit()
            return new_subject.subject_id
        except Exception:
            self.session.rollback()
            raise

    def update_subject(self, subject_id, new_title):
        subject = self.get_subject_by_id(subject_id)
        if subject:
            subject.subject_title = new_title
            self.session.commit()

    def delete_subject(self, subject_id):
        subject = self.get_subject_by_id(subject_id)
        if subject:
            self.session.delete(subject)
            self.session.commit()

    def close(self):
        if not self._external_session and self.session:
            self.session.close()
