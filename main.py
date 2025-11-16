import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from database import db, create_document, get_documents
from schemas import RawMaterial, Inward, Production, Sale, Expense

app = FastAPI(title="Briquette Manufacturing API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Briquette Manufacturing Backend Running"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "❌ Unknown"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    return response


# Utility to convert Mongo docs to API-friendly dicts

def serialize_doc(doc: dict):
    if not doc:
        return doc
    d = dict(doc)
    if "_id" in d:
        try:
            d["id"] = str(d.pop("_id"))
        except Exception:
            d["id"] = d.pop("_id")
    return d


# Endpoints for each collection

@app.get("/api/rawmaterials")
def list_raw_materials(limit: Optional[int] = 200):
    docs = get_documents("rawmaterial", {}, limit)
    return [serialize_doc(x) for x in docs]


@app.post("/api/rawmaterials")
def create_raw_material(payload: RawMaterial):
    new_id = create_document("rawmaterial", payload)
    return {"id": new_id}


@app.get("/api/inwards")
def list_inwards(limit: Optional[int] = 200):
    docs = get_documents("inward", {}, limit)
    return [serialize_doc(x) for x in docs]


@app.post("/api/inwards")
def create_inward(payload: Inward):
    new_id = create_document("inward", payload)
    return {"id": new_id}


@app.get("/api/production")
def list_production(limit: Optional[int] = 200):
    docs = get_documents("production", {}, limit)
    return [serialize_doc(x) for x in docs]


@app.post("/api/production")
def create_production(payload: Production):
    new_id = create_document("production", payload)
    return {"id": new_id}


@app.get("/api/sales")
def list_sales(limit: Optional[int] = 200):
    docs = get_documents("sale", {}, limit)
    return [serialize_doc(x) for x in docs]


@app.post("/api/sales")
def create_sale(payload: Sale):
    new_id = create_document("sale", payload)
    return {"id": new_id}


@app.get("/api/expenses")
def list_expenses(limit: Optional[int] = 200):
    docs = get_documents("expense", {}, limit)
    return [serialize_doc(x) for x in docs]


@app.post("/api/expenses")
def create_expense(payload: Expense):
    new_id = create_document("expense", payload)
    return {"id": new_id}


# Simple KPIs

class ProfitResponse(BaseModel):
    total_sales: float
    total_expenses: float
    profit: float


@app.get("/api/kpi/profit", response_model=ProfitResponse)
def get_profit():
    sales = get_documents("sale")
    expenses = get_documents("expense")

    total_sales = sum([(s.get("quantity_sold", 0) or 0) * (s.get("unit_price", 0) or 0) for s in sales])
    total_expenses = sum([e.get("amount", 0) or 0 for e in expenses])
    profit = total_sales - total_expenses
    return ProfitResponse(total_sales=total_sales, total_expenses=total_expenses, profit=profit)


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
