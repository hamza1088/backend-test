from sqlalchemy.orm import Session
from faker import Faker
import models

fake = Faker()

def seed_categories(db: Session, num_categories: int):
    for _ in range(num_categories):
        category = models.Category(category_name=fake.word())
        db.add(category)
    db.commit()

def seed_products(db: Session, num_products: int):
    categories = db.query(models.Category).all()

    for _ in range(num_products):
        product = models.Product(
            product_name=fake.unique.word(),
            category_id=fake.random_element(elements=[c.category_id for c in categories]),
            unit_price=fake.random_number(digits=2, fix_len=True),
            description=fake.sentence()
        )
        db.add(product)
    db.commit()

def seed_sales(db: Session, num_sales: int):
    products = db.query(models.Product).all()

    for _ in range(num_sales):
        sale = models.Sale(
            product_id=fake.random_element(elements=[p.product_id for p in products]),
            sale_date=fake.date_this_year(),
            quantity_sold=fake.random_int(min=1, max=100),
            revenue=fake.random_number(digits=2, fix_len=True)
        )
        db.add(sale)
    db.commit()

def seed_inventory(db: Session, num_inventory_entries: int):
    products = db.query(models.Product).all()

    for _ in range(num_inventory_entries):
        inventory_entry = models.Inventory(
            product_id=fake.random_element(elements=[p.product_id for p in products]),
            current_stock=fake.random_int(min=0, max=500),
            last_updated=fake.date_time_this_decade()
        )
        db.add(inventory_entry)
    db.commit()
