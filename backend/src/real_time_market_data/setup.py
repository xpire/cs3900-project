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
    sim00=[100, 200, 300],
    sim01=[20, 40, 80, 160, 80],
    sim02=[300, 30, 100, 400],
    sim10=[100, 200, 300],
    sim11=[20, 40, 80, 160, 80],
    sim12=[300, 30, 100, 400],
    sim20=[100, 200, 300],
    sim21=[20, 40, 80, 160, 80],
    sim22=[300, 30, 100, 400],
    sim30=[100, 200, 300],
    sim31=[20, 40, 80, 160, 80],
    sim32=[300, 30, 100, 400],
)


def create_simulators(db):
    global stock_details

    simulators = []
    for symbol, day_patterns in stock_details.items():
        stock = crud.stock.get_stock_by_symbol(db=db, stock_symbol=symbol)
        simulators.append(StockSimulator(stock, day_patterns))
    return simulators
