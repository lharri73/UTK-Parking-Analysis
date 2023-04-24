import os

from utparking.lib.behavior_model import Runner

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")


def main():
    runner = Runner(DATA_DIR, time_scale=1 / 0.01)
    runner.setup_run()
    runner.run()


if __name__ == "__main__":
    main()
