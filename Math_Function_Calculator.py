import math
from collections import Counter


# ---------- Calculation Functions ----------

def addition_calculator():
    """Add multiple numbers."""
    numbers = input("Enter numbers separated by spaces: ")
    nums = [float(x) for x in numbers.split()]
    print(f"Sum: {sum(nums)}")


def subtraction_calculator():
    """Subtract multiple numbers sequentially."""
    numbers = input("Enter numbers separated by spaces: ")
    nums = [float(x) for x in numbers.split()]
    total = nums[0]
    for n in nums[1:]:
        total -= n
    print(f"Difference: {total}")


def multiplication_calculator():
    """Multiply multiple numbers."""
    numbers = input("Enter numbers separated by spaces: ")
    nums = [float(x) for x in numbers.split()]
    total = 1
    for n in nums:
        total *= n
    print(f"Product: {total}")


def division_calculator():
    """Divide multiple numbers sequentially."""
    numbers = input("Enter numbers separated by spaces: ")
    nums = [float(x) for x in numbers.split()]
    total = nums[0]
    try:
        for n in nums[1:]:
            total /= n
        print(f"Quotient: {total}")
    except ZeroDivisionError:
        print("Error: Division by zero!")


def average_calculator():
    """Calculate the mean of numbers."""
    numbers = input("Enter numbers separated by spaces: ")
    nums = [float(x) for x in numbers.split()]
    print(f"Average: {sum(nums) / len(nums)}")


def percent_calculator():
    """Perform various percentage calculations."""
    print("1. a% of b")
    print("2. a is what % of b")
    print("3. Increase b by a%")
    print("4. Decrease b by a%")
    ch = input("Choice: ")
    if ch == "1":
        a = float(input("Percent: "))
        b = float(input("Number: "))
        print(f"Result: {(a / 100) * b}")
    elif ch == "2":
        a = float(input("Part: "))
        b = float(input("Whole: "))
        print(f"Result: {(a / b) * 100}%")
    elif ch == "3":
        a = float(input("Percent: "))
        b = float(input("Number: "))
        print(f"Result: {b * (1 + a / 100)}")
    elif ch == "4":
        a = float(input("Percent: "))
        b = float(input("Number: "))
        print(f"Result: {b * (1 - a / 100)}")


def exponent_calculator():
    """Calculate base raised to an exponent."""
    base = float(input("Base: "))
    exp = float(input("Exponent: "))
    print(f"{base}^{exp} = {base ** exp}")


def squareroot_calculator():
    """Calculate square root of a number."""
    number = float(input("Number: "))
    if number < 0:
        print("No real square root!")
    else:
        print(f"√{number} = {math.sqrt(number)}")


def logarithm_calculator():
    """Calculate logarithm with various bases."""
    n = float(input("Number: "))
    base = input("Base (10 for log, e for ln, or number): ").lower()
    if base == "10":
        print(f"log10({n}) = {math.log10(n)}")
    elif base == "e":
        print(f"ln({n}) = {math.log(n)}")
    else:
        base = float(base)
        print(f"log base {base} of {n} = {math.log(n, base)}")


def quadratic_solver():
    """Solve quadratic equation ax² + bx + c = 0."""
    a = float(input("a: "))
    b = float(input("b: "))
    c = float(input("c: "))
    d = b ** 2 - 4 * a * c
    if d < 0:
        print("No real solutions")
    elif d == 0:
        print(f"One solution: {-b / (2 * a)}")
    else:
        print(f"Solutions: {(-b + math.sqrt(d)) / (2 * a)} and {(-b - math.sqrt(d)) / (2 * a)}")


def factor_quadratic():
    """Factor quadratic expression."""
    print("Factor quadratic: ax² + bx + c")
    a = int(input("a: "))
    b = int(input("b: "))
    c = int(input("c: "))
    d = b ** 2 - 4 * a * c
    if d < 0:
        print("Cannot factor over real numbers")
        return
    sqrt_d = int(math.sqrt(d))
    if sqrt_d * sqrt_d != d:
        print("Cannot factor nicely over integers")
        return
    r1 = (-b + sqrt_d) // (2 * a)
    r2 = (-b - sqrt_d) // (2 * a)
    print(f"Factored form: {a}(x-{r1})(x-{r2})")


def system_of_equations():
    """Solve 2x2 system of linear equations."""
    print("Solve ax + by = c and dx + ey = f")
    a = float(input("a: "))
    b = float(input("b: "))
    c = float(input("c: "))
    d = float(input("d: "))
    e = float(input("e: "))
    f = float(input("f: "))
    det = a * e - b * d
    if det == 0:
        print("No unique solution")
    else:
        x = (c * e - b * f) / det
        y = (a * f - c * d) / det
        print(f"x = {x}, y = {y}")


def slope_intercept_solver():
    """Solve y = mx + b for x or y."""
    m = float(input("Slope m: "))
    b = float(input("Intercept b: "))
    choice = input("Solve for y or x? (y/x): ").lower()
    if choice == "y":
        x = float(input("x = "))
        print(f"y = {m * x + b}")
    elif choice == "x":
        y = float(input("y = "))
        if m == 0:
            print("No solution or infinite solutions")
        else:
            print(f"x = {(y - b) / m}")


def slope_2points():
    """Calculate slope between two points."""
    x1 = float(input("x1: "))
    y1 = float(input("y1: "))
    x2 = float(input("x2: "))
    y2 = float(input("y2: "))
    if x1 == x2:
        print("Undefined slope")
    else:
        print(f"Slope: {(y2 - y1) / (x2 - x1)}")


def area_calculator():
    """Calculate area of a rectangle."""
    l = float(input("Length: "))
    w = float(input("Width: "))
    print(f"Area: {l * w}")


def perimeter_calculator():
    """Calculate perimeter of a polygon."""
    numbers = input("Enter sides separated by spaces: ")
    nums = [float(x) for x in numbers.split()]
    print(f"Perimeter: {sum(nums)}")


def trianglearea_calculator():
    """Calculate triangle area using Heron's formula."""
    a = float(input("Side 1: "))
    b = float(input("Side 2: "))
    c = float(input("Side 3: "))
    s = (a + b + c) / 2
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    print(f"Triangle area: {area}")


def circlearea_calculator():
    """Calculate area of a circle."""
    radius = float(input("Radius: "))
    print(f"Circle area: {math.pi * radius ** 2}")


def circumference_calculator():
    """Calculate circumference of a circle."""
    r = float(input("Radius: "))
    print(f"Circumference: {2 * math.pi * r}")


def polygon_area_calculator():
    """Calculate area of a regular polygon."""
    n = int(input("Number of sides: "))
    s = float(input("Side length: "))
    if n < 3:
        print("Not a polygon")
        return
    area = (n * s ** 2) / (4 * math.tan(math.pi / n))
    print(f"Polygon area: {area}")


def surface_area_of_cube():
    """Calculate surface area of a cube."""
    a = float(input("Edge length of cube: "))
    surface_area = 6 * a ** 2
    print(f"Surface area of cube: {surface_area}")


def prism_surface_area():
    """Calculate surface area of a rectangular prism."""
    l = float(input("Length: "))
    w = float(input("Width: "))
    h = float(input("Height: "))
    print(f"Surface area: {2 * (l * w + w * h + h * l)}")


def cylinder_volume():
    """Calculate volume of a cylinder."""
    r = float(input("Radius: "))
    h = float(input("Height: "))
    print(f"Volume: {math.pi * r * r * h}")


def cone_volume():
    """Calculate volume of a cone."""
    r = float(input("Radius: "))
    h = float(input("Height: "))
    print(f"Volume: {(1 / 3) * math.pi * r * r * h}")


def sphere_volume_calculator():
    """Calculate volume of a sphere."""
    r = float(input("Radius: "))
    print(f"Sphere volume: {4 / 3 * math.pi * r ** 3}")


def distance_formula():
    """Calculate distance between two points."""
    x1 = float(input("x1: "))
    y1 = float(input("y1: "))
    x2 = float(input("x2: "))
    y2 = float(input("y2: "))
    print(f"Distance: {math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)}")


def pythagoras():
    """Calculate hypotenuse using Pythagorean theorem."""
    a = float(input("Side 1: "))
    b = float(input("Side 2: "))
    print(f"Hypotenuse: {math.sqrt(a ** 2 + b ** 2)}")


def angle_converter():
    """Convert between degrees and radians."""
    ch = input("1. Deg → Rad, 2. Rad → Deg: ")
    if ch == "1":
        deg = float(input("Degrees: "))
        print(f"Radians: {math.radians(deg)}")
    else:
        rad = float(input("Radians: "))
        print(f"Degrees: {math.degrees(rad)}")


def median_calculator():
    """Calculate median of a dataset."""
    numbers = input("Numbers separated by spaces: ")
    nums = sorted([float(x) for x in numbers.split()])
    n = len(nums)
    if n % 2 == 1:
        median = nums[n // 2]
    else:
        median = (nums[n // 2 - 1] + nums[n // 2]) / 2
    print(f"Median: {median}")


def mode_calculator():
    """Calculate mode(s) of a dataset."""
    numbers = input("Numbers separated by spaces: ")
    nums = [float(x) for x in numbers.split()]
    count = Counter(nums)
    max_count = max(count.values())
    modes = [k for k, v in count.items() if v == max_count]
    print(f"Mode(s): {modes}")


def range_calculator():
    """Calculate range of a dataset."""
    numbers = input("Numbers separated by spaces: ")
    nums = [float(x) for x in numbers.split()]
    print(f"Range: {max(nums) - min(nums)}")


def quartiles():
    """Calculate quartiles of a dataset."""
    nums = sorted([float(x) for x in input("Numbers: ").split()])
    n = len(nums)
    q2 = nums[n // 2] if n % 2 else (nums[n // 2] + nums[n // 2 - 1]) / 2
    mid = n // 2
    lower = nums[:mid]
    upper = nums[mid + 1:] if n % 2 else nums[mid:]

    def med(arr):
        n = len(arr)
        return arr[n // 2] if n % 2 else (arr[n // 2] + arr[n // 2 - 1]) / 2

    print(f"Q1: {med(lower)}")
    print(f"Q2 (median): {q2}")
    print(f"Q3: {med(upper)}")


def std_variance_calculator():
    """Calculate variance and standard deviation."""
    numbers = input("Numbers separated by spaces: ")
    nums = [float(x) for x in numbers.split()]
    mean = sum(nums) / len(nums)
    variance = sum((x - mean) ** 2 for x in nums) / len(nums)
    std = math.sqrt(variance)
    print(f"Variance: {variance}, Standard Deviation: {std}")


def prime_checker():
    """Check if a number is prime."""
    n = int(input("Number: "))
    if n < 2:
        print("Not prime")
        return
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            print("Not prime")
            return
    print("Prime")


def gcd_lcm():
    """Calculate GCD and LCM of two numbers."""
    a = int(input("Number 1: "))
    b = int(input("Number 2: "))
    gcd = math.gcd(a, b)
    lcm = abs(a * b) // gcd
    print(f"GCD: {gcd}, LCM: {lcm}")


def factorial_calculator():
    """Calculate factorial of a number."""
    n = int(input("Number: "))
    if n < 0:
        print("No factorial for negative numbers!")
    else:
        print(f"{n}! = {math.factorial(n)}")


def fibonacci_sequence():
    """Generate Fibonacci sequence."""
    n = int(input("Number of terms: "))
    seq = [0, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    print(seq[:n])


def roman_converter():
    """Convert decimal number to Roman numerals."""
    num = int(input("Number to convert to Roman: "))
    if num <= 0:
        print("Please enter a positive number")
        return
    original_num = num
    vals = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syms = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    res = ""
    for i, v in enumerate(vals):
        while num >= v:
            res += syms[i]
            num -= v
    print(f"{original_num} in Roman numerals: {res}")


def simplify_fraction():
    """Simplify a fraction to lowest terms."""
    num = int(input("Numerator: "))
    den = int(input("Denominator: "))
    g = math.gcd(num, den)
    print(f"Simplified: {num // g}/{den // g}")


def simplify_radical():
    """Simplify a square root radical."""
    n = int(input("Number: "))
    largest_sq = 1
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % (i * i) == 0:
            largest_sq = i * i
    outside = int(math.sqrt(largest_sq))
    inside = n // largest_sq
    print(f"Simplified: {outside}√{inside}")


def sequences():
    """Calculate arithmetic or geometric sequence."""
    print("1. Arithmetic\n2. Geometric")
    ch = input("Choice: ")
    if ch == "1":
        a = float(input("a1: "))
        d = float(input("d: "))
        n = int(input("n: "))
        print(f"nth term = {a + (n - 1) * d}")
        print(f"Sum = {n / 2 * (2 * a + (n - 1) * d)}")
    else:
        a = float(input("a1: "))
        r = float(input("r: "))
        n = int(input("n: "))
        print(f"nth term = {a * r ** (n - 1)}")
        print(f"Sum = {a * (1 - r ** n) / (1 - r)}")


def unit_converter():
    """Convert between common units."""
    print("1. Meters ↔ Feet")
    print("2. Celsius ↔ Fahrenheit")
    print("3. Kg ↔ Lb")
    ch = input("Choice: ")
    if ch == "1":
        m = float(input("Meters: "))
        print(f"Feet = {m * 3.28084}")
    elif ch == "2":
        c = float(input("Celsius: "))
        print(f"Fahrenheit = {c * 9 / 5 + 32}")
    elif ch == "3":
        kg = float(input("Kg: "))
        print(f"Lbs = {kg * 2.20462}")


def random_generator():
    """Generate random numbers."""
    import random
    print("1. Random integer")
    print("2. Random float 0-1")
    print("3. Roll dice")
    ch = input("Choice: ")
    if ch == "1":
        a = int(input("Min: "))
        b = int(input("Max: "))
        print(f"Result: {random.randint(a, b)}")
    elif ch == "2":
        print(f"Result: {random.random()}")
    else:
        sides = int(input("Dice sides: "))
        print(f"Result: {random.randint(1, sides)}")


def base_converter():
    """Convert between number bases."""
    print("1. Dec → Bin\n2. Bin → Dec\n3. Dec → Hex")
    ch = input("Choice: ")
    if ch == "1":
        n = int(input("Decimal: "))
        print(f"Binary: {bin(n)[2:]}")
    elif ch == "2":
        b = input("Binary: ")
        print(f"Decimal: {int(b, 2)}")
    else:
        n = int(input("Decimal: "))
        print(f"Hexadecimal: {hex(n)[2:].upper()}")


def determinant_2x2():
    """Calculate determinant of 2x2 matrix."""
    a = float(input("a: "))
    b = float(input("b: "))
    c = float(input("c: "))
    d = float(input("d: "))
    print(f"Determinant: {a * d - b * c}")


def determinant_3x3():
    """Calculate determinant of 3x3 matrix."""
    m = []
    print("Enter 3 rows of 3 numbers each:")
    for _ in range(3):
        m.append(list(map(float, input().split())))
    a, b, c = m[0]
    d, e, f = m[1]
    g, h, i = m[2]
    det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
    print(f"Determinant: {det}")


def volume_calculator():
    """Calculate volume of a rectangular prism."""
    l = float(input("Length: "))
    w = float(input("Width: "))
    h = float(input("Height: "))
    print(f"Volume: {l * w * h}")


def trapezoid_area():
    """Calculate area of a trapezoid."""
    a = float(input("Base 1: "))
    b = float(input("Base 2: "))
    h = float(input("Height: "))
    print(f"Area: {(a + b) / 2 * h}")


def parallelogram_area():
    """Calculate area of a parallelogram."""
    b = float(input("Base: "))
    h = float(input("Height: "))
    print(f"Area: {b * h}")


def ellipse_area():
    """Calculate area of an ellipse."""
    a = float(input("Semi-major radius: "))
    b = float(input("Semi-minor radius: "))
    print(f"Area: {math.pi * a * b}")


def trig_calculator():
    """Calculate trigonometric functions."""
    choice = input("Choose sin, cos, tan, arcsin, arccos, arctan: ").lower()
    if "arc" in choice:
        val = float(input("Value: "))
        if choice == "arcsin":
            print(f"arcsin({val}) = {math.degrees(math.asin(val))}°")
        elif choice == "arccos":
            print(f"arccos({val}) = {math.degrees(math.acos(val))}°")
        elif choice == "arctan":
            print(f"arctan({val}) = {math.degrees(math.atan(val))}°")
    else:
        val = float(input("Angle in degrees: "))
        rad = math.radians(val)
        if choice == "sin":
            print(f"sin({val}) = {math.sin(rad)}")
        elif choice == "cos":
            print(f"cos({val}) = {math.cos(rad)}")
        elif choice == "tan":
            print(f"tan({val}) = {math.tan(rad)}")
def expression_calculator():
    """Evaluate a mathematical expression."""
    expr = input("Enter expression: ")

    try:
        allowed = {
            "sqrt": math.sqrt,
            "pi": math.pi,
            "e": math.e,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "log10": math.log10
        }

        result = eval(expr, {"__builtins__": None}, allowed)
        print(f"{expr} = {result}")

    except Exception as e:
        print(f"Error: {e}")


# ---------- Search Function ----------

def search_calculators(calculators_dict, calculator_names):
    """Search for calculators by keyword."""
    keyword = input("\nEnter search keyword (or press Enter to see all): ").strip().lower()

    if not keyword:
        return None  # Show all

    matches = []
    for key, name in calculator_names.items():
        if keyword in name.lower():
            matches.append((key, name))

    if not matches:
        print(f"\nNo calculators found matching '{keyword}'")
        input("Press Enter to continue...")
        return "no_match"

    print(f"\n{'=' * 40}")
    print(f"   Search Results for '{keyword}'")
    print('=' * 40)
    for key, name in matches:
        print(f"{key}. {name}")
    print("\n0. Back to main menu")
    print('=' * 40)

    choice = input("\nEnter choice: ").strip()
    if choice == "0":
        return "back"
    elif choice in [k for k, _ in matches]:
        return choice
    else:
        print("Invalid choice")
        input("Press Enter to continue...")
        return "invalid"



# ---------- Main Menu ----------

def display_menu():
    """Display the main calculator menu."""
    print("\n" + "=" * 40)
    print("   CheatSheet Calculator")
    print("   Make Sure To Scroll Up To See Your Answer")
    print("   Type 'S' to Search | '0' to Exit")
    print("=" * 40)

    print("Arithmetic Operations:")
    print("1-Add, 2-Subtract, 3-Multiply, 4-Divide, 5-Average, 6-Percent, 52-Expression Calculator")
    print()
    print("Algebra:")
    print("7-Exponent, 8-Square Root, 9-Logarithm, 10-Quadratic, 11-Factor Quad")
    print("12-System 2x2, 13-Slope-Intercept, 14-Slope (2pts)")
    print()
    print("Geometry:")
    print("15-Rectangle Area, 16-Perimeter, 17-Triangle Area, 18-Circle Area")
    print("19-Circumference, 20-Polygon Area, 21-Cube SA, 22-Prism SA")
    print("23-Cylinder Vol, 24-Cone Vol, 25-Sphere Vol, 26-Distance, 27-Pythagoras, 28-Angle Conv")
    print()
    print("Statistics:")
    print("29-Median, 30-Mode, 31-Range, 32-Quartiles, 33-Std Dev/Variance")
    print()
    print("Number Theory:")
    print("34-Prime Check, 35-GCD/LCM, 36-Factorial, 37-Fibonacci, 38-Roman Numerals")
    print()
    print("Other:")
    print("39-Simplify Fraction, 40-Simplify Radical, 41-Sequences, 42-Unit Converter")
    print("43-Random Generator, 44-Base Converter, 45-Det 2x2, 46-Det 3x3")
    print("47-Volume (Prism), 48-Trapezoid, 49-Parallelogram, 50-Ellipse, 51-Trig")

    print("\n0. Exit")
    print("=" * 40)


def main():
    """Main program loop."""
    calculators = {
        "1": addition_calculator,
        "2": subtraction_calculator,
        "3": multiplication_calculator,
        "4": division_calculator,
        "5": average_calculator,
        "6": percent_calculator,
        "52": expression_calculator,
        "7": exponent_calculator,
        "8": squareroot_calculator,
        "9": logarithm_calculator,
        "10": quadratic_solver,
        "11": factor_quadratic,
        "12": system_of_equations,
        "13": slope_intercept_solver,
        "14": slope_2points,
        "15": area_calculator,
        "16": perimeter_calculator,
        "17": trianglearea_calculator,
        "18": circlearea_calculator,
        "19": circumference_calculator,
        "20": polygon_area_calculator,
        "21": surface_area_of_cube,
        "22": prism_surface_area,
        "23": cylinder_volume,
        "24": cone_volume,
        "25": sphere_volume_calculator,
        "26": distance_formula,
        "27": pythagoras,
        "28": angle_converter,
        "29": median_calculator,
        "30": mode_calculator,
        "31": range_calculator,
        "32": quartiles,
        "33": std_variance_calculator,
        "34": prime_checker,
        "35": gcd_lcm,
        "36": factorial_calculator,
        "37": fibonacci_sequence,
        "38": roman_converter,
        "39": simplify_fraction,
        "40": simplify_radical,
        "41": sequences,
        "42": unit_converter,
        "43": random_generator,
        "44": base_converter,
        "45": determinant_2x2,
        "46": determinant_3x3,
        "47": volume_calculator,
        "48": trapezoid_area,
        "49": parallelogram_area,
        "50": ellipse_area,
        "51": trig_calculator
    }

    calculator_names = {k: v.__name__.replace("_", " ").title() for k, v in calculators.items()}

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "0":
            print("Exiting program...")
            break

        if choice.lower() == "s":
            result = search_calculators(calculators, calculator_names)
            if result in (None, "back", "no_match", "invalid"):
                continue
            choice = result

        if choice in calculators:
            try:
                calculators[choice]()
            except Exception as e:
                print(f"An error occurred: {e}")
            input("\nPress Enter to return to menu...")
        else:
            print("Invalid choice, try again.")
            input("Press Enter...")


if __name__ == "__main__":
    main()