// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract Borrowing is Ownable {
    using SafeMath for uint256;

    // Struct to hold borrowing details
    struct Borrow {
        uint256 amount;
        uint256 interestRate; // in basis points (1% = 100 basis points)
        uint256 duration; // in seconds
        uint256 startTime;
        address borrower;
        bool isActive;
    }

    // Mapping of borrow IDs to Borrow details
    mapping(uint256 => Borrow) public borrows;
    uint256 public borrowCounter;

    // Token used for borrowing
    IERC20 public token;

    // Events
    event BorrowCreated(uint256 borrowId, address indexed borrower, uint256 amount, uint256 interestRate, uint256 duration);
    event BorrowRepaid(uint256 borrowId, address indexed borrower);
    event BorrowLiquidated(uint256 borrowId, address indexed borrower);

    // Constructor to set the token address
    constructor(address _tokenAddress) {
        token = IERC20(_tokenAddress);
    }

    // Function to create a new borrow
    function createBorrow(uint256 _amount, uint256 _interestRate, uint256 _duration) external {
        require(_amount > 0, "Amount must be greater than 0");
        require(_interestRate > 0, "Interest rate must be greater than 0");
        require(_duration > 0, "Duration must be greater than 0");

        // Transfer tokens from borrower to contract as collateral
        token.transferFrom(msg.sender, address(this), _amount);

        // Create a new borrow
        borrows[borrowCounter] = Borrow({
            amount: _amount,
            interestRate: _interestRate,
            duration: _duration,
            startTime: block.timestamp,
            borrower: msg.sender,
            isActive: true
        });

        emit BorrowCreated(borrowCounter, msg.sender, _amount, _interestRate, _duration);
        borrowCounter++;
    }

    // Function to repay a borrow
    function repayBorrow(uint256 _borrowId) external {
        Borrow storage borrow = borrows[_borrowId];
        require(borrow.isActive, "Borrow is not active");
        require(borrow.borrower == msg.sender, "Only borrower can repay the borrow");

        uint256 interest = calculateInterest(borrow.amount, borrow.interestRate, borrow.duration);
        uint256 totalRepayment = borrow.amount.add(interest);

        // Transfer tokens from borrower to contract for repayment
        token.transferFrom(msg.sender, address(this), totalRepayment);

        // Mark borrow as repaid
        borrow.isActive = false;

        // Transfer collateral back to borrower
        token.transfer(msg.sender, borrow.amount);

        emit BorrowRepaid(_borrowId, msg.sender);
    }

    // Function to liquidate a borrow
    function liquidateBorrow(uint256 _borrowId) external {
        Borrow storage borrow = borrows[_borrowId];
        require(borrow.isActive, "Borrow is not active");
        require(block.timestamp >= borrow.startTime + borrow.duration, "Borrow duration has not expired");

        // Mark borrow as liquidated
        borrow.isActive = false;

        // Transfer collateral to the contract owner (or liquidator)
        token.transfer(owner(), borrow.amount);

        emit BorrowLiquidated(_borrowId, borrow.borrower);
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
