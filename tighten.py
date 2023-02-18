import json
import sys
import itertools
import os
import subprocess
import re
import shutil
from tabulate import tabulate


def forgeit():
    try:
        output = subprocess.check_output(
            ['forge', 'test', '--gas-report', '--json'])
        output_str = output.decode("utf-8")
        parse_json(output_str)
    except subprocess.CalledProcessError as e:
        print("Error: ", e)


def deletit(directories):
    for directory in directories:
        for root, dirs, files in os.walk(directory):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))


def generate_table(data):
    table_data = [[i+1, item[0], item[1]] for i, item in enumerate(data)]
    headers = ["#", "Struct Order", "Gas"]
    print(tabulate(table_data, headers, tablefmt="fancy_grid"))


def parse_json(output):
    output = output.split("\n")
    json_data = ""
    for line in output:
        if "{" in line:
            json_data = line
            break
    # print(json_data)
    data = json.loads(json_data)
    min_gas = float('inf')
    min_gas_objects = []
    for key, value in data.items():
        # Extract the object name
        object_name = key.split('test/')[1].split('.sol')[0]

        # Extract the gas cost
        gas_cost = value["test_results"]["test()"]["kind"]["Standard"]
        if gas_cost < min_gas:
            min_gas = gas_cost
            min_gas_objects = [(object_name.replace("_", ","), gas_cost)]
        elif gas_cost == min_gas:
            min_gas_objects.append((object_name.replace("_", ","), gas_cost))
    generate_table(min_gas_objects)


def tightenit(data_types):
    # Get all possible combinations of data types
    for combination in itertools.permutations(data_types):
        struct_vars = []
        for i, data_type in enumerate(combination):
            struct_vars.append(f'{data_type} arg{i};')
        struct_vars_str = ''.join(struct_vars)

        sample_values = []
        for i, data_type in enumerate(combination):
            if 'uint' in data_type:
                sample_values.append("1")
            elif 'int' in data_type:
                sample_values.append("1")
            elif 'bytes' in data_type:
                sample_values.append("\"a\"")
            elif 'bool' in data_type:
                sample_values.append("true")
            elif 'address' in data_type:
                sample_values.append(
                    "0x0000000000000000000000000000000000000000")
            elif 'string' in data_type:
                sample_values.append("\"a\"")
            else:
                sample_values.append("\"\"")
        sample_values_str = ','.join(sample_values)

        contract_code = f'''
        // SPDX-License-Identifier: MIT
        pragma solidity 0.8.7;

        contract StructPackingExample {{
            struct CheapStruct {{
                {struct_vars_str}
            }}

            CheapStruct example;

            function test() public {{
                CheapStruct memory someStruct = CheapStruct(
                    {sample_values_str}
                );
                example = someStruct;
            }}
        }}
        '''
        # print(contract_code)
        file_name = '_'.join(combination) + '.sol'
        with open(f'test/{file_name}', 'w') as f:
            f.write(contract_code)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please provide a list of data types separated by commas')
        sys.exit(1)
    data_types = sys.argv[1].split(',')
    tightenit(data_types)
    forgeit()
    deletit(['test', 'out'])
