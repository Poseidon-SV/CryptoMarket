from crypto_package import db
from crypto_package.models import Currency

my_data = Currency.query.get(4)
db.session.delete(my_data)
db.session.commit()

