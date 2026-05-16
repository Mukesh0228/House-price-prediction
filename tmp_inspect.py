from backend.app import create_app
from backend.models import Property

app = create_app()
with app.app_context():
    props = Property.query.limit(6).all()
    for p in props:
        print(p.id, p.title, p.image_filename)
