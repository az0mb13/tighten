def get_data_type_size(data_type):
    # Returns the size of a data type in bytes
    if data_type.startswith('uint'):
        return int(data_type[4:]) // 8
    elif data_type.startswith('int'):
        return int(data_type[3:]) // 8
    elif data_type.startswith('bytes'):
        return int(data_type[5:])
    elif data_type == 'address':
        return 20
    elif data_type == 'bool':
        return 1
    else:
        raise ValueError(f'Invalid data type: {data_type}')


def pack_variables(data_types):
    # Packs variables into storage slots
    slots = [[]]
    for data_type in data_types:
        size = get_data_type_size(data_type)
        if size > 32:
            raise ValueError(
                f'Data type {data_type} is too large to fit in a single storage slot')
        packed = False
        for slot in slots:
            if sum(get_data_type_size(var) for var in slot) + size <= 32:
                slot.append(data_type)
                packed = True
                break
        if not packed:
            slots.append([data_type])
    return slots


def print_packing_order(data_types):
    slots = pack_variables(data_types)
    for i, slot in enumerate(slots):
        print(f'Storage slot {i}:')
        for var in slot:
            print(f'  {var}')


data_types = ['uint256', 'bytes10', 'bytes20', 'bytes30',
              'bytes32', 'address', 'uint16', 'uint8']
print_packing_order(data_types)
