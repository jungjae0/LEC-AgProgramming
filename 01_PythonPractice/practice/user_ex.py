import tkinter as tk
from tkinter import simpledialog
from rich import print

def py2m2(pyeong):
    return pyeong * 3.3

def simple_gui_input(text="값을 입력하시오"):
    return simpledialog.askstring(title='입력창', prompt=text)


def error_py2m2():

    while True:
        try:
            pyeong = float(simple_gui_input("평을 입력하세요: "))
            # pyeong = float(get_csv_value())
            break
        except ValueError:
            print("[bold red]숫자만 입력하세요[/bold red]")

    return print(f'[bold blue]{pyeong}평[/bold blue] => [bold magenta]{py2m2(pyeong):.2f}㎡[/bold magenta]')

def get_csv_value():

    with open('input.csv') as file_data:
        line = file_data.readline()
        return line

    return None

def main():
    error_py2m2()

if __name__ == '__main__':
    main()