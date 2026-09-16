def generate_table(data: list, units=None, highlights=[]) -> str:
    """
    generates markdown table from 2d list
    first row is header
    number of columns will be defined by number of headers

    highlights are indices of cells to highlight in bold 

    format:
    [(row, column)]

    *row 0 will be row 1 in data
    """
    num_columns = len(data[0])
    table = ''

    # generate header
    table += '| ' + ' | '.join(data[0]) + ' |\n'
    # line
    table +=  '| ' + ' | '.join([':--:'] * num_columns) + ' |\n'
    # actual data
    markdown_rows = []
    for row_index, row in enumerate(data[1:]):
        formatted_row = []

        if units:
            row_iterator = zip(row, units)
        else:
            row_iterator = zip(row, [''] * num_columns)

        for column_index, (cell, unit) in enumerate(row_iterator):
            if (row_index, column_index) in highlights:
                highlight = '**'
            else:
                highlight = ''

            if type(cell) == str:
                formatted_row += [highlight + cell + unit + highlight]
            elif type(cell) == float:
                formatted_row += [highlight + f'{cell:.2f}' + unit + highlight]
            else:
                formatted_row += [highlight + str(cell) + unit + highlight]
        
        markdown_rows += ['| ' + ' | '.join(formatted_row) + ' |']

    table += '\n'.join(markdown_rows)
    
    return table

def get_best_indices(data, evaluators=[]):
    """
    evaluators are used to check which value in the column is the "best"
    list of funcs like argmax
    or any custom one
    it'll receive a list of values and return the index of best one
    put None if column doesn't need to be evaluated
    """
    bests = []
    num_columns = len(data[0])

    columns = [[row[column_index] 
                for row in data[1:]] 
                for column_index in range(num_columns)]

    for column_index, (column, evaluator) in enumerate(zip(columns, evaluators)):
        if evaluator == None:
            continue
        bests += [(evaluator(column), column_index)]

    return bests


# run test: python -m markdown
if __name__ == '__main__':
    import numpy as np

    data = [
        ['strategy', 'mean 10 year return', 'aaa'], 
        ['buy and hold', 160.6, 89.6], 
        ['dca', 100.6, 120.34], 
        ['test', 100.6, 20.34]
    ]

    units = ['', '%', '%']

    highlights = get_best_indices(
        data, 
        evaluators=[None, np.argmax, np.argmin])

    table = generate_table(
        data, 
        units=units, 
        highlights=highlights)

    print(table)