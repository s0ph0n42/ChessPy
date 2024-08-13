import Game

CPUONLY = __import__('Globals').GameMode.CPUONLY
HUMANCPU = __import__('Globals').GameMode.HUMANCPU
HUMANONLY = __import__('Globals').GameMode.HUMANONLY

game = Game.Game(HUMANONLY)
#game = Game.Game(HUMANCPU)
#game = Game.Game(CPUONLY)

try:
    game.run()

    with open('LOG.txt', 'a') as log:
        log.write("\nSuccess: ")
        log.write(game.board.history[-1])

except FileNotFoundError as ex:
    for arg in ex.args:
        print(arg)

    print("Incorrect directory or missing files")
    exit(1)

except Exception as ex:
    with open('./LOG.txt', 'a') as log:
        log.write("\nFailure\n")

        for arg in ex.args:
            log.write(arg)

        log.write("\n")

        for fen in game.board.history:
            log.write(fen)
            log.write("\n")

        log.write("\n")
    exit(1)