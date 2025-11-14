"""
animal_v12_cli.py
A tiny CLI to interact with animals.
"""
import argparse

class Animal:
    def __init__(self, name):
        self.name = name
        self.energy = 100

    def status(self):
        return f"{self.name}: energy={self.energy}"

def main():
    parser = argparse.ArgumentParser(description="Simple animal CLI")
    parser.add_argument("--name", required=True)
    parser.add_argument("--action", choices=["status","sleep"], default="status")
    args = parser.parse_args()
    a = Animal(args.name)
    if args.action == "sleep":
        a.energy = 100
        print("slept")
    else:
        print(a.status())

if __name__ == "__main__":
    main()
