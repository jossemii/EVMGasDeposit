pragma solidity ^0.8.11;

contract Deposit {
    address public owner;
    mapping(bytes32 => uint) public token_list;

    event NewSession(bytes32 token, uint amount);
    constructor() public {
        owner = msg.sender;
    }

    function add_gas(bytes32 token) public payable {
        token_list[token] += msg.value;
        emit NewSession(token, msg.value);
    }

    function get_gas(bytes32 token) public view returns (uint) {
        return token_list[token];
    }

    function get_owner() public view returns (address) {
        return owner;
    }
}