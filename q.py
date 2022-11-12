def writing(type, result, amount):
    with open('operations.csv', 'a') as f:
        f.write(f'{type}, {result}, {amount}\n')