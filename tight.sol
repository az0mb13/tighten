pragma solidity 0.8.9;

contract tight {
    struct INVOICE {
        uint256 tokenId;
        address to;
        address from;
        uint256 openedOn;
        uint256 closedOn;
        STATUS status;
        PAYMENT_MODE paymentMode;
        uint256 amount;
        string invoiceUrl; //only hash is stored
        uint256 dummyId; //doc num
        uint256 cut;
        string aliass;
        string refNo;
        string serviceDate;
        string imageUrl; //only hash is stored
    }

    struct tests {
        uint256 a;
        uint256 b;
        bool c;
    }

    function setInvoice() external {
        tests memory test = tests(1, 2, true);
    }
}
