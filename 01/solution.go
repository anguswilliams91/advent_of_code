// Solution to day 1.
package main

import (
	"aoc"
	"fmt"
	"strconv"
	"strings"
)

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
func insertCalories(calories int, topThree []int) []int {
	if calories > topThree[0] {
		if calories <= topThree[1] {
			topThree[0] = calories
		} else if calories <= topThree[2] {
			topThree[0] = topThree[1]
			topThree[1] = calories
		} else {
			topThree[0] = topThree[1]
			topThree[1] = topThree[2]
			topThree[2] = calories
		}
	}
	return topThree
}

// Finds the sum of highest calory totals held by elves.
func solve(puzzleInput string) aoc.Solution[int, int] {
	topThree := []int{0, 0, 0}
	for _, elfItems := range strings.Split(puzzleInput, "\n\n") {
		calories := getElfCalories(elfItems)
		topThree = insertCalories(calories, topThree)
	}
	return aoc.Solution[int, int]{
		PartOne: topThree[2],
		PartTwo: topThree[0] + topThree[1] + topThree[2],
	}
}

func main() {
	puzzleInput := aoc.LoadInput("input.txt")
	s := solve(puzzleInput)
	fmt.Println("Part one: ", s.PartOne)
	fmt.Println("Part two: ", s.PartTwo)
}
