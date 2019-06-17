from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from db_setup import *

engine = create_engine("sqlite:///electronic.db")

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# session.query(User).delete()

# session.query(Category).delete()

# session.query(Items).delete()

# Create User
user1 = User(user_name="Chintala Sreevidya",
             user_email="sreevidyachintala16@gmail.com",
             user_picture="https://lh3.googleusercontent.com/a-/"
             "AAuE7mC5iFOdtIN8N8IkHwT-7mJxgV7MWYuWDayxdPpolB8=s640-rw-il")
session.add(user1)
session.commit()
print("Done..!")

# Create Categories

category1 = Category(name="Air conditioner", user_id=1)
session.add(category1)
session.commit()

category2 = Category(name="Washing Machine", user_id=1)
session.add(category2)
session.commit()

category3 = Category(name="Television", user_id=1)
session.add(category3)
session.commit()

category4 = Category(name="Oven", user_id=1)
session.add(category4)
session.commit()


# Items
product_1 = Items(brandname="Videocon",
                  model=" CWCDGD-CQ5S243P",
                  image="https://lscdn.blob.core.windows.net/products/ac"
                  "/images/Videocon-VFS53-CVE-MGA-1.5-Ton-Split-AC.jpg.",
                  color="White",
                  price="25000",
                  description="Videocon"
                              " Bacteria and other harmful germ"
                              "are blocked by the anti-bacteria filter.",
                  category_id="1",
                  userid=1)
session.add(product_1)
session.commit()

product_2 = Items(brandname="Bosch",
                  model="FH0B8NDL22",
                  image="https://azcd.harveynorman.com.au/media/"
                  "catalog/product/cache/21/image/992x558/"
                  "9df78eab33525d08d6e5fb8d27136e95/"
                  "d/e/def_6.jpg",
                        color="White",
                        price="25000",
                        description="Bosch is the best"
                        "it can wash good amount of clothes at one go.",
                        category_id="2",
                        userid=1)
session.add(product_2)
session.commit()

product_3 = Items(brandname="Sony",
                  model="VPL-DX221",
                  image="https://images-na.ssl-images-amazon.com/"
                  "images/I/71oG3K9GssL._SX425_.jpg",
                  color="black",
                        price="40000",
                        description="Sony has the best"
                        "Television for your business.",
                        category_id="3",
                        userid=1)
session.add(product_3)
session.commit()

product_4 = Items(brandname="Samsung",
                  model=" CE117PC-B2/XTL 32L",
                  image="https://n2.sdlcdn.com/imgs/b/g/5/"
                  "Samsung-28-ltrs-MC28H5025VS-Convection"
                  "-SDL002715882-1-958bb.jpg",
                  color="black",
                  price="15000",
                  description=" Samsung known for"
                        " It has Tandoor technology and fermentation"
                        " feature for traditional cooking.",
                  category_id="4",
                  userid=1)
session.add(product_4)
session.commit()

print("Brands are Added..!")
