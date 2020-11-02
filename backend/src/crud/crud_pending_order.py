from sqlalchemy.orm import Session
from src import crud, models, schemas
from src.core.utilities import fail_save, log_msg
from src.models.pending_order import PendingOrder
from src.schemas.response import Fail, Result, Success, return_result


class CRUDPendingOrder:
    @fail_save
    @return_result
    def create_order(
        self,
        *,
        db: Session,
        order: schemas.PendingOrderDBcreate,
    ) -> bool:
        if not crud.stock.symbol_exists(db=db, symbol=order.symbol):
            return Fail(f"Cannot add a non-existent symbol as a pending order of User(uid = {order.user_id}).")

        # TODO check difference between add, commit, flush
        order_m = PendingOrder.subclass(order.order_type)(**order.dict(exclude_none=True))
        db.add(order_m)
        db.flush()

    @fail_save
    @return_result
    def delete_order(self, *, db: Session, id: int, user=None) -> Result:
        order = db.query(PendingOrder).filter(PendingOrder.id == id).first()

        if order is None:
            return Fail(f"No limit order of id {id} exists.").log()

        elif user is not None and user.uid != order.user_id:
            return Fail(f"The order(id = {id}) is not owned by the user(uid = {user.uid}).")

        db.remove(order)
        db.flush()


pending_order = CRUDPendingOrder()
