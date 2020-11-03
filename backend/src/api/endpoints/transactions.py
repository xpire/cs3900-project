from typing import List

from fastapi import APIRouter, Depends
from src import schemas
from src.api.deps import get_current_user_m
from src.models.user import User
from src.schemas.transaction import TransactionAPIout

router = APIRouter()

"""
class Transaction(BaseModel):
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("user.uid"))
    symbol = Column(String, ForeignKey("stock.symbol"))
    qty = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    trade_type = Column(String)  # buy/sell/short/cover
    timestamp = Column(DateTime)
    stock = relationship(
        "Stock",
        backref="transactions",
        cascade="save-update, merge",
    )
"""

"""
    for transaction in user.model.transaction_hist:
        ret.append(
            {
                "symbol": transaction.symbol,
                "name": transaction.stock.name,
                "amount": transaction.qty,
                "price": transaction.price,
                "value": transaction.qty * transaction.price,
                "t_type": transaction.trade_type,
                "timestamp": transaction.timestamp,
            }
        )
"""


@router.get("/")
async def get_transactions(user_m: User = Depends(get_current_user_m)) -> List[TransactionAPIout]:
    def to_transaction(t):
        return schemas.TransactionAPIout(**t.dict(), name=t.stock.name)

    return [to_transaction(t) for t in user_m.transaction_hist]
