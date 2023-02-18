# Tighten

Automatic tight struct packing optimization for Solidity

**V2:** Works purely on struct packing logic, no compilation. 

**V1 (old):** Compiles and checks the output on a sample contract using foundry gas reporter

**NOTE**: This is a work in progress! Verify the results on your own. V2 is more accurate. V1 will take exponential time on large inputs. 

## Prerequisites

Only for V1: Make sure Foundry is installed. This is used in calculating gas using a sample contract. 

## Usage 

### V2

```
python tightenV2.py <struct_data_types>
```

Example:

```
python tightenV2.py uint256 bytes10 bytes20 bytes30 bytes32 address uint16 uint8
```

![example](https://github.com/az0mb13/tighten/blob/master/eg2.png?raw=true)


### V1

```
python tighten.py <struct_data_types>
```

Example:

```
python tighten.py uint,bytes,int,bool,address,uint256
```
![example](https://github.com/az0mb13/tighten/blob/master/eg.png?raw=true)

## To Do's

- Add support for all the remaining data types
- Beautify output struct order
