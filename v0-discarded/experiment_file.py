import re
user_input = "seek 0"

match = re.search(r"^seek (\d+)", user_input)
if match:
    number = int(match.group(1))
    print("seeking...", number)


