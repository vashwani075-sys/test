print("Hello! today is friday")

n = int(input("What is your age? "))

# 1. Changed || to 'or', and added a colon at the end
if n > 111 or n < 1:
    # 3. Indented this line
    print("your age is not acceptable")
# 2. Added a colon at the end
else:
    # 3. Indented this line, and your f-string works perfectly here!
    print(f"next year your age will be {n + 1} years")
