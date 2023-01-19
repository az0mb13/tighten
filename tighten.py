import sys
import itertools
import os
import subprocess
import re
import shutil


def forgeit():
    try:
        output = subprocess.check_output(['forge', 'test', '--gas-report'])
        output_str = output.decode("utf-8")

        gasit(output_str)
    except subprocess.CalledProcessError as e:
        print("Error: ", e)


def deletit(directories):
    for directory in directories:
        for root, dirs, files in os.walk(directory):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))


def gasit(parsed_str):

    gas_values = re.findall(r'\(gas: (\d+)\)', parsed_str)
    file_names = re.findall(r'Running 1 test for test/(.+)\.sol:', parsed_str)
    data = zip(file_names, gas_values)
    # Convert the gas values from strings to integers
    data = [(file_name, int(gas)) for file_name, gas in data]
    # Find the minimum gas value
    min_gas = min(data, key=lambda x: x[1])

    print("Struct order: ", min_gas[0])
    print("Gas: ", min_gas[1])


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
