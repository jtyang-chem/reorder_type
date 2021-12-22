# reorder_type
### Reorder description of atom types and correspond positons of lammps format file

1. Create a lmp data file from some format( e.g. .cif) file with `atomsk`
2. Set the new order with atom type and order number in dictionary of python
3. Set the path of your lammps file to be changed
4. run the python script

- this file use the third column(after the "#") of masses part as type info, if these info missed or the lammps file is not made by `atomsk`, it's your free to add the column by hand
