import os
import json
from eth_account import account
from eth_typing import abi
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st



load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB_PROVIDER_URI")))

@st.cache(allow_output_mutation=True)

def load_contract():
	with open(Path('./contracts/compiled/Auction.json')) as f:
	    auction_abi = json.load(f)
	contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
	contract = w3.eth.contract(
		address=contract_address,
		abi=auction_abi
	)

	return contract

contract = load_contract()

car_database = {
    "Gwagon": ["Gwagon", "0x909dcf46F6F0e7cA8873925512A0ff1d2FeFab99", "New", 2, "Images/Gwagon.jpeg"],
    "Mercedes Benz": ["Mercedes Benz", "0x3d3C97BC739D7a2723183Fc65D9F2E2D89e7B39d", "New", 3, "Images/mercedes-benz-ag.jpg"],
    "Portia911": ["Portia911", "0x834f5789AdADc68c8900a85c7DcD813CcD8b964b", "New", 5, "Images/Portia911.jpg"],
    "Subaru stationwagon": ["Subaru stationwagon", "0x68954BE07F95A82E60D01e8D0caff759410bda30", "Used", .5, "Images/subaru-stationwagon.jpg"],
    "Tesla ModelX": ["Tesla ModelX", "0x778822F90fAc0DB90537473c2336e63Bb7A270Dc", "New", 4, "Images/Tesla Modelx.jpeg"],
    "Python Monster Truck": ["Python Monster Truck", "0x2E7a71BF2FEc933622095A16a06463d7fc79DeF3", "Used", 2, "Images/Python Monster Truck.jpg"]
}

# A list of the Cars avaliable for Auction
car = ["Gwagon", "Mercedes Benz", "Portia911", "Subaru Stationwagon", "Tesla ModelX", "Python Monster Truck"]


def get_car():
    """Display the database of car information."""
    db_list = list(car_database.values())

    for number in range(len(car)):
        st.image(db_list[number][4], width=200)
        st.write("Name: ", db_list[number][0])
        st.write("Ethereum Account Address: ", db_list[number][1])
        st.write("Condition: ", db_list[number][2])
        st.write("Minimum Bid: ", db_list[number][3], "eth")
        st.text(" \n")

# Streamlit Code

# Streamlit application headings
st.markdown("# Cars R Us Auction!")
st.markdown("## Bid For The Car Of Your Dreams!")
st.text(" \n")

# Streamlit Sidebar Code - Start
get_car()

st.sidebar.markdown("## Client Account Address and Ethernet Balance in Ether")

# Write the client's Ethereum account address to the sidebar
st.sidebar.write()

# Create a select box to chose a car to bid on
car = st.sidebar.selectbox('Select a Car', car)

# Create a input field to record the initial bid
starting_bid = st.sidebar.number_input("Bid")

st.sidebar.markdown("## Car, Minimum Bid, and Ethereum Address")

# Identify the Car for auction
car = car_database[car][0]

# Write the car's name to the sidebar
st.sidebar.write(car)

# Identify the the starting bid for the car being auctioned
starting_bid = car_database[car][3]

# Write the cars starting bid
st.sidebar.write(starting_bid)

# Identify the auction owner's Ethereum Address
car_address = car_database[car][1]

# Write the inTech auction owner's Ethereum Address to the sidebar
st.sidebar.write(car_address)

if st.sidebar.button("Bid"):
    contract.functions.bid().transact({'from': account, 'gas': 3000000})

if st.sidebar.button("Withdraw"):
    contract.functions.withdraw()

if st.sidebar.button("Auction End"):
    contract.functions.auctionEnd()

st.sidebar.markdown("## Highest Bid in Ether")