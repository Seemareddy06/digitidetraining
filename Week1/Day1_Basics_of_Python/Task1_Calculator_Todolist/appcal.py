def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b): return "Cannot divide by zero!" if b == 0 else a / b
def floor_division(a, b): return "Cannot divide by zero!" if b == 0 else a // b
def modulus(a, b): return "Cannot divide by zero!" if b == 0 else a % b

def calculator():
    print("Select Operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Floor Division")
    print("6. Modulus")

    choice = input("Enter choice (1-6): ")

    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
    except ValueError:
        print("Invalid input! Please enter numbers only.")
        return

    if choice == '1':
        print("Result:", add(num1, num2))
    elif choice == '2':
        print("Result:", subtract(num1, num2))
    elif choice == '3':
        print("Result:", multiply(num1, num2))
    elif choice == '4':
        print("Result:", divide(num1, num2))
    elif choice == '5':
        print("Result:", floor_division(num1, num2))
    elif choice == '6':
        print("Result:", modulus(num1, num2))
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    calculator()
