from app import *
db.create_all()

admin=User(username="admin@user.com", name="Admin", password="123456",
 address="NA", pincode="600001", type="admin")

db.session.add(admin)
db.session.commit()