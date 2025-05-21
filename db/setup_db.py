from .config import ENGINE
from .models import Base

def setup_db():
    Base.metadata.create_all(bind=ENGINE)