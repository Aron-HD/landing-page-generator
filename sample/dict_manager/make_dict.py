import json
import pandas as pd
from yapf.yapflib.yapf_api import FormatFile


def main():

    awards_dict = create_dict("awards")
    for a in awards_dict.keys():                # instantiate categories dict for each award
        awards_dict[a]['categories'] = dict()

    categories_dict = create_dict("categories")
    for c in categories_dict.keys():            
        award = categories_dict[c]['award']
        # consolidate special awards to own dict for iteration in template
        categories_dict[c]['special_awards'] = dict()
        special_awards = categories_dict[c]['special_awards']
        # drop empty special awards (pop these values?)
        for k, v in zip(
            [v for k, v in categories_dict[c].items() if v and 'spec_award' in k], 
            [v for k, v in categories_dict[c].items() if v and 'spec_bio' in k]
        ):
            special_awards.update({k: v})
        # add special awards
        categories_dict[c].update(special_awards)
        # add categories to respective award
        awards_dict[award]['categories'].update({c: categories_dict[c]}) 
           
    write_file(file='dictionary.py', content=awards_dict)


def create_dict(name):

    data = pd.read_csv(f'csv/{name}_meta.csv')
    items = data[f'{name}'].to_list()
    data.set_index(name, inplace=True)
    data.fillna('', inplace=True)
    # return records in a dict
    dictionary = {}
    for i in items:
        records = data.loc[[i]].to_dict('index')
        dictionary.update(records)
    return dictionary


def write_file(file, content):
    # delete dictionary when not needed
    with open(f'../{file}', 'w') as f:
        print(content, file=f)
    FormatFile(f'../{file}', in_place=True)
    print('wrote: ', file)
    # change extension name and write the file to JSON
    file = file.replace('.py', '.json')
    # jsonify dictionary and write to file
    with open (f'../../data/{file}', 'w') as jf:
        json.dump(content, jf)
    print('wrote: ', file)


if __name__ == '__main__':
    main()
