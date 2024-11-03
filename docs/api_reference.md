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
  
