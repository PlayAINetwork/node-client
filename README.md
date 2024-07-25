# PlayAI Node Client

## Description

**PlayAI node** facilitates offchain computation tasks, specifically the validation of rawVideos recorded by users. RawVideos can be large in size, so distributing these tasks increases efficiency, and in turn, the users who run the nodes are rewarded.This git repo includes the client code that can be used to run the node.

## Overview

The architecture involves simple communication between the Client and Server. The main components are:

- **Node Client**: Fetches tasks and submits the results.
- **Backend Server**: Assigns tasks to clients, tracks task execution, and collects results.
- **Smart Contract**: Comprises three contracts:
  1. **Tasks on-chain contract**: Where task data is posted by the backend server.
  2. **NFT contract for node sale**: Acts as whitelisting for nodes and verifies attestation.

## Backend Server Functionalities

- **Generate tasks**: Upon receiving rawVideo, generate tasks and define receiver clients.
- **Assign tasks**: Assign tasks to clients by checking their health status via the `/health` endpoint.
- **Expose endpoints**: 
  - `/taskInfo`: For clients to fetch task information.
  - `/taskResult`: For clients to submit results.
- **Track tasks**: Track tasks and submit execution of tasks on the smart contract as an aggregator upon reaching a response threshold.

## Node Client Functionalities

- **Expose `/health` endpoint**: To show active status.
- **Fetch tasks**: Fetch tasks from the server at specific intervals.
- **Execute tasks**: Execute tasks by applying compute rules (currently, this involves downloading a file and defaulting it to true).
- **Send results**: Send the result of tasks to the server along with a signed signature.

## Running a Node

Running a node is simple:

``` curl -sL1 https://node.playai.network/run.sh | bash ```

This command pulls a script that installs the required packages and requests environment variables within the console.

Alternatively, users can clone the node repository, create a new .env file from .env.example, and follow the commands manually.


## System Requirements
PlayAI nodes can run on various systems, from low specification nodes with 2GB RAM to high specification nodes with 16GB RAM. Rewards are based on aggregated task responses over time, not just single responses.

## Packages and Dependencies
Docker

## External Ports
Ensure port 3000 is open by default, or configure it in the ENV file.

## Important Aspects

- **Uptime checks**: The server periodically check for uptime by pinging nodes, expecting a 200 response. Unavailability will lead to non-assignment of tasks, reduced rewards, and potential blacklisting.
- **Unique identifier ID**: Users using node receive a unique identifier ID, issued once per nodeKey, linked to the PlayAI Dashboard. Multiple unique IDs can be issued unless submitted via the PlayAI Dashboard.
- **NodeKey sale**: The NodeKey sale will involve an NFT, allowing the owner to delegate a burner address for running nodes, ensuring the NodeKey Holder doesn't need to use their private key. This allows for unique private keys for each user and unique IDs issuance.





