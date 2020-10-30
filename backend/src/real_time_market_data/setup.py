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
import itertools as it

import numpy as np
from src import crud
from src.real_time_market_data.simulated_stock import StockSimulator

patterns = [
    list(200 + 100 * np.sin(np.linspace(-np.pi, np.pi - np.pi / 14, 27))),
    list(np.cos(np.linspace(-np.pi, np.pi - np.pi / 14, 27))),
    list(np.sin(np.linspace(-np.pi, np.pi - np.pi / 14, 27))),
]

stock_details = dict(
    sim00=patterns[0],
    sim01=patterns[1],
    sim02=patterns[2],
    sim10=patterns[0],
    sim11=patterns[1],
    sim12=patterns[2],
    sim20=patterns[0],
    sim21=patterns[1],
    sim22=patterns[2],
    sim30=patterns[0],
    sim31=patterns[1],
    sim32=patterns[2],
)


def create_simulators(db):
    global stock_details

    simulators = []
    for symbol, day_patterns in stock_details.items():
        stock = crud.stock.get_stock_by_symbol(db=db, stock_symbol=symbol)
        simulators.append(StockSimulator(stock, day_patterns))
    return simulators
