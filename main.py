from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from typing import List
from sqlalchemy.orm import joinedload

from database import SessionLocal, Scope, Category, Item, Factor 


app = FastAPI()

# Configure CORS
origins = ["http://localhost", "http://localhost:4200"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
@app.get("/api/scopes")
async def get_scopes() -> List[dict]:
    db = SessionLocal()
    
    try:
        scopes = db.query(Scope).all()
        return [
            {
                "id": scope.id, 
                "label": scope.label
            } for scope in scopes
        ]
        
    finally:
        db.close()


@app.get("/api/categories")
async def get_categories() -> List[dict]:
    db = SessionLocal()
    try:
        categories = db.query(Category).all()
        return [
            {
                "id": category.id, 
                "label": category.label
            } for category in categories
        ]
        
    finally:
        db.close()


@app.get("/api/items/lookup")
async def get_items(category: int = None, scope: int = None) -> List[dict]:
    db = SessionLocal()

    try:
        items = db.query(Item).filter(
            (Item.isActive == True) &
            (Item.categoryId == category) &
            ((Item.scopeId == scope) | (Item.scope.has(label="Commun")))
        ).all()
          
        return [
            {
                "id": item.id,
                "label": item.label,
                "common": item.scope.label == "Commun"
            } for item in items
        ]
        
    finally:
        db.close()


@app.get("/api/item/{item_id}/factors")
async def get_factors(item_id: int) -> List[dict]:
    db = SessionLocal()
    try:
        item_factors = db.query(Factor).options(joinedload(Factor.unit)).filter(Factor.itemId == item_id, Factor.isActive == True).all()

        return [
            {
                "id": factor.id, 
                "valeur": factor.valeur, 
                "unit": {
                    "label": factor.unit.label, 
                    "symb": factor.unit.symb
                    }
                }
            for factor in item_factors
        ]
        
    finally:
        db.close()
