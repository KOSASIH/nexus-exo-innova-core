// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract Lending is Ownable {
    using SafeMath for uint256;

    // Struct to hold loan details
    struct Loan {
        uint256 amount;
        uint256 interestRate; // in basis points (1% = 100 basis points)
        uint256 duration; // in seconds
        uint256 startTime;
        address borrower;
        bool isActive;
    }

    // Mapping of loan IDs to Loan details
    mapping(uint256 => Loan) public loans;
    uint256 public loanCounter;

    // Events
    event LoanCreated(uint256 loanId, address indexed borrower, uint256 amount, uint256 interestRate, uint256 duration);
    event LoanRepaid(uint256 loanId, address indexed borrower);
    event LoanLiquidated(uint256 loanId, address indexed borrower);

    // Token used for lending
    IERC20 public token;

    // Constructor to set the token address
    constructor(address _tokenAddress) {
        token = IERC20(_tokenAddress);
    }

    // Function to create a new loan
    function createLoan(uint256 _amount, uint256 _interestRate, uint256 _duration) external {
        require(_amount > 0, "Amount must be greater than 0");
        require(_interestRate > 0, "Interest rate must be greater than 0");
        require(_duration > 0, "Duration must be greater than 0");

        // Transfer tokens from borrower to contract as collateral
        token.transferFrom(msg.sender, address(this), _amount);

        // Create a new loan
        loans[loanCounter] = Loan({
            amount: _amount,
            interestRate: _interestRate,
            duration: _duration,
            startTime: block.timestamp,
            borrower: msg.sender,
            isActive: true
        });

        emit LoanCreated(loanCounter, msg.sender, _amount, _interestRate, _duration);
        loanCounter++;
    }

    // Function to repay a loan
    function repayLoan(uint256 _loanId) external {
        Loan storage loan = loans[_loanId];
        require(loan.isActive, "Loan is not active");
        require(loan.borrower == msg.sender, "Only borrower can repay the loan");

        uint256 interest = calculateInterest(loan.amount, loan.interestRate, loan.duration);
        uint256 totalRepayment = loan.amount.add(interest);

        // Transfer tokens from borrower to contract for repayment
        token.transferFrom(msg.sender, address(this), totalRepayment);

        // Mark loan as repaid
        loan.isActive = false;

        // Transfer collateral back to borrower
        token.transfer(msg.sender, loan.amount);

        emit LoanRepaid(_loanId, msg.sender);
    }

    // Function to liquidate a loan
    function liquidateLoan(uint256 _loanId) external {
        Loan storage loan = loans[_loanId];
        require(loan.isActive, "Loan is not active");
        require(block.timestamp >= loan.startTime + loan.duration, "Loan duration has not expired");

        // Mark loan as liquidated
        loan.isActive = false;

        // Transfer collateral to the contract owner (or liquidator)
        token.transfer(owner(), loan.amount);

        emit LoanLiquidated(_loanId, loan.borrower);
    }

    // Function to calculate interest
    function calculateInterest(uint256 _amount, uint256 _interestRate, uint256 _duration) internal pure returns (uint256) {
        return _amount.mul(_interestRate).mul(_duration).div(365 days).div(10000); // Annualized interest
    }

    // Function to withdraw tokens from the contract (only owner)
    function withdrawTokens(uint256 _amount) external onlyOwner {
        token.transfer(msg.sender, _amount);
    }
}
