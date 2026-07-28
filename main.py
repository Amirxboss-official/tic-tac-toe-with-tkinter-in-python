import tkinter as tk
from tkinter import messagebox as msg

def get_board_size():
    while True:
        try:
            val = input("Enter your board size (3 for 3x3, 4 for 4x4, etc): ")
            size = int(val)

            if size < 3:
                print("min number: 3")
                continue

            return size

        except ValueError:
            print("please Enter numberr only")

class Main:
    def __init__(self, size):
        self.size = size
        self.root = tk.Tk()
        self.root.title(f"{size}x{size} Board")
        self.cell_px = 100
        self.w = self.size * self.cell_px
        self.h = self.size * self.cell_px + 50
        self.current_player = "x"
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        pos_x = (screen_width // 2) - (self.w // 2)
        pos_y = (screen_height // 2) - (self.h // 2)
        self.root.geometry(
            f"{self.w}x{self.h}+{pos_x}+{pos_y}"
        )

        self.root.resizable(False, False)
        self.buttons = [
            [None for _ in range(size)]
            for _ in range(size)
        ]

        self.l1 = tk.Label(
            self.root,
            text="turn: x",
            font=("Arial", 24)
        )

        self.l1.grid(
            row=self.size,
            column=0,
            columnspan=self.size
        )

        self.build_board()
        self.root.mainloop()


    def build_board(self):
        for r in range(self.size):
            for c in range(self.size):
                btn = tk.Button(
                    self.root,
                    width=5,
                    height=2,
                    font=("Arial", 24),
                    command=lambda row=r, col=c:
                    self.on_click(row, col)
                )

                btn.grid(
                    row=r,
                    column=c,
                    sticky="nsew"
                )

                self.buttons[r][c] = btn


        for i in range(self.size):
            self.root.grid_rowconfigure(
                i,
                weight=1
            )

            self.root.grid_columnconfigure(
                i,
                weight=1
            )

    def on_click(self, r, c):
        if self.buttons[r][c]["text"] != "":
            msg.showwarning(
                "False Clicked",
                "Please click on empty home!"
            )
            return

        self.buttons[r][c].config(
            text=self.current_player
        )

        if self.check(r, c, self.current_player):
            return

        if self.current_player == "x":
            self.current_player = "o"
        else:
            self.current_player = "x"

        self.l(self.current_player)

    def check(self, r, c, player):     
        if all(
            self.buttons[r][col]["text"] == player
            for col in range(self.size)
        ):
            self.win(player)
            return True

        if all(
            self.buttons[row][c]["text"] == player
            for row in range(self.size)
        ):
            self.win(player)
            return True

        if all(
            self.buttons[i][i]["text"] == player
            for i in range(self.size)
        ):
            self.win(player)
            return True

        if all(
            self.buttons[i][self.size - 1 - i]["text"] == player
            for i in range(self.size)
        ):
            self.win(player)
            return True

        if all(
            self.buttons[row][col]["text"] != ""
            for row in range(self.size)
            for col in range(self.size)
        ):
            answer = msg.askyesno(
                "Draw",
                "Draw!!\nRestart?"
            )

            if answer:
                self.reset()
            else:
                self.root.destroy()

            return True
        return False

    def win(self, player):
        answer = msg.askyesno(
            "Winner",
            f"Player {player} wins!\nRestart?"
        )
        if answer:
            self.reset()
        else:
            self.root.destroy()

    def reset(self):
        for r in range(self.size):
            for c in range(self.size):
                self.buttons[r][c].config(text="")

        self.current_player = "x"
        self.l("x")

    def l(self, t):
        self.l1.config(
            text=f"turn: {t}"
        )

if __name__ == "__main__":
    board_size = get_board_size()
    my_board = Main(board_size)
