from functions.get_file_content import get_file_content


result = get_file_content("calculator", "lorem.txt")
print("Result for 'lorem.txt' file:")
if len(result) <= 10000:
    print(f"Length of lorem.txt under 10000 characters")
else:
    print(f"Error: Length of lorem.txt exceeds 10000 characters")

if '[...File "' in result:
    print(f"Truncation message present")
else:
    print("Error: truncation message missing")

result = get_file_content("calculator", "main.py")
print("Result for 'main.py' file:")
print(result)

result = get_file_content("calculator", "pkg/calculator.py")
print("Result for 'pkg/calculator.py' file:")
print(result)

result = get_file_content("calculator", "/bin/cat")
print("Result for '/bin/cat' file:")
print(result)

result = get_file_content("calculator", "pkg/does_not_exist.py")
print("Result for 'pkg/does_not_exist.py' file:")
print(result)