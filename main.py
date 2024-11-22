#!/usr/bin/python
import sys
from lark import Lark, Transformer, v_args

grammar = """
    start: (comment | declaration | table)*

    comment: "%{" /[^%]+/ "%}"
    
    declaration: "const" NAME "=" value
    value: NUMBER | table

    table: "table([" (entry ("," entry)*)? "])"
    entry: NAME "=" value

    NAME: /[a-zA-Z][_a-zA-Z0-9]*/
    NUMBER: /d+/
    
    %import common.WS
    %ignore WS
"""


class ConfigTransformer(Transformer):
    def start(self, items):
        return 'n'.join(str(item) for item in items if item)

    def comment(self, items):
        return ''

    def declaration(self, items):
        return f"const {items[1]} = {items[3]}"

    def table(self, items):
        entries = ',n  '.join(str(item) for item in items[1:-1])
        return f"table([n  {entries}n])"

    def entry(self, items):
        return f"{items[0]} = {items[2]}"

    def value(self, items):
        return str(items[0])

    def NAME(self, token):
        return token.value

    def NUMBER(self, token):
        return token.value


def main():
    if len(sys.argv) != 2:
        print("Использование: python script.py <путь к файлу TOML>")
        sys.exit(1)
    file_path = sys.argv[1]
    with open(file_path, 'r') as file:
        content = file.read()
    parser = Lark(grammar, parser='lalr', transformer=ConfigTransformer(), start='start')
    try:
        output = parser.parse(content)
        print(output)
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
