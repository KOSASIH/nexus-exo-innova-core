// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/IERC721Metadata.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract NFTMarketplace is Ownable {
    using SafeMath for uint256;
    using Counters for Counters.Counter;

    // Struct to hold NFT listing details
    struct Listing {
        uint256 id;
        address seller;
        address nftContract;
        uint256 tokenId;
        uint256 price;
        bool isActive;
    }

    // State variables
    Counters.Counter private _listingIdCounter;
    mapping(uint256 => Listing) public listings;
    mapping(address => mapping(uint256 => bool)) public isListed; // nftContract => tokenId => isListed
    uint256 public marketplaceFee; // Fee in basis points (1% = 100 basis points)

    // Events
    event Listed(uint256 indexed listingId, address indexed seller, address indexed nftContract, uint256 tokenId, uint256 price);
    event Unlisted(uint256 indexed listingId, address indexed seller);
    event Sold(uint256 indexed listingId, address indexed buyer, address indexed nftContract, uint256 tokenId, uint256 price);

    // Constructor to set the initial marketplace fee
    constructor(uint256 _marketplaceFee) {
        marketplaceFee = _marketplaceFee;
    }

    // Function to list an NFT for sale
    function listNFT(address _nftContract, uint256 _tokenId, uint256 _price) external {
        require(_price > 0, "Price must be greater than 0");
        require(IERC721(_nftContract).ownerOf(_tokenId) == msg.sender, "You must own the NFT to list it");
        require(!isListed[_nftContract][_tokenId], "NFT is already listed");

        // Transfer the NFT to the marketplace
        IERC721(_nftContract).transferFrom(msg.sender, address(this), _tokenId);

        // Create a new listing
        _listingIdCounter.increment();
        uint256 listingId = _listingIdCounter.current();
        listings[listingId] = Listing({
            id: listingId,
            seller: msg.sender,
            nftContract: _nftContract,
            tokenId: _tokenId,
            price: _price,
            isActive: true
        });
        isListed[_nftContract][_tokenId] = true;

        emit Listed(listingId, msg.sender, _nftContract, _tokenId, _price);
    }

    // Function to unlist an NFT
    function unlistNFT(uint256 _listingId) external {
        Listing storage listing = listings[_listingId];
        require(listing.isActive, "Listing is not active");
        require(listing.seller == msg.sender, "You are not the seller");

        // Transfer the NFT back to the seller
        IERC721(listing.nftContract).transferFrom(address(this), msg.sender, listing.tokenId);

        // Mark the listing as inactive
        listing.isActive = false;
        isListed[listing.nftContract][listing.tokenId] = false;

        emit Unlisted(_listingId, msg.sender);
    }

    // Function to buy an NFT
    function buyNFT(uint256 _listingId) external payable {
        Listing storage listing = listings[_listingId];
        require(listing.isActive, "Listing is not active");
        require(msg.value >= listing.price, "Insufficient funds sent");

        // Calculate the marketplace fee
        uint256 fee = listing.price.mul(marketplaceFee).div(10000);
        uint256 sellerAmount = listing.price.sub(fee);

        // Transfer the NFT to the buyer
        IERC721(listing.nftContract).transferFrom(address(this), msg.sender, listing.tokenId);

        // Transfer the funds to the seller
        payable(listing.seller).transfer(sellerAmount);

        // Transfer the fee to the owner of the marketplace
        payable(owner()).transfer(fee);

        // Mark the listing as inactive
        listing.isActive = false;
        isListed[listing.nftContract][listing.tokenId] = false;

        emit Sold(_listingId, msg.sender, listing.nftContract, listing.tokenId, listing.price);
    }

    // Function to set the marketplace fee (only owner)
    function setMarketplaceFee(uint256 _marketplaceFee) external onlyOwner {
        marketplaceFee = _marketplaceFee;
    }

    // Function to withdraw funds in case of emergency (only owner)
    function withdrawFunds() external onlyOwner {
        uint256 balance = address(this).balance;
        require(balance > 0, "No funds to withdraw");
        payable(owner()).transfer(balance);
    }

    // Function to get listing details
    function getListing(uint256 _listingId) external view returns (Listing memory) {
        return listings[_listingId];
    }

    // Function to get the total number of listings
    function getTotalListings() external view returns (uint256) {
        return _listingIdCounter.current();
    }

    // Function to check if an NFT is listed
    function checkIfListed(address _nftContract, uint256 _tokenId) external view returns (bool) {
        return isListed[_nftContract][_tokenId];
    }
}
