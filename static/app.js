// let provider;
// let accounts;
// //const web3 = new Web3();
// let accountAddress = "";
// let signer;
// let web3_flag = 0;
// let img_url;
// let tweet_url;
// let data;
// let ChainId;
// let nft_msg_before_loading;
// let tweetIdFromUrl;
// let smartcontract_addr;
// let transation_hash;
// let ChainId_db;
// //const Web3 = require("web3");

// function construct_Web3_Validation()
// { 
//     console.log(web3_flag);
//     console.log(url_web3);    
//     if (web3_flag == 1)
//     {
//         document.getElementById("web3_msg").innerHTML = document.getElementById("web3_msg").innerHTML + url_web3;
//     }
// }

// if(ChainId == 4){ 
//     smartcontract_addr = data['contract_address'];
//     var myContract = await new window.web3.eth.Contract(abi, data['contract_address'], {from: accountAddress, // default from address
//     gasPrice: '20000000000' // default gas price in wei, 20 gwei in this case
// });
//     console.log("[[11]]");
//     //console.log(myContract.options);
// myContract.methods.mint(accountAddress, tokenUri).send({from: accountAddress})
// .then(function(receipt)                                  
// {
//     console.log("[[12]]");
// // receipt can also be a new contract instance, when coming from a "contract.deploy({...}).send()"
//     console.log(receipt);
//     console.log("[[13]]");    
//     document.getElementById("nft_msg2").innerHTML = "<h4> NFT Minted! </h4><p style='text-align:left;'>Congratulations! <br>Here is your Transaction Hash:<br><a target='_blank'  href='https://rinkeby.etherscan.io/tx/"+String(receipt['transactionHash']) + "'>" + String(receipt['transactionHash'])+"</a></p>";
//     transation_hash = receipt['transactionHash'];
//     ChainId_db = "4";
//     writeNFTToDB("0 - Minted");
                                
// })
// .catch((error) => {
//       if (error['code'] === 4001) {
//         // EIP-1193 userRejectedRequest error
//         console.log('Please connect to MetaMask.');
//            document.getElementById("nft_msg2").innerHTML = "<h4> NFT could not be minted!</h4><p style='text-align:left;'>Looks like you <i>rejected</i> transaction signature.<br>So we cannot Mint your NFT. If you still want to Mint your NFT, please try again?</p>"; 
//                   transation_hash = "Not Minted";
//     ChainId_db = "4";          
//               writeNFTToDB("1 - Transaction Rejected");
//       } else {
//         console.error(error);
//                   transation_hash = "Not Minted";
//     ChainId_db = "4";          
//               writeNFTToDB("2 - Transaction Failed - Reason:"+ String(error).slice(0,25));          
//       }
//     });
// }

window.userWalletAddress = null
const connectWallet = document.getElementById('connectWallet')
const walletAddress = document.getElementById('walletAddress')
const sendTransaction = document.getElementById('sendTransaction')



function checkInstalled() {
  if (typeof window.ethereum == 'undefined') {
    connectWallet.innerText = 'MetaMask isnt installed, please install it'
    connectWallet.classList.remove()
    connectWallet.classList.add()
    return false
  }
  connectWallet.addEventListener('click', connectWalletwithMetaMask)
}

async function connectWalletwithMetaMask() {
  const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' })
  .catch((e) => {
  console.error(e.message)
  return
  })

  if (!accounts) { return }

  window.userWalletAddress = accounts[0]
  walletAddress.innerText = window.userWalletAddress

  connectWallet.innerText = 'Sign Out'
  connectWallet.removeEventListener('click', connectWalletwithMetaMask)
  setTimeout(() => {
    connectWallet.addEventListener('click', signOutOfMetaMask)
  }, 200)

}


function signOutOfMetaMask() {
  window.userwalletAddress = null
  walletAddress.innerText = ''
  connectWallet.innerText = 'Connect Wallet'

  connectWallet.removeEventListener('click', signOutOfMetaMask)
  setTimeout(() => {
    connectWallet.addEventListener('click', connectWalletwithMetaMask)
  }, 200  )
}

async function mintNFT() {
  let send = await window.ethereum.request({ method: "eth_sendTransaction",
  params: [ {

  }
  ]
}).catch((err)=> {
    console.log(err)
})

console.log(parseFloat((send) / Math.pow(10,18)))

sendTransaction.innerText = parseFloat((send) / Math.pow(10,18))
}

window.addEventListener('DOMContentLoaded', () => {
  checkInstalled()
})
