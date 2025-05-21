from .config import ENGINE
from .models import Base

# Сreate the autoria_cars table (if not exists)
def setup_db():
    Base.metadata.create_all(bind=ENGINE)