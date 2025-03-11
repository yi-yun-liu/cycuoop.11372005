# Zodiac list corresponding to the 12 animals
zodiac = [
    "Monkey", "Rooster", "Dog", "Pig", "Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat"
]

def get_zodiac(year):
    # Calculate the zodiac sign based on the Chinese zodiac cycle, which repeats every 12 years
    return zodiac[(year - 4) % 12]

def main():
    # Get user input for year, month, and day
    year = int(input("Please enter the year: "))
    month = int(input("Please enter the month: "))
    day = int(input("Please enter the day: "))

    # Get the zodiac sign for the given year
    zodiac_sign = get_zodiac(year)
    
    # Output the result
    print(f"You entered the date: {year}-{month}-{day}")
    print(f"The zodiac sign for that year is: {zodiac_sign}")

# Run the main program
main()




