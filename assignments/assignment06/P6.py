# How to use the script
# python3 P6.py -f input.txt

from z3 import *
import argparse


def test_equal_outputs(ina_val, m, inb_val, n):
    #asserting input
    ina, inb = Ints('ina inb')
    COND_1 = And(ina == ina_val, inb == inb_val)

    # power
    outa0_0 = Int('outa0_0')
    COND_2 = outa0_0 == ina
    outa = outa0_0
    for i in range(m):
        x = Int('outa' + str(i))
        COND_2 = And(COND_2, x == outa * ina)
        outa = x

    # power_new
    outb0_0 = Int('outb0_0')
    COND_3 = outb0_0 == inb
    outb = outb0_0
    for i in range(n):
        x = Int('outb' + str(i))
        COND_3 = And(COND_3, x == outb * outb)
        outb = x

    Assumptions = And(COND_1, COND_2, COND_3)

    IMP = Implies(Assumptions, outa == outb)

    s = Solver()
    s.add(Not(IMP))

    # prints unsat which means that the two functions output same results.
    res = str(s.check())
    print(res)
    return str(s.check()) == "unsat"


def main():
    # getting file_path
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('-f',
                           '--file',
                           action='store',
                           type=str,
                           required=True)
    args = my_parser.parse_args()
    input_file_path = args.file

    # reading input
    with open(input_file_path, newline='') as input_file:
        file_content = input_file.read().splitlines()

        if len(file_content) < 4:
            print('Invalid input file')
            exit()

        res = test_equal_outputs(int(file_content[0]), int(file_content[1]),
                                 int(file_content[2]), int(file_content[3]))

        if res:
            print("Outputs are equal.")
        else:
            print("Outputs are not equal.")


main()
