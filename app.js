// app.js

// Initialize Web3
if (typeof web3 !== 'undefined') {
    web3 = new Web3(web3.currentProvider);
} else {
    // Set up Web3 provider for Ganache CLI
    web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
}

// Load the contract ABI (replace with your ABI)
const contractABI = [
    // ABI here
];

// Replace 'contractAddress' with the address where your contract is deployed
const contractAddress = '0x123...';

// Create a contract instance
const charityContract = new web3.eth.Contract(contractABI, contractAddress);

// Example function to get all charity projects
async function getAllCharityProjects() {
    const numProjects = await charityContract.methods.getNumCharityProjects().call();
    const projects = [];

    for (let i = 0; i < numProjects; i++) {
        const project = await charityContract.methods.getCharityProject(i).call();
        projects.push(project);
    }

    return projects;
}

// Example function to create a new charity project
async function createCharityProject(title, description, targetAmount, walletAddress) {
    // Assuming you have a function in your contract named 'createCharityProject'
    await charityContract.methods.createCharityProject(title, description, targetAmount, walletAddress).send({from: ethereum.selectedAddress});
}

// Example function to donate to a charity project
async function donateToProject(projectId, amount) {
    // Assuming you have a function in your contract named 'donate'
    await charityContract.methods.donate(projectId, amount).send({from: ethereum.selectedAddress, value: amount});
}

// Example usage
window.onload = async function() {
    const allProjects = await getAllCharityProjects();
    console.log(allProjects); // Display all charity projects retrieved from the contract
}
