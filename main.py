import os
from dotenv import load_dotenv
from backend.crew import SmartTravelCrew


def main():
    load_dotenv()
    print("Welcome to Smart Travel Agent!")

    destination = input("Where do you want to go? ")
    origin      = input("Where are you departing from? ")
    duration    = int(input("How many days is your trip? "))

    crew   = SmartTravelCrew()
    result = crew.run(origin, destination, duration)

    print("\n--- Your Travel Plan ---")
    print(result)


if __name__ == "__main__":
    main()
