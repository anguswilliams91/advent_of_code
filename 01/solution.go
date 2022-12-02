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

// Finds the sum of highest calory totals held by elves.
func solve(puzzleInput string) aoc.Solution[int, int] {
	topThreeCalories := []int{0, 0, 0}
	for _, elfItems := range strings.Split(puzzleInput, "\n\n") {
		totalCalories := getElfCalories(elfItems)
		indexToUpdate := -1
		for i, calories := range topThreeCalories {
			if totalCalories > calories {
				indexToUpdate = i
			} else {
				break
			}
		}
		if indexToUpdate != -1 {
			topThreeCalories[indexToUpdate] = totalCalories
		}
	}
	return aoc.Solution[int, int]{
		PartOne: topThreeCalories[2],
		PartTwo: topThreeCalories[0] + topThreeCalories[1] + topThreeCalories[2],
	}
}

func main() {
	puzzleInput := aoc.LoadInput("input.txt")
	s := solve(puzzleInput)
	fmt.Println("Part one: ", s.PartOne)
	fmt.Println("Part two: ", s.PartTwo)
}
