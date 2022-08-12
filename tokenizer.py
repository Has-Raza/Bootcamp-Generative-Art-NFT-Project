import os
import json
from web3 import Account
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import requests

load_dotenv()

# Create a W3 Connection
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/8cc726f0cb834d9c9ce2dcadf5c9f630"))
private_key = os.getenv("PRIVATE_KEY")
contract_address = "0x47fafd7EA2Ba599D553d2c4422CCbAddAD783273"

def generate_account(w3,private_key):
    account = Account.privateKeyToAccount(private_key)
    return account

# Set up Pinata Headers
json_headers = {
    "Content-Type":"application/json",
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_API_KEY")
}

file_headers = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_API_KEY")
}

def convert_data_to_json(content):
    data = {"pinataOptions":{"cidVersion":1}, 
            "pinataContent":content }
    return json.dumps(data)

def pin_file_to_ipfs(data):
    r = requests.post("https://api.pinata.cloud/pinning/pinFileToIPFS",
                      files={'file':data},
                      headers= file_headers)
    print(r.json())
    ipfs_hash = r.json()["IpfsHash"]
    return ipfs_hash

def pin_json_to_ipfs(json):
    r = requests.post("https://api.pinata.cloud/pinning/pinJSONToIPFS",
                      data=json,
                      headers= json_headers)
    print(r.json())
    ipfs_hash = r.json()["IpfsHash"]
    return ipfs_hash

def pin_nft(nft_name, nft_file,**kwargs):
    # Pin nft picture to IPFS
    ipfs_file_hash = pin_file_to_ipfs(nft_file.getvalue())

    # Build our NFT Token JSON
    token_json = {
       "name": nft_name,
       "image": f"ipfs.io/ipfs/{ipfs_file_hash}"
    }

    # Add extra attributes if any passed in
    token_json.update(kwargs.items())

    # Add to pinata json to be uploaded to Pinata
    json_data = convert_data_to_json(token_json)

    # Pin the real NFT Token JSON
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash, token_json


# Pull in Ethereum Account - Used for signing transactions
account = generate_account(w3,private_key)
st.write("Loaded Account Address: ", account.address)
st.write("Smart Contract Address: ", contract_address)

######################################################################
## Load the contract
######################################################################

@st.cache(allow_output_mutation=True)
def load_contract():
    with open(Path("contracts/compiled/art_abi.json")) as file:
        nft_abi = json.load(file)

    contract_address = "0x47fafd7EA2Ba599D553d2c4422CCbAddAD783273"

    nft_contract = w3.eth.contract(address=contract_address,
                    abi=nft_abi)

    return nft_contract            

contract = load_contract()
user_account = st.text_input("Enter Your Wallet Address", value="")
#private_key = st.text_input("Enter Your Private Key", value="")

############`#`#########################################################
## Streamlit Inputs
######################################################################

######################################################################
## Creating variables that describe the NFT
######################################################################
today = "t"

st.markdown("## Create the NFT")

nft_name = st.text_input("NFT Name: ")
creation_date = st.text_input("Date of creation: ", value=f"{today}")
about_the_nft = st.text_input("Addionial Message About the NFT", value="")

# Upload the Certificate Picture File
file = st.file_uploader("Upload an Image", type=["png","jpeg"])


######################################################################
## Button to Award the Certificate
######################################################################

if st.button("MINT"):

    nft_ipfs_hash,token_json = pin_nft(
        nft_name,
        file, 
        date_of_creation = creation_date, 
        details=about_the_nft)

    nft_uri = f"ipfs.io/ipfs/{nft_ipfs_hash}"

    nonce = w3.eth.getTransactionCount(account.address)
 
    tx = contract.functions.mint(user_account,nft_uri).buildTransaction({
        'chainId':4,
        'gas':20000000,
        'nonce':nonce
    })

    st.write("Raw TX: ", tx)

    signed_tx = account.sign_transaction(tx)

    st.write("Signed TX Hash: ", signed_tx.rawTransaction)

    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # This generally works on the mainnet - Rinkeby, not so much
    # receipt = w3.eth.waitForTransactionReceipt(tx_hash,timeout=300)      

    st.write("Transaction mined")
    # st.write(dict(receipt))

    st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
    st.markdown(f"[NFT IPFS Gateway Link] (https://{nft_uri})")
    st.markdown(f"[NFT IPFS Image Link] (https://{token_json['image']})")