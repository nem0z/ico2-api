import json
from sqlalchemy.orm import Session

from database import Base, Scope, Category, Unit, Item, Factor, SessionLocal

# Function to create or retrieve existing entities
def get_or_create(session: Session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = {k: v for k, v in kwargs.items()}
        if defaults:
            params.update(defaults)
        obj = model(**params)
        session.add(obj)
        session.commit()
        return obj, True


def import_data(db_session: Session, data: dict):
    # Extract data from the JSON
    item_label = data["label"]
    scope_label = data["scopeLabel"]
    category_label = data["categoryLabel"]
    factors_data = data.get("factors", [])

    # Create or retrieve existing Category, Scope, and Unit
    scope, _ = get_or_create(db_session, Scope, label=scope_label)
    category, _ = get_or_create(db_session, Category, label=category_label)

    # Create or retrieve existing Item
    item, _ = get_or_create(db_session, Item, label=item_label, categoryId=category.id, scopeId=scope.id, isActive=True)

    # Create or retrieve existing Factors
    for factor_data in factors_data:
        unit_label = factor_data["unit"]["label"]
        unit_symb = factor_data["unit"]["symb"]
        unit, _ = get_or_create(db_session, Unit, label=unit_label, symb=unit_symb)

        value = factor_data["value"]
        factor, _ = get_or_create(db_session, Factor, valeur=value, unitId=unit.id, itemId=item.id, isActive=True)

if __name__ == "__main__":
    db_session = SessionLocal()
    
    # Load data from the JSON file
    with open("data.json", "r") as file:
        data = json.load(file)

        try:
            for item_data in data:
                import_data(db_session, item_data)
        finally:
            db_session.close()
