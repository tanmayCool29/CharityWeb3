const {Web3} = require('web3');
const contractABI = require('./build/contracts/CharityWebsite.json').abi;

const web3 = new Web3(new Web3.providers.HttpProvider('http://localhost:8545'));

const contractAddress = '0x03f5811C8e635202a085E3d4db703F7d306B51e0'; // Replace with your contract address
const charityContract = new web3.eth.Contract(contractABI, contractAddress);

async function getAllCharityProjects() {
    const numProjects = await charityContract.methods.getNumCharityProjects().call();
    const projects = [];

    for (let i = 0; i < numProjects; i++) {
        const project = await charityContract.methods.getCharityProject(i).call();
        projects.push(project);
    }

    return projects;
}

async function createCharityProject(title, description, targetAmount, walletAddress, fromAddress) {
    const gasPrice = await web3.eth.getGasPrice();
    const gasLimit = 2000000;

    await charityContract.methods.createCharityProject(title, description, targetAmount, walletAddress)
        .send({ from: fromAddress, gas: gasLimit, gasPrice: gasPrice });
}

module.exports = { getAllCharityProjects, createCharityProject };
