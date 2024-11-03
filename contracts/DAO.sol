// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract DAO is Ownable {
    using SafeMath for uint256;

    // Struct to hold proposal details
    struct Proposal {
        uint256 id;
        address proposer;
        string description;
        uint256 voteCount;
        uint256 endTime;
        bool executed;
        mapping(address => bool) voters;
    }

    // State variables
    IERC20 public governanceToken;
    uint256 public proposalCount;
    uint256 public votingDuration;
    mapping(uint256 => Proposal) public proposals;

    // Events
    event ProposalCreated(uint256 indexed proposalId, address indexed proposer, string description);
    event Voted(uint256 indexed proposalId, address indexed voter);
    event ProposalExecuted(uint256 indexed proposalId);

    // Constructor to set the governance token and voting duration
    constructor(address _governanceToken, uint256 _votingDuration) {
        governanceToken = IERC20(_governanceToken);
        votingDuration = _votingDuration;
    }

    // Function to create a new proposal
    function createProposal(string memory _description) external {
        require(bytes(_description).length > 0, "Description cannot be empty");

        proposalCount++;
        Proposal storage newProposal = proposals[proposalCount];
        newProposal.id = proposalCount;
        newProposal.proposer = msg.sender;
        newProposal.description = _description;
        newProposal.endTime = block.timestamp.add(votingDuration);
        newProposal.executed = false;

        emit ProposalCreated(proposalCount, msg.sender, _description);
    }

    // Function to vote on a proposal
    function vote(uint256 _proposalId) external {
        Proposal storage proposal = proposals[_proposalId];
        require(block.timestamp < proposal.endTime, "Voting has ended");
        require(!proposal.voters[msg.sender], "You have already voted");

        uint256 voterBalance = governanceToken.balanceOf(msg.sender);
        require(voterBalance > 0, "You must hold governance tokens to vote");

        // Record the vote
        proposal.voters[msg.sender] = true;
        proposal.voteCount = proposal.voteCount.add(voterBalance);

        emit Voted(_proposalId, msg.sender);
    }

    // Function to execute a proposal
    function executeProposal(uint256 _proposalId) external {
        Proposal storage proposal = proposals[_proposalId];
        require(block.timestamp >= proposal.endTime, "Voting is still ongoing");
        require(!proposal.executed, "Proposal has already been executed");
        require(proposal.voteCount > 0, "No votes received");

        // Execute the proposal (this can be customized based on the proposal's purpose)
        // For example, transferring funds, changing parameters, etc.

        proposal.executed = true;

        emit ProposalExecuted(_proposalId);
    }

    // Function to withdraw governance tokens in case of emergency (only owner)
    function emergencyWithdrawTokens(uint256 _amount) external onlyOwner {
        governanceToken.transfer(msg.sender, _amount);
    }

    // Function to change the voting duration (only owner)
    function setVotingDuration(uint256 _duration) external onlyOwner {
        votingDuration = _duration;
    }
}
