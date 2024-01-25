from typing import List, Optional
from fastapi import FastAPI

from database import SessionLocal, Scope, Category, Unit, Item, Factor 

app = FastAPI()

# Routes
@app.get("/api/scopes")
async def get_scopes() -> List[dict]:
    db = SessionLocal()
    scopes = db.query(Scope).all()
    db.close()
    return [{"id": scope.id, "label": scope.label} for scope in scopes]

@app.get("/api/categories")
async def get_categories() -> List[dict]:
    db = SessionLocal()
    categories = db.query(Category).all()
    db.close()
    return [{"id": category.id, "label": category.label} for category in categories]

@app.get("/api/items/lookup")
async def get_items(category: Optional[int] = None, scope: Optional[int] = None) -> List[dict]:
    db = SessionLocal()

    if scope is None:
        # If scope is not defined, include items with scope "Commun" and the specified category
        items = db.query(Item).filter(Item.isActive == True, (Item.categoryId == category) if category else True).all()
    else:
        # Include items with the specified scope and category
        items = db.query(Item).filter(Item.scopeId == scope, Item.isActive == True, (Item.categoryId == category) if category else True).all()

    db.close()

    result = []
    for item in items:
        result.append({
            "id": item.id,
            "label": item.label,
            "common": item.scope.label == "Commun" if item.scope else False  # Check if the scope is "Commun"
        })

    return result

@app.get("/api/items/{item_id}/factors")
async def get_factors(item_id: int) -> List[dict]:
    db = SessionLocal()
    item_factors = db.query(Factor).filter(Factor.itemId == item_id).all()
    db.close()
    result = [{"id": factor.id, "valeur": factor.valeur, "unite": {"id": factor.unite.id, "label": factor.unite.label, "symb": factor.unite.symb}} for factor in item_factors]
    return result
