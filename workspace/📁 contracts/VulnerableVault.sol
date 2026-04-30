// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract VulnerableVault {
    mapping(address => uint256) public balances;
    mapping(address => bool) public authorizedCallers;
    address public owner;
    
    constructor() {
        owner = msg.sender;
    }
    
    function deposit() external payable {
        require(msg.value > 0, "Must send ETH");
        balances[msg.sender] += msg.value;
    }
    
    function withdraw(uint256 amount) external {
        // REENTRANCY VULNERABILITY: External call before state update
        (bool success,) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
        
        // State update happens AFTER external call
        balances[msg.sender] -= amount;
    }
    
    function setAuthorizedCaller(address caller, bool authorized) external {
        // AUTHENTICATION BYPASS: No access control check
        authorizedCallers[caller] = authorized;
    }
    
    function mint(address to, uint256 amount) external {
        // AUTHENTICATION BYPASS: No access control
        // UNRESTRICTED MINT: Anyone can mint tokens
        balances[to] += amount;
    }
    
    function getBalance(address account) external view returns (uint256) {
        return balances[account];
    }
    
    function transferOwnership(address newOwner) external {
        // AUTHENTICATION BYPASS: No access control
        owner = newOwner;
    }
    
    // Fallback function to enable reentrancy attacks
    receive() external payable {
        // If called during withdrawal, could trigger recursive calls
    }
}
