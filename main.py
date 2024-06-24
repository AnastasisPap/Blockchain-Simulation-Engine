from init_parser import get_args
from Logic.simulation import Simulation

def main():
    args = get_args()
    sim = Simulation(args)
    sim.start()


if __name__ == '__main__':
    main()