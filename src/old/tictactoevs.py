import lightbulb
import hikari
import miru
from constants import NORMAL_COLOR, SUCCESS_COLOR, FAILED_COLOR

# INIT
plugin = lightbulb.Plugin("tictactoevs")


# REQUIRED FUNCTIONS
def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)


class TicTacToeButton(miru.Button):
    def __init__(self, row: int, col: int):
        super().__init__(label="\u200b", style=hikari.ButtonStyle.SECONDARY, row=row)
        self.row: int = row
        self.col: int = col

    async def callback(self, ctx: miru.Context) -> None:
        if isinstance(self.view, TicTacToeView):
            view: TicTacToeView = self.view
            value: int = view.board[self.row][self.col]

            if value in (3, -3):
                return

            if view.currentPlayer == "X":
                self.style = hikari.ButtonStyle.DANGER
                self.label = "X"
                self.disabled = True
                view.board[self.row][self.col] = -1
                view.currentPlayer = "O"
                embed = hikari.Embed(title="TicTacToe - O's Turn", color = NORMAL_COLOR)
            else:
                self.style = hikari.ButtonStyle.SUCCESS
                self.label = "O"
                self.disabled = True
                view.board[self.row][self.col] = 1
                view.currentPlayer = "X"
                embed = hikari.Embed(title="TicTacToe - X's Turn", color = NORMAL_COLOR)

            gameState = view.checkGameState(view.board)

            if gameState is not None:
                if gameState == "X":
                    embed = hikari.Embed(title="TicTacToe - X Won!", color = SUCCESS_COLOR)
                elif gameState == "O":
                    embed = hikari.Embed(title="TicTacToe - O Won!", color = SUCCESS_COLOR)
                else:
                    embed = hikari.Embed(title="TicTacToe - Tie!", color = NORMAL_COLOR)

                for button in view.children:
                    assert isinstance(button, miru.Button)
                    button.disabled = True
                view.stop()

            await ctx.edit_response(embed=embed, components=view.build())
    

class TicTacToeView(miru.View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.currentPlayer: str = "X"

        # Create Boards
        self.boardButtons = [[0 for _ in range(3)] for _ in range(3)]
        self.board = [[0 for _ in range(3)] for _ in range(3)]

        # Create Board Buttons
        for y in range(3):
            for x in range(3):
                button = TicTacToeButton(y, x)
                self.boardButtons[y][x] = button
                self.add_item(button)


    # Runs on Timeout
    async def onTimeout(self) -> None:
        for item in self.children:
            assert isinstance(item, miru.Button)
            item.disabled = True

        embed = hikari.Embed(title="TicTacToe - Game Timed Out", color = FAILED_COLOR)
        assert self.message is not None
        await self.message.edit(embed=embed, components=self.build())


    # Finds All Possible Moves
    def getPossibleMoves(self, board):
        possibleMoves = []
        for row in range(3):
            for col in range(3):
                if board[row][col] == 0:
                    possibleMoves.append([row, col])
        return possibleMoves


    # Checks if Game Over
    def checkGameState(self, board):
        content = None
        if board[0][0] == board[0][1] == board[0][2] and board[0][0] != 0:
            content = board[0][0] 
        elif board[1][0] == board[1][1] == board[1][2] and board[1][0] != 0:
            content = board[1][0]
        elif board[2][0] == board[2][1] == board[2][2] and board[2][0] != 0:
            content = board[2][0]
        elif board[0][0] == board[1][0] == board[2][0] and board[0][0] != 0:
            content = board[0][0]
        elif board[0][1] == board[1][1] == board[2][1] and board[0][1] != 0:
            content = board[0][1]
        elif board[0][2] == board[1][2] == board[2][2] and board[0][2] != 0:
            content = board[0][2]
        elif board[0][0] == board[1][1] == board[2][2] and board[0][0] != 0:
            content = board[0][0]
        elif board[0][2] == board[1][1] == board[2][0] and board[0][2] != 0:
            content = board[2][0]

        if content == 1:
            return "O"
        elif content == -1:
            return "X"
        elif len(self.getPossibleMoves(board)) == 0:
            return "tie"


# COMMANDS
@plugin.command
@lightbulb.command("tictactoevs", "Starts a TicTacToe Game")
@lightbulb.implements(lightbulb.SlashCommand)
async def tictactoevs(ctx: lightbulb.Context) -> None:
    embed = hikari.Embed(title="TicTacToe - X's Turn", color = NORMAL_COLOR)
    view = TicTacToeView()
    proxy = await ctx.respond(embed=embed, components=view.build())
    await view.start(await proxy.message())


