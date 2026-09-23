from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from database import create_db_and_tables, get_session
from models import Item, ItemCreate, ItemUpdate, StatusEnum

app = FastAPI(title="Lost and Found System API")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate, session: Session = Depends(get_session)):
    """Create a new lost/found item."""
    db_item = Item.model_validate(item)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

# 2. GET /items
@app.get("/items", response_model=List[Item])
def read_items(session: Session = Depends(get_session)):
    """Return all reported items."""
    items = session.exec(select(Item)).all()
    return items

# 3. GET /items/{item_id}
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int, session: Session = Depends(get_session)):
    """Return a specific item using its ID."""
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item

# 4. PUT /items/{item_id}
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item_update: ItemUpdate, session: Session = Depends(get_session)):
    """Update the details/status of an existing item."""
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    update_data = item_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
        
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

# 5. DELETE /items/{item_id}
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, session: Session = Depends(get_session)):
    """Delete an item report."""
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        
    session.delete(db_item)
    session.commit()
    return None

# 6. GET /items/status/{status}
@app.get("/items/status/{status}", response_model=List[Item])
def read_items_by_status(status: StatusEnum, session: Session = Depends(get_session)):
    """Return items based on their status."""
    items = session.exec(select(Item).where(Item.status == status)).all()
    return items

# 7. GET /items/category/{category}
@app.get("/items/category/{category}", response_model=List[Item])
def read_items_by_category(category: str, session: Session = Depends(get_session)):
    """Return all items belonging to a particular category."""
    items = session.exec(select(Item).where(Item.category == category)).all()
    return items
