from sqlalchemy.orm import Session
from src import crud, models, schemas
from src.core.utilities import fail_save, log_msg
from src.models.pending_order import PendingOrder


class CRUDPendingOrder:
    @fail_save
    def create_order(
        self,
        *,
        db: Session,
        order: schemas.PendingOrder,
    ) -> bool:
        if not crud.user.symbol_exist(db=db, symbol_in=order.symbol):
            log_msg(
                f"Adding a non-existent symbol on pending order of User(uid = {order.user_id}).",
                "WARNING",
            )
            return False

        # TODO check difference between add, commit, flush
        order_m = PendingOrder.subclass(order.order_type)(**order.dict())
        db.add(order_m)
        db.flush()
        return True

    @fail_save
    def delete_order(self, *, db: Session, id: int):
        order = db.query(PendingOrder).filter(PendingOrder.id == id).first()

        if order is None:
            log_msg(f"No limit order of id {id} exists. ", "ERROR")
            return False

        db.remove(order)
        db.flush()
        return True


pending_order = CRUDPendingOrder()
