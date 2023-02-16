# Tighten

Automatic tight struct packing optimization for Solidity

**NOTE**: This is a work in progress! Verify the results on your own.

## Prerequisites

Make sure Foundry is installed. This is used in calculating gas using a sample contract. 

## Usage 

```
python tighten.py <struct_data_types>
```

Example:

```
python tighten.py bool,uint256,uint8
```
![example](https://github.com/az0mb13/tighten/blob/master/eg.png?raw=true)

## To Do's

- Add support for all the remaining data types
- Beautify output struct order
- Show all the ordering methods that are cheap instead of 1
