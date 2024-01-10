import random
# from myFunctions import execute_this
from Prosumer import Prosumer
from Buyer import Buyer
import Market
from excel_readwrite import read_data_from_excel
import CONSTANTS



# @execute_this
def main():
    all_data = read_data_from_excel(CONSTANTS.DATA_FILE_PATH)
    prosumers = []
    buyers = []
    records_found = len(all_data['PV Capacity'])
    for x in range(records_found):
        # if all_data['Energy Generation'][x] >60:
        #     print(all_data["sr no"][x])
        prosumers.append(Prosumer(
            _id=x+1,
            init_money=random.randint(30, 1_000),
            energy_generation=all_data['PV Capacity'][x],
            selling_price=random.randint(2, 10),
            load=random.randint(1, 3),
            initial_energy=all_data['PV Capacity'][x],
            buying_price=random.randint(2, 10),
            max_capacity=random.randint(50, 100)))


    for x in range(records_found, records_found+40):
        buyers.append(Buyer(
            _id=x+1,
            init_money=random.randint(1_000, 2_000),
            buying_price=random.randint(2, 10),
            load=random.randint(1, 3),
            max_capacity=random.randint(50, 100),
            initial_energy=random.randint(5, 10)))

    market = Market.Market(10, 2)
    market.real_world_market(buyers=buyers, sellers=prosumers)
