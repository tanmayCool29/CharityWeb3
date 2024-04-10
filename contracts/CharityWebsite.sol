// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract CharityWebsite {

    struct CharityProject {
        string title;
        string description;
        uint targetAmount;
        address walletAddress;
        uint amountReceived;
    }

    CharityProject[] public charityProjects;

    event CharityProjectCreated(uint indexed projectId, string title, string description, uint targetAmount, address walletAddress);
    event DonationMade(uint indexed projectId, address indexed donor, uint amount);

    function listAllCharityProjects() public view returns (uint[] memory) {
        uint[] memory projectIds = new uint[](charityProjects.length);
        for (uint i = 0; i < charityProjects.length; i++) {
            projectIds[i] = i;
        }
        return projectIds;
    }

    function createCharityProject(string memory _title, string memory _description, uint _targetAmount, address _walletAddress) public {
        charityProjects.push(CharityProject(_title, _description, _targetAmount, _walletAddress, 0));
        uint projectId = charityProjects.length - 1;
        emit CharityProjectCreated(projectId, _title, _description, _targetAmount, _walletAddress);
    }

    function donate(uint _projectId, uint _amount) public payable {
        require(_projectId < charityProjects.length, "Invalid project ID");
        require(_amount > 0, "Donation amount must be greater than 0");

        charityProjects[_projectId].amountReceived += _amount;
        emit DonationMade(_projectId, msg.sender, _amount);
    }

    function getCharityProject(uint _projectId) public view returns (string memory title, string memory description, uint targetAmount, address walletAddress, uint amountReceived) {
        require(_projectId < charityProjects.length, "Invalid project ID");

        CharityProject memory project = charityProjects[_projectId];
        return (project.title, project.description, project.targetAmount, project.walletAddress, project.amountReceived);
    }

    function getNumCharityProjects() public view returns (uint) {
        return charityProjects.length;
    }
}
