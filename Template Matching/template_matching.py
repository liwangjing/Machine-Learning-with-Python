import numpy as np
import argparse
import imutils
import cv2
import show_image as helper


def matching():
    puzzle = cv2.imread("res\puzzle_small.jpg")
    waldo = cv2.imread("res\waldo.jpg")
    helper.show_image("puzzle", puzzle)
    helper.show_image("waldo", waldo)
    (waldoHeight, waldoWidth) = waldo.shape[:2]
    print "type", waldo.shape[:2]

    # matchTemplate():
    # puzzle: image that contains our target
    # waldo: our target
    # cv2.TM_CCOEFF: matching mode, compute the correlation coefficient
    result = cv2.matchTemplate(puzzle, waldo, cv2.TM_CCOEFF)
    (_, _, minLoc, maxLoc) = cv2.minMaxLoc(result)
    print "minLoc", minLoc
    print "maxLoc", maxLoc

    #grab the bounding box of waldo and extract him from the puzzle image
    # topLeft = maxLoc
    topLeft = minLoc
    bottomRight = (topLeft[0] + waldoWidth, topLeft[1] + waldoHeight)
    roi = puzzle[topLeft[1]:bottomRight[1], topLeft[0]:bottomRight[0]]

    # construct a darkened transparent 'layer' to darked everything in the puzzle
    mask = np.zeros(puzzle.shape, dtype= "uint8")
    puzzle = cv2.addWeighted(puzzle, 0.25, mask, 0.75, 0)

    # put the original waldo back to the puzzle, so waldo is brighter
    puzzle[topLeft[1]:bottomRight[1], topLeft[0]:bottomRight[0]] = roi

    # show final image
    helper.show_image('final', puzzle)


def main():
    matching()


if __name__ == '__main__':
    main()
