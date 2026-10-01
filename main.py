import random
num = int(random.random())
print(num)


if __name__ == "__main__":

	guess = int(input("Gebe eine Zahl an: "))
	try_counter = 0
	while guess != num:
		if guess <= num:
			print("zu klein")
		elif guess >= num:
			print("zu groß")
		guess = int(input("Neue Zahl: "))
		try_counter += 1

	if guess == num:
		print("Korrekt!")
		print(f"Versuche: {try_counter}")
		