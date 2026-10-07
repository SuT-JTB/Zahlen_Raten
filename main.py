from random import randint
num = randint(1, 100)
print(num)


if __name__ == "__main__":

	guess = int(input("Gebe eine Zahl an: "))
	try_counter = 0
	while guess != num:
		if guess <= num:
			print("Zu klein")
		elif guess >= num:
			print("Zu groß")
		guess = int(input("Neue Zahl: "))
		try_counter += 1

	if guess == num:
		print("Korrekt!")
		print(f"Versuche: {try_counter}")
		
		