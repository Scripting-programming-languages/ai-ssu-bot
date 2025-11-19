from app.core.database import PostgresDatabase
from app.repository.message_repository import MessageRepository
from app.repository.session_repository import SessionRepository
from app.repository.faq_repository import FAQRepository

database = PostgresDatabase()

session_repo = SessionRepository()
message_repo = MessageRepository()
faq_repo = FAQRepository()
