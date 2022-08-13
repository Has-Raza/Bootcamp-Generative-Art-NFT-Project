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
