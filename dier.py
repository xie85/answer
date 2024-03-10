def check_brackets(s):
    stack = []
    mismatches = []  # 存储不匹配的括号位置和类型 ('?' 或 'x')
    for i, char in enumerate(s):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if stack:
                stack.pop()
            else:
                mismatches.append((i, '?'))
    # 遍历完毕后，栈中剩余的都是未匹配的左括号
    for i in stack:
        mismatches.append((i, 'x'))
    
    # 构造输出字符串，包括原始字符和在不匹配括号下面标记的字符
    result = list(s)
    for i, mark in mismatches:
        result.insert(i + 1 + result[:i+1].count('\n'), mark)  # 考虑到插入导致的索引偏移和已经插入的'\n'
    return ''.join(result)

# 测试用例
test_cases = [
    "bge)))))))))",
    "((IIII)))))",
    "()()()()(uuu",
    "))))UUUU((()"
]

for test in test_cases:
    print(check_brackets(test))
