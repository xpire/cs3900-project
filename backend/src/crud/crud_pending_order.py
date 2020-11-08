"""
CRUD operations for pending orders (limit and after market)
"""

from sqlalchemy.orm import Session
from src import crud, schemas
from src.core.utilities import fail_save
from src.crud.base import CRUDBase
from src.models.pending_order import PendingOrder
from src.schemas.response import Fail, Result, return_result


class CRUDPendingOrder(CRUDBase[PendingOrder]):
    @fail_save
    @return_result()
    def create_order(
        self,
        *,
        db: Session,
        order: schemas.PendingOrderDBcreate,
    ) -> Result:
        """Adds a pending to the database

        Args:
            db (Session): database session
            order (schemas.PendingOrderDBcreate): order to be added

        Returns:
            Result: Success/Fail
        """
        if not crud.stock.symbol_exists(db=db, symbol=order.symbol):
            return Fail(f"Cannot add a non-existent symbol as a pending order of User(uid = {order.user_id}).")

        print("ADD PENDING ORDER:", order)
        order_m = PendingOrder.subclass(order.order_type)(**order.dict(exclude_none=True))
        db.add(order_m)
        db.commit()

    @fail_save
    @return_result()
    def delete_order(self, *, db: Session, id: int, user=None) -> Result:
        """Deletes a pending order from the database. If user is specified, order must exist for the user.

        Returns:
            Result: Success/Fail
        """
        order_m = self.query(db).get(id)

        if order_m is None:
            return Fail(f"No limit order of id {id} exists.").log()

        elif user is not None and user.uid != order_m.user_id:
            return Fail(f"The order(id = {id}) is not owned by the user(uid = {user.uid}).")

        db.delete(order_m)
        db.commit()


pending_order = CRUDPendingOrder(PendingOrder)
