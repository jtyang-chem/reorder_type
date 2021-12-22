import numpy as np
import pandas as pd
import re
import io

def get_mass_str(lmp_file):
    with open(lmp_file, 'r') as f:
        fstr = f.read()

    # print(fstr)

    result = re.findall(r'Masses([\w\W]*)Atoms', fstr)
    if result:
       # result = result[0].split('\n')
        result = result[0]
    else:
        print("no string matched for mass_str")

    # print(result)
    return result

def reorder_type(lmp_file, order_dict):
    mass_str = get_mass_str(lmp_file)

def get_mass_df(lmp_file):
    mass_str = get_mass_str(lmp_file)
    result = pd.read_csv(io.StringIO(mass_str), sep="\s+", header = None, index_col = 0, skiprows = 1)
    return result

def reorder_mass_df(df, order_dict):
    # df = pd.read_csv(io.StringIO(mass_str), sep="\s+", header = None, index_col = 0, skiprows = 1)
    df.index = df[3].map(order_dict)
    df.sort_index(inplace= True)
    df.index.name = None
    return df

def reorder_mass_str(mass_str, order_dict):
    df = pd.read_csv(io.StringIO(mass_str), sep="\s+", header = None, index_col = 0, skiprows = 1)
    print(df)
    print(order_dict)
    df.index = df[3].map(order_dict)
    df.sort_index(inplace= True)
    print(df)

def get_pos_str(lmp_file):
    with open(lmp_file, 'r') as f:
        fstr = f.read()

    # print(fstr)

    result = re.findall(r'Atoms.*\n([\w\W]*)', fstr)
    if result:
        # result = result[0].split('\n')
        result = result[0]
    else:
        print("no string matched for mass_str")

    # print(result)
    return result
    
def get_pos_df(lmp_file):
    p_str = get_pos_str(lmp_file)
    result = pd.read_csv(io.StringIO(p_str), sep="\s+", header = None, index_col = 0, skiprows = 1)
    result.index.name = None
    return result

def reorder_pos_df(df, index_dict):
    result = df.copy()
    # print("reorder_pos_df")
    # print(df.head)
    result[1] = df[1].map(index_dict)
    result.index.name = None
    # result = result.sort_index(inplace= True)
    return result

def get_index_dict(lmp_file, order_dict):
    m_df = get_mass_df(lmp_file)
    new_index = m_df[3].map(order_dict)
    # print(new_index)
    result = dict(zip(m_df.index, new_index.to_list() ))
    # print(result)
    return result

def get_new_mass_str(lmp_file, order_dict):
    m_df = get_mass_df(lmp_file)
    new_m_df = reorder_mass_df(m_df, order_dict)
    # print(new_m_df.index)
    result = new_m_df.to_string(header = None)
    return result

def get_new_pos_str(lmp_file, order_dict):
    index_dict = get_index_dict(lmp_file, order_dict)
    pos_df = get_pos_df(lmp_file)
    new_pos_df = reorder_pos_df(pos_df, index_dict)
    result = new_pos_df.to_string(header = None)
    return result

def mk_reorder_lmp(lmp_file, order_dict, fout):
    new_mass_str = get_new_mass_str(lmp_file, order_dict)
    new_pos_str = get_new_pos_str(lmp_file, order_dict)
    with open(lmp_file, 'r') as f:
        old_fstr = f.read()

    print(new_pos_str[:200])
    new_fstr = re.sub('(?<=Masses\n\n).*(?=\nAtoms)', new_mass_str, old_fstr, flags = re.DOTALL)
    new_fstr = re.sub('(?<=Atoms # atomic\n\s\n).*', new_pos_str, new_fstr, flags = re.DOTALL)

    with open(fout, 'w') as f:
        f.write(new_fstr)

    print("new file completed!")

def test():
    order_dict= {"C":1, "H":2, "N":3, "O":4}
    lmp_file = "./old.lmp"
    # m_df = get_mass_df(lmp_file)
    # print(m_df)
    # # print(mass_str)
    # new_m_df = reorder_mass_df(m_df, order_dict)
    # print(new_m_df)

    # print("pos:")
    # index_dict = get_index_dict(lmp_file, order_dict)
    # pos_df = get_pos_df(lmp_file)
    # print(pos_df)
    # new_pos_df = reorder_pos_df(pos_df, index_dict)
    # print(new_pos_df)
    
    print("make new file:")
    fout = "new.lmp"
    mk_reorder_lmp(lmp_file, order_dict, fout)

    # pos_str = get_pos_str(lmp_file)
    # print(pos_str[-100:])

def test_re():
    # a = r''' Example
# This is a very annoying string
# that takes up multiple lines
# and h@s a// kind{s} of stupid symbols in it
# ok String'''
    with open("test.txt", 'r') as f:
        a= f.read()

    # a = re.sub('\nThis(.*)ok','',a, flags=re.DOTALL)
    a = re.sub('(?<=\nThis).*(?=ok)','',a, flags=re.DOTALL)

    print(a)


def test_str():
    order_dict= {"C":1, "H":2, "N":3, "O":4}
    lmp_file = "./old.lmp"
    mass_str = get_mass_str(lmp_file)
    reorder_mass_str(mass_str, order_dict)
    
def main():
    order_dict= {"C":1, "H":2, "N":3, "O":4}
    lmp_file = "./old.lmp"
    fout = "new.lmp"
    mk_reorder_lmp(lmp_file, order_dict, fout)

if __name__ == "__main__":
    main()
