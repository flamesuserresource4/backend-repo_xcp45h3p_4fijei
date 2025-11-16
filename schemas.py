"""
Database Schemas for Briquette Manufacturing App

Each Pydantic model represents a MongoDB collection. The collection name is the
lowercased class name (e.g., RawMaterial -> "rawmaterial").
"""

from pydantic import BaseModel, Field
from typing import Optional
import datetime as dt


class RawMaterial(BaseModel):
    name: str = Field(..., description="Raw material name, e.g., Sawdust")
    unit: str = Field(..., description="Unit of measure, e.g., kg, ton")
    cost_per_unit: float = Field(..., ge=0, description="Standard cost per unit of raw material")


class Inward(BaseModel):
    date: dt.date = Field(..., description="Date of inward/receiving")
    material_name: str = Field(..., description="Name of raw material received")
    quantity: float = Field(..., ge=0, description="Quantity received")
    unit_cost: float = Field(..., ge=0, description="Actual cost per unit for this batch")
    supplier: Optional[str] = Field(None, description="Supplier name")
    notes: Optional[str] = Field(None, description="Any additional information")


class Production(BaseModel):
    date: dt.date = Field(..., description="Date of production")
    product: str = Field("briquette", description="Product name")
    quantity_produced: float = Field(..., ge=0, description="Quantity produced (e.g., kg)")
    notes: Optional[str] = Field(None)


class Sale(BaseModel):
    date: dt.date = Field(...)
    customer: Optional[str] = Field(None)
    quantity_sold: float = Field(..., ge=0, description="Quantity sold (e.g., kg)")
    unit_price: float = Field(..., ge=0, description="Sale price per unit")
    notes: Optional[str] = Field(None)


class Expense(BaseModel):
    date: dt.date = Field(...)
    category: str = Field(..., description="e.g., Electricity, Labor, Transport")
    amount: float = Field(..., ge=0)
    notes: Optional[str] = Field(None)
