package main

import (
	"aoc"
	"strings"
)

func part1Score(op string, me string) int {
	score := 0
	if me == "X" {
		score += 1
		if op == "A" {
			score += 3
		} else if op == "C" {
			score += 6
		}
	} else if me == "Y" {
		score += 2
		if op == "A" {
			score += 6
		} else if op == "B" {
			score += 3
		}
	} else {
		score += 3
		if op == "B" {
			score += 6
		} else if op == "C" {
			score += 3
		}
	}
	return score
}

func part2Score(op string, outcome string) int {
	score := 0
	if outcome == "X" {
		if op == "A" {
			score += 3
		} else if op == "B" {
			score += 1
		} else {
			score += 2
		}
	} else if outcome == "Y" {
		score += 3
		if op == "A" {
			score += 1
		} else if op == "B" {
			score += 2
		} else {
			score += 3
		}
	} else {
		score += 6
		if op == "A" {
			score += 2
		} else if op == "B" {
			score += 3
		} else {
			score += 1
		}
	}
	return score
}

func solve(input string) aoc.Solution[int, int] {
	games := strings.Split(input, "\n")
	partOne := 0
	partTwo := 0
	for _, game := range games {
		moves := strings.Split(game, " ")
		op, meOrOutcome := moves[0], moves[1]
		partOne += part1Score(op, meOrOutcome)
		partTwo += part2Score(op, meOrOutcome)
	}
	return aoc.Solution[int, int]{PartOne: partOne, PartTwo: partTwo}
}

func main() {
	puzzleInput := aoc.LoadInput("input.txt")
	timedSolve := aoc.Timer("Day two", solve)
	timedSolve(puzzleInput)
}
