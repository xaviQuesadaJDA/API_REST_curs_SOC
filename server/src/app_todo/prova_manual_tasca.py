#!/usr/bin/python3

import tasca

def main():
    tasca_1 = tasca.Tasca(None, "Tasca nova 1")    # On None és persistencia i "Tasca nova 1" el nou títol.
    tasca_2 = tasca.Tasca(None, "Tasca nova 2")
    tasca_3 = tasca.Tasca(None, "Tasca nova 3")
    tasca_feta = tasca.Tasca(None, "Tasca nova 3", True)

    print(f"{tasca_1.titol}, {tasca_1.done}")
    print(f"{tasca_2.titol}, {tasca_2.done}")
    print(tasca_3)
    print(tasca_feta)

if __name__ == "__main__":
    main()