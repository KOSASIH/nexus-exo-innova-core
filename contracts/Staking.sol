// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract Staking is Ownable, ReentrancyGuard {
    using SafeMath for uint256;

    // Struct to hold staking details
    struct Stake {
        uint256 amount;
        uint256 rewardDebt; // Amount of rewards already claimed
        uint256 lastStakedTime; // Last time the user staked
    }

    // Mapping of user addresses to their stakes
    mapping(address => Stake) public stakes;

    // Total staked amount
    uint256 public totalStaked;

    // Token used for staking
    IERC20 public stakingToken;

    // Reward token
    IERC20 public rewardToken;

    // Reward rate (tokens per second)
    uint256 public rewardRate;

    // Events
    event Staked(address indexed user, uint256 amount);
    event Unstaked(address indexed user, uint256 amount);
    event RewardPaid(address indexed user, uint256 reward);

    // Constructor to set the token addresses and reward rate
    constructor(address _stakingToken, address _rewardToken, uint256 _rewardRate) {
        stakingToken = IERC20(_stakingToken);
        rewardToken = IERC20(_rewardToken);
        rewardRate = _rewardRate;
    }

    // Function to stake tokens
    function stake(uint256 _amount) external nonReentrant {
        require(_amount > 0, "Amount must be greater than 0");

        // Update user's stake
        Stake storage userStake = stakes[msg.sender];
        updateReward(msg.sender);

        // Transfer tokens from user to contract
        stakingToken.transferFrom(msg.sender, address(this), _amount);

        // Update total staked amount
        totalStaked = totalStaked.add(_amount);
        userStake.amount = userStake.amount.add(_amount);
        userStake.lastStakedTime = block.timestamp;

        emit Staked(msg.sender, _amount);
    }

    // Function to unstake tokens
    function unstake(uint256 _amount) external nonReentrant {
        Stake storage userStake = stakes[msg.sender];
        require(userStake.amount >= _amount, "Insufficient staked amount");

        // Update rewards before unstaking
        updateReward(msg.sender);

        // Transfer tokens back to user
        stakingToken.transfer(msg.sender, _amount);

        // Update total staked amount
        totalStaked = totalStaked.sub(_amount);
        userStake.amount = userStake.amount.sub(_amount);

        emit Unstaked(msg.sender, _amount);
    }

    // Function to claim rewards
    function claimRewards() external nonReentrant {
        updateReward(msg.sender);
    }

    // Internal function to update rewards for a user
    function updateReward(address _user) internal {
        Stake storage userStake = stakes[_user];
        uint256 pendingReward = calculateReward(_user);
        if (pendingReward > 0) {
            userStake.rewardDebt = userStake.rewardDebt.add(pendingReward);
            rewardToken.transfer(_user, pendingReward);
            emit RewardPaid(_user, pendingReward);
        }
    }

    // Function to calculate pending rewards for a user
    function calculateReward(address _user) public view returns (uint256) {
        Stake storage userStake = stakes[_user];
        uint256 stakedDuration = block.timestamp.sub(userStake.lastStakedTime);
        uint256 reward = userStake.amount.mul(rewardRate).mul(stakedDuration).div(1e18);
        return reward.sub(userStake.rewardDebt);
    }

    // Function to withdraw tokens in case of emergency (only owner)
    function emergencyWithdraw(uint256 _amount) external onlyOwner {
        stakingToken.transfer(msg.sender, _amount);
    }

    // Function to withdraw reward tokens in case of emergency (only owner)
    function emergencyWithdrawRewards(uint256 _amount) external onlyOwner {
        rewardToken.transfer(msg.sender, _amount);
    }
}
