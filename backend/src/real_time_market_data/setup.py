"""
sim00,Ecksdee UNSW,XD00,Simulated,Private,AUD
sim01,Ecksdee UNSW,XD00,Simulated,Private,AUD
sim02,Ecksdee UNSW,XD00,Simulated,Private,AUD
sim10,Ecksdee UNSW,XD06,Simulated,Private,AUD
sim11,Ecksdee UNSW,XD06,Simulated,Private,AUD
sim12,Ecksdee UNSW,XD06,Simulated,Private,AUD
sim21,Ecksdee UNSW,XD12,Simulated,Private,AUD
sim22,Ecksdee UNSW,XD12,Simulated,Private,AUD
sim20,Ecksdee UNSW,XD12,Simulated,Private,AUD
sim30,Ecksdee UNSW,XD18,Simulated,Private,AUD
sim31,Ecksdee UNSW,XD18,Simulated,Private,AUD
sim32,Ecksdee UNSW,XD18,Simulated,Private,AUD
"""
from src import crud
from src.real_time_market_data.simulated_stock import StockSimulator

stock_details = dict(
    # symbol = (day_lo, day_hi, rise_at_pivot)
    sim00=(100, 100, True),
    sim01=(50, 200, True),
    sim02=(50, 200, False),
    sim10=(100, 100, True),
    sim11=(50, 200, True),
    sim12=(50, 200, False),
    sim20=(100, 100, True),
    sim21=(50, 200, True),
    sim22=(50, 200, False),
    sim30=(100, 100, True),
    sim31=(50, 200, True),
    sim32=(50, 200, False),
)


def create_simulators(db):
    global stock_details

    simulators = []
    for symbol, (lo, hi, rise_at_pivot) in stock_details.items():
        stock = crud.stock.get_stock_by_symbol(db=db, stock_symbol=symbol)
        simulators.append(StockSimulator(stock, lo, hi, rise_at_pivot))
    return simulators
