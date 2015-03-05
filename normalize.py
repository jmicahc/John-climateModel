import numpy as np
from collections import OrderedDict

def csvLine(f, items):
    if items==[]: return
    for item in items[:-1]:
        f.write(str(item) + ",")
    f.write(str(items[-1]) + "\n")

if __name__ == '__main__':

    f = list(open('climatedata_sealevel.csv', 'r'))
    colnames = f[0].replace('\n','').split(',')
    
    #Dictionary to contain processed raw data.
    data = OrderedDict()
    
    #Dictionary to contain normalized data.
    normalized = OrderedDict()

    #List of tuples containing column names and indices defining columns to run analysis on.
    cols = [(i, item) for i, item in enumerate(colnames)]# if item in ['Time','Sea Level','Red', 'CO2',] ]
    print cols, colnames
    for line in f[1:]:
        items = line[:-2].replace('No data', 'None').replace('No dat', 'None').split(',')

        for i,name in cols:
            if name not in data:
                data[name] = [float(items[i])] if items[i] != 'None' else ['None']
            else:
                data[name].append(float(items[i]) if items[i] != 'None' else 'None')
        for c in data:
            if c != 'Time':
                t = [v for v in data[c] if v != 'None']
                std = np.std([v for v in data[c] if v != 'None'])
                mean = np.mean([v for v in data[c] if v != 'None'])

                normalized[c] = []
                for v in data[c]:
                    normalized[c] += [(v - mean) / std] if v != 'None' else ['None']
            else:
                normalized[c] = data[c]

    fout = open('differences.csv', 'w')
    fout.write(",".join(colnames) + '\n')

    if not len(normalized.values()) == 0:
        for row in range(1, max([len(l) for l in normalized.values()])):
            items = []
            for col in data:
                if normalized[col][row] != 'None' and normalized[col][row-1] != 'None':
                    if col != 'Time':
                        v = abs(normalized[col][row] - normalized[col][row-1])
                    else:
                        v = normalized[col][row]
                    items.append(v)
                else:
                    items.append('None')
            csvLine(fout, items)
