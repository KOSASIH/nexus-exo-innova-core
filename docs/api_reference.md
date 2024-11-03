# API Documentation

## Introduction

This document provides an overview of the API endpoints available in the Nexus Exo Innova platform. The API follows RESTful principles and allows clients to interact with the backend services.

## Base URL

[https://api.nexus-exo-innova.com/v1](https://api.nexus-exo-innova.com/v1)


## Authentication

All API requests require an authentication token. Obtain the token by logging in and including it in the `Authorization` header:

```
Authorization: Bearer <token>
```

## Endpoints

### User Management

#### Register User

- **POST** `/users/register`
- **Description**: Registers a new user.
- **Request Body**:
  ```json
  1 {
  2   "username": "string",
  3   "email": "string",
  4   "password": "string"
  5 }
  ```
  
Response:
- **201 Created**: User registered successfully.
- **400 Bad Request**: Validation errors.

### Login User
- **POST** /users/login
- **Description**: Authenticates a user and returns a token.
- **Request Body**:

   ```json
   1 {
   2   "email": "string",
   3   "password": "string"
   4 }
   ```
   
Response:
- **200 OK**: Returns user details and token.
- **401 Unauthorized**: Invalid credentials.

## DeFi Operations
### Lend Assets
- **POST** /lending
- **Description**: Lends assets to the platform.
- **Request Body**:

   ```json
   1 {
   2   "asset": "string",
   3   "amount": "number",
   4   "duration": "number"
   5 }
   ```
   
Response:
- **200 OK**: Lending operation successful.
- **400 Bad Request**: Validation errors.

### Borrow Assets
- **POST** /borrowing
- **Description**: Borrows assets from the platform.
- **Request Body**:

   ```json
   1 {
   2   "asset": "string",
   3   "amount": "number"
   4 }
   ```
   
Response:
- **200 OK**: Borrowing operation successful.
- **400 Bad Request**: Validation errors.

## NFT Operations
### Create NFT
- **POST** /nft/create
- **Description**: Creates a new NFT.
- **Request Body**:

   ```json
   1 {
   2   "title":
   3  
   4 "string", "description": "string", "image": "string"
   5 }
   ```

- **Response**:
- **201 Created**: NFT created successfully.
- **400 Bad Request**: Validation errors.

#### Buy NFT

- **POST** `/nft/buy`
- **Description**: Buys an existing NFT.
- **Request Body**:
   ```json
   1 {
   2   "nftId": "string",
   3   "price": "number"
   4 }
   ```

Response:
- **200 OK**: NFT purchase successful.
- **400 Bad Request**: Validation errors.

## Wallet Operations
### Get Wallet Balance
- **GET** /wallet/balance
- **Description**: Retrieves the user's wallet balance.

Response:
- **200 OK**: Returns wallet balance.
- **401 Unauthorized**: Invalid token.

### Send Assets
- **POST** /wallet/send
- **Description**: Sends assets to another user.
- **Request Body**:

   ```json
   1 {
   2   "recipient": "string",
   3   "asset": "string",
   4   "amount": "number"
   5 }
   ```

Response:
- **200 OK**: Asset transfer successful.
- **400 Bad Request**: Validation errors.

### Error Handling
The API uses standard HTTP status codes to indicate the outcome of a request. In case of an error, the response body will contain a JSON object with an error property describing the issue.

   ```json
   1 {
   2   "error": "string"
   3 }
   ```

# Conclusion
The Nexus Exo Innova API provides a robust and scalable interface for clients to interact with the platform's services. This documentation serves as a reference for developers integrating with the API.
