import lightbulb
import hikari
import miru
import math
from constants import NORMAL_COLOR, SUCCESS_COLOR, FAILED_COLOR

# INIT
plugin = lightbulb.Plugin("tictactoe")


# REQUIRED FUNCTIONS
def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

@plugin.listener(hikari.StartedEvent)
async def started_event(event):
    miru.install(plugin.app)

class SelectVersion(miru.View):
    def __init__(self, channel, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.channel: hikari.GuildChannel = channel

    @miru.button(emoji="🤖", style=hikari.ButtonStyle.SUCCESS)
    async def ai(self, select: miru.Button, ctx: miru.Context) -> None:
        embed = hikari.Embed(title="-=-=-=- TicTacToe -=-=-=-", description="It's Your Turn", color = NORMAL_COLOR)
        view = TicTacToeViewAI()
        proxy = await plugin.app.rest.create_message(self.channel, embed=embed, components=view.build())
        await view.start(proxy)

    @miru.button(emoji="⚔️", style=hikari.ButtonStyle.SUCCESS)
    async def vs(self, button: miru.Button, ctx: miru.Context) -> None:
        embed = hikari.Embed(title="-=-=-=- TicTacToe -=-=-=-", description="It's Your Turn", color = NORMAL_COLOR)
        view = TicTacToeViewVS()
        proxy = await plugin.app.rest.create_message(self.channel, embed=embed, components=view.build())
        await view.start(proxy)


# AI
class TicTacToeButtonAI(miru.Button):
    def __init__(self, row: int, col: int):
        super().__init__(label="\u200b", style=hikari.ButtonStyle.SECONDARY, row=row)
        self.row: int = row
        self.col: int = col

    async def callback(self, ctx: miru.Context) -> None:
        if isinstance(self.view, TicTacToeViewAI):
            view: TicTacToeViewAI = self.view
            value: int = view.board[self.row][self.col]

            if value in (3, -3):
                return

            if view.currentPlayer == "player":
                self.style = hikari.ButtonStyle.DANGER
                self.label = "X"
                self.disabled = True
                view.board[self.row][self.col] = -1
                view.currentPlayer = "bot"
                embed = hikari.Embed(title="-=-=-=- TicTacToe -=-=-=-", description="Bot Thinking...", color = NORMAL_COLOR)

            gameState = view.checkGameState(view.board)

            if gameState is not None:
                if gameState == "player":
                    embed = hikari.Embed(title="-=-=-=- TicTacToe -=-=-=-", description="You Won!", color = SUCCESS_COLOR)
                elif gameState == "bot":
                    embed = hikari.Embed(title="-=-=-=- TicTacToe -=-=-=-", description="Bot Won!", color = FAILED_COLOR)
                else:
                    embed = hikari.Embed(title="-=-=-=- TicTacToe -=-=-=-", description="Tie!", color = NORMAL_COLOR)

                for button in view.children:
                    assert isinstance(button, miru.Button)
                    button.disabled = True
                view.stop()

            await ctx.edit_response(embed=embed, components=view.build())

            if view.currentPlayer == "bot" and gameState == None:
                await view.botTurn(view.board)
                gameState = view.checkGameState(view.board)
                if gameState is not None:
                    if gameState == "player":
                        embed = hikari.Embed(title="-=-=-=- TicTacToe -=-=-=-", description="You Won!", color = SUCCESS_COLOR)
                    elif gameState == "bot":
                        embed = hikari.Embed(title="-=-=-=- TicTacToe -=-=-=-", description="Bot Won!", color = FAILED_COLOR)
                    else:
                        embed = hikari.Embed(title="-=-=-=- TicTacToe -=-=-=-", description="Tie!", color = NORMAL_COLOR)

                    for button in view.children:
                        assert isinstance(button, miru.Button)
                        button.disabled = True
                    view.stop()

                else:
                    embed = hikari.Embed(title="-=-=-=- TicTacToe -=-=-=-", description="It's Your Turn", color = NORMAL_COLOR)

            await ctx.edit_response(embed=embed, components=view.build())
    

class TicTacToeViewAI(miru.View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.currentPlayer: str = "player"

        # Create Boards
        self.boardButtons = [[0 for _ in range(3)] for _ in range(3)]
        self.board = [[0 for _ in range(3)] for _ in range(3)]

        # Create Board Buttons
        for y in range(3):
            for x in range(3):
                button = TicTacToeButtonAI(y, x)
                self.boardButtons[y][x] = button
                self.add_item(button)


    # Runs on Timeout
    async def onTimeout(self) -> None:
        for item in self.children:
            assert isinstance(item, miru.Button)
            item.disabled = True

        embed = hikari.Embed(title="-=-=-=- TicTacToe -=-=-=-", description="Game Timed Out", color = FAILED_COLOR)
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
            return "bot"
        elif content == -1:
            return "player"
        elif len(self.getPossibleMoves(board)) == 0:
            return "tie"



    def minimax(self, isMaxTurn, depth, board):

        # Check if Game Over
        state = self.checkGameState(board)
        if state == "tie":
            return 0
        elif state == "player":
            return -10+depth
        elif state == "bot":
            return 10-depth

        # Get New Possible Moves
        possibleMoves = self.getPossibleMoves(board)
        scores = []

        # Iterate Through Possible Moves
        for move in possibleMoves:

            # Test Move
            board[move[0]][move[1]] = 1 if isMaxTurn else -1

            # Run Minimax on New Move
            scores.append(self.minimax(not isMaxTurn, depth+1, board))

            # Undo Test Move
            board[move[0]][move[1]] = 0

            # If Bot Turn and Score = 1: Break
            # If Not Bot Turn and Score = -1: Break
            if (isMaxTurn and max(scores) == 10) or (not isMaxTurn and min(scores) == -10):
                break

        # If Bot Turn, Return Max Score
        # If Player Turn, Return Min Score
        return max(scores) if isMaxTurn else min(scores)
    


    async def botTurn(self, board):
        # Get List of Possible Moves
        possibleMoves = self.getPossibleMoves(board)

        # Define Vars
        bestScore = -math.inf
        bestMove = None

        # Iterate Through Possible Moves
        for move in possibleMoves:

            # Set Test Move
            board[move[0]][move[1]] = 1

            # Run Minimax on Move and Get Score
            score = self.minimax(False, 1, board)

            # Undo Test Move
            board[move[0]][move[1]] = 0

            # If Score > bestScore, Update Vars
            if (score > bestScore):
                bestScore = score
                bestMove = move

        # Update Buttons and Board with Best Move
        self.boardButtons[bestMove[0]][bestMove[1]].label = "O"
        self.boardButtons[bestMove[0]][bestMove[1]].style = hikari.ButtonStyle.SUCCESS
        self.boardButtons[bestMove[0]][bestMove[1]].disabled = True 
        self.board[bestMove[0]][bestMove[1]] = 1
        self.currentPlayer = "player"


# VS
class TicTacToeButtonVS(miru.Button):
    def __init__(self, row: int, col: int):
        super().__init__(label="\u200b", style=hikari.ButtonStyle.SECONDARY, row=row)
        self.row: int = row
        self.col: int = col

    async def callback(self, ctx: miru.Context) -> None:
        if isinstance(self.view, TicTacToeViewVS):
            view: TicTacToeViewVS = self.view
            value: int = view.board[self.row][self.col]

            if value in (3, -3):
                return

            if view.currentPlayer == "X":
                self.style = hikari.ButtonStyle.DANGER
                self.label = "X"
                self.disabled = True
                view.board[self.row][self.col] = -1
                view.currentPlayer = "O"
                embed = hikari.Embed(title="-=-=-=- TicTacToe -=-=-=-", description="O's Turn", color = NORMAL_COLOR)
            else:
                self.style = hikari.ButtonStyle.SUCCESS
                self.label = "O"
                self.disabled = True
                view.board[self.row][self.col] = 1
                view.currentPlayer = "X"
                embed = hikari.Embed(title="-=-=-=- TicTacToe -=-=-=-", description="X's Turn", color = NORMAL_COLOR)

            gameState = view.checkGameState(view.board)

            if gameState is not None:
                if gameState == "X":
                    embed = hikari.Embed(title="-=-=-=- TicTacToe -=-=-=-", description="X Won!", color = SUCCESS_COLOR)
                elif gameState == "O":
                    embed = hikari.Embed(title="-=-=-=- TicTacToe -=-=-=-", description="O Won!", color = SUCCESS_COLOR)
                else:
                    embed = hikari.Embed(title="-=-=-=- TicTacToe -=-=-=-", description="Tie!", color = NORMAL_COLOR)

                for button in view.children:
                    assert isinstance(button, miru.Button)
                    button.disabled = True
                view.stop()

            await ctx.edit_response(embed=embed, components=view.build())
    

class TicTacToeViewVS(miru.View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.currentPlayer: str = "X"

        # Create Boards
        self.boardButtons = [[0 for _ in range(3)] for _ in range(3)]
        self.board = [[0 for _ in range(3)] for _ in range(3)]

        # Create Board Buttons
        for y in range(3):
            for x in range(3):
                button = TicTacToeButtonVS(y, x)
                self.boardButtons[y][x] = button
                self.add_item(button)


    # Runs on Timeout
    async def onTimeout(self) -> None:
        for item in self.children:
            assert isinstance(item, miru.Button)
            item.disabled = True

        embed = hikari.Embed(title="-=-=-=- TicTacToe -=-=-=-", description="Game Timed Out", color = FAILED_COLOR)
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
@lightbulb.command("tictactoe", "Play TicTacToe!")
@lightbulb.implements(lightbulb.SlashCommand)
async def tictactoe(ctx: lightbulb.Context) -> None:
    embed = hikari.Embed(title="-=-=-=- TicTacToe -=-=-=-", description="🤖 -> Robot vs Player \n ⚔️ -> Player vs Player", color = NORMAL_COLOR)
    view = SelectVersion(ctx.channel_id)
    resp = await ctx.respond(embed=embed, components=view)
    await view.start(await resp.message())
    await view.wait()
    await resp.delete()
