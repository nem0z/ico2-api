import sys
import json, csv
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
    factor_data = data["factor"]

    # Create or retrieve existing Category, Scope, and Unit
    scope, _ = get_or_create(db_session, Scope, label=scope_label)
    category, _ = get_or_create(db_session, Category, label=category_label)

    # Create or retrieve existing Item
    item, _ = get_or_create(db_session, Item, label=item_label, categoryId=category.id, scopeId=scope.id, isActive=True)

    # Create or retrieve existing Factors
    unit_label = factor_data["unit"]["label"]
    unit_symb = factor_data["unit"]["symb"]
    unit, _ = get_or_create(db_session, Unit, label=unit_label, symb=unit_symb)

    value = factor_data["value"]
    _, _ = get_or_create(db_session, Factor, value=value, unitId=unit.id, itemId=item.id, isActive=True)

def csv_to_dict(data):
    formatted_data = []
    for row in data:
        formatted_row = {}
        for key, value in row.items():
            keys = key.split(".")
            current_level = formatted_row
            for k in keys[:-1]:
                current_level = current_level.setdefault(k, {})
            current_level[keys[-1]] = value
        formatted_data.append(formatted_row)

    return formatted_data

if __name__ == "__main__":
    db_session = SessionLocal()
    
    with open(sys.argv[1], mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=";")
        data = [dict(row) for row in csv_reader]

        formatted_data = csv_to_dict(data)

        try:
            for item_data in formatted_data:
                import_data(db_session, item_data)
        finally:
            db_session.close()
