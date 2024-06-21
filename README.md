# Project 1.8: Smart Contract on the Algorand Blockchain

### Bondio Francesco, Bortoletti Adele, Razuri Olazo Eitan, Trovò Karin

This document outlines the implementation of a blockchain-based voting system for the academic senate using the Algorand blockchain. By leveraging blockchain technology, this project aims to enhance the transparency, security, efficiency, and trust of the voting process.

## System Workflow
The voting system operates as follows:
- **Wallet Creation and Public Key Submission**: Senators create an Algorand wallet and submit their public keys.
- **Token Distribution**: Each senator receives a USIV coin for voting.
- **Casting Votes**: Votes are cast using the USIV coin along with the senator’s choice.
- **Finality and Unchangeability**: Once cast, votes are final and unalterable.

## Directory Structure
The project is organized into several directories and subdirectories, containing various scripts, notebooks, and assets crucial for the Smart Contract Senate system. Below is a simplified overview of the directory structure:

- **code**
  - 00-voting-app.ipynb
    
  – 01-members-credentials.ipynb
  
  – 02-club-token.ipynb
  
  – 03-members-receive-club-token.ipynb
  
  – 04-voting-smart-contract.ipynb

- **assets**
  – token
    - token_info

  - credentials
    – credentials_temp

## Requirements
The implementation of our Smart Contract on the Algorand blockchain was primarily driven using Python, since it facilitates interactions. Throughout the project, Python’s Algorand SDK enabled direct communication with the Algorand network to execute smart contracts and manage blockchain transactions effectively.

## Conclusion
The outcome of this project illustrates a method of creating a secure voting system using blockchain technology. The implementation of a smart contract for the Senate Voting System demonstrates how blockchain can help institutional frameworks by providing a platform that is both verifiable and immutable.
