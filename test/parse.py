import MyStack2
from icecream import ic

str_success = """
#include <stdio.h>

int main(void) {
	printf("Hello!")
	return 0;
}
"""

str_error = """
#include <stdio.h>

int main(void) {
	printf("Hello!"
	return 0;
}
"""


def match_symbols(str):
    open_symbols = "<({"
    stack = MyStack2.MyStack2(10)

    for c in str:
        if c in open_symbols:
            stack.push(c)
            ic(f"push {c} into stack")
            continue

        match c:
            case ">":
                val = stack.pop()
                ic(f"pop {val} from stack")
                if val != "<":
                    ic(f'{val} is not matched with "')
                    return "Error"
            case ")":
                val = stack.pop()
                ic(f"pop {val} from stack")
                if val != "(":
                    ic(f'{val} is not matched with "')
                    return "Error"
            case "}":
                val = stack.pop()
                ic(f"pop {val} from stack")
                if val != "{":
                    ic(f'{val} is not matched with "')
                    return "Error"
            case _:
                pass

    return "Success"


if __name__ == "__main__":
    print(match_symbols(str_success))
    print(match_symbols(str_error))
