import os

from shutil import copyfile as Copy
from PIL import Image


def Crop(Input, Height, Width):
    if not os.path.isdir("PlayersSprites"):
        os.mkdir("PlayersSprites")
    if not os.path.isdir("PlayersSprites/" + Input):
        os.mkdir("PlayersSprites/" + Input)
    if not os.path.isdir("PlayersSprites/" + Input + "/Origin"):
        os.mkdir("PlayersSprites/" + Input + "/Origin")
    Im = Image.open("Skeleton/" + Input + '.png')
    ImWidth, ImHeight = Im.size
    k = 1
    area = (0, 0, 64, 64)
    for i in range(0, ImHeight, Height):
        for j in range(0, ImWidth, Width):
            Tile = (j, i, j + ImWidth, i + ImHeight)
            NewImage = Im.crop(Tile)
            NewImage = NewImage.crop(area)
            NewImage.save("PlayersSprites/" + Input + "/Origin/" + Input + "-" + str(k) + ".png", "PNG")
            k += 1

    Copy("Skeleton/" + Input + ".png", "PlayersSprites/" + Input + "/Origin/" + Input + "-base.png")


def SaveStatic(Input):
    if not os.path.isdir("PlayersSprites/" + Input + "/Animations"):
        os.mkdir("PlayersSprites/" + Input + "/Animations")
    PathIn = "PlayersSprites/" + Input + "/Origin/" + Input
    PathOut = "PlayersSprites/" + Input + "/Animations/"
    Copy(PathIn + "-2.png", PathOut + "Down.png")
    Copy(PathIn + "-5.png", PathOut + "Left.png")
    Copy(PathIn + "-8.png", PathOut + "Right.png")
    Copy(PathIn + "-11.png", PathOut + "Up.png")


def SaveAnimations(Input):
    Frames = []
    PathIn = "PlayersSprites/" + Input + "/Origin/" + Input
    PathOut = "PlayersSprites/" + Input + "/Animations/"

    # SAVE DOWN
    ImageOne = Image.open(PathIn + "-1.png")
    ImageTwo = Image.open(PathIn + "-2.png")
    ImageThree = Image.open(PathIn + "-3.png")
    Frames.append(ImageTwo)
    Frames.append(ImageOne)
    Frames.append(ImageTwo)
    Frames.append(ImageThree)
    Frames[0].save(
        PathOut + "Down.gif",
        save_all = True,
        append_images = Frames[1:],
        optimize = True,
        duration = 150,
        loop = 0,
        disposal = 2
    )
    ImageOne.close()
    ImageTwo.close()
    ImageThree.close()
    Frames = []

    # SAVE LEFT
    ImageOne = Image.open(PathIn + "-4.png")
    ImageTwo = Image.open(PathIn + "-5.png")
    ImageThree = Image.open(PathIn + "-6.png")
    Frames.append(ImageTwo)
    Frames.append(ImageOne)
    Frames.append(ImageTwo)
    Frames.append(ImageThree)
    Frames[0].save(
        PathOut + "Left.gif",
        save_all=True,
        append_images=Frames[1:],
        optimize=True,
        duration=150,
        loop=0,
        disposal=2
    )
    ImageOne.close()
    ImageTwo.close()
    ImageThree.close()
    Frames = []

    # SAVE RIGHT
    ImageOne = Image.open(PathIn + "-7.png")
    ImageTwo = Image.open(PathIn + "-8.png")
    ImageThree = Image.open(PathIn + "-9.png")
    Frames.append(ImageTwo)
    Frames.append(ImageOne)
    Frames.append(ImageTwo)
    Frames.append(ImageThree)
    Frames[0].save(
        PathOut + "Right.gif",
        save_all=True,
        append_images=Frames[1:],
        optimize=True,
        duration=150,
        loop=0,
        disposal=2
    )
    ImageOne.close()
    ImageTwo.close()
    ImageThree.close()
    Frames = []

    # SAVE Up
    ImageOne = Image.open(PathIn + "-10.png")
    ImageTwo = Image.open(PathIn + "-11.png")
    ImageThree = Image.open(PathIn + "-12.png")
    Frames.append(ImageTwo)
    Frames.append(ImageOne)
    Frames.append(ImageTwo)
    Frames.append(ImageThree)
    Frames[0].save(
        PathOut + "Up.gif",
        save_all=True,
        append_images=Frames[1:],
        optimize=True,
        duration=150,
        loop=0,
        disposal=2
    )
    ImageOne.close()
    ImageTwo.close()
    ImageThree.close()


def main():
    Input = "Player4"
    Crop(Input, 64, 64)
    SaveStatic(Input)
    SaveAnimations(Input)


main()
