"""
animal_v11_async.py
Simple async simulation of animals 'doing' activities.
"""
import asyncio
import random

class Animal:
    def __init__(self, name):
        self.name = name
        self.energy = 100

    async def do_activity(self, activity, duration):
        print(f"{self.name} starts {activity}")
        # pretend activity drains energy over time
        for _ in range(duration):
            await asyncio.sleep(0.01)
            self.energy -= random.randint(0, 5)
        print(f"{self.name} ends {activity} (energy={self.energy})")
        return self.energy

async def main():
    a = Animal("Flash")
    await asyncio.gather(a.do_activity("play", 3), a.do_activity("nap", 2))

if __name__ == "__main__":
    asyncio.run(main())
