// Solution to day 1.
package main

import (
	"aoc"
	"strconv"
	"strings"
)

type topThree [3]int

// Gets the total calories of the items held by an elf.
func getElfCalories(elfItems string) int {
	totalCalories := 0
	for _, itemCaloriesString := range strings.Split(elfItems, "\n") {
		itemCalories, _ := strconv.Atoi(itemCaloriesString)
		totalCalories += itemCalories
	}
	return totalCalories
}

// Inserts a calorie count into the top three.
func (t *topThree) update(calories int) {
	if calories > t[0] {
		if calories <= t[1] {
			t[0] = calories
		} else if calories <= t[2] {
			t[0] = t[1]
			t[1] = calories
		} else {
			t[0] = t[1]
			t[1] = t[2]
			t[2] = calories
		}
	}
}

// Finds the sum of highest calory totals held by elves.
func solve(puzzleInput string) aoc.Solution[int, int] {
	t := topThree{0, 0, 0}
	for _, elfItems := range strings.Split(puzzleInput, "\n\n") {
		calories := getElfCalories(elfItems)
		t.update(calories)
	}
	return aoc.Solution[int, int]{
		PartOne: t[2],
		PartTwo: t[0] + t[1] + t[2],
	}
}

func main() {
	puzzleInput := aoc.LoadInput("input.txt")
	timedSolve := aoc.Timer("Day one", solve)
	timedSolve(puzzleInput)
}
