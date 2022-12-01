// Solution to day 1.
package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

type solution struct {
	partOne int
	partTwo int
}

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
func solve(puzzleInput string) solution {
	topThreeCalories := []int{0, 0, 0}
	for _, elfItems := range strings.Split(puzzleInput, "\n\n") {
		totalCalories := getElfCalories(elfItems)
		indexToUpdate := -1
		for i, calories := range topThreeCalories {
			if totalCalories > calories {
				indexToUpdate = i
			}
		}
		if indexToUpdate != -1 {
			topThreeCalories[indexToUpdate] = totalCalories
		}
	}
	return solution{
		partOne: topThreeCalories[2],
		partTwo: topThreeCalories[0] + topThreeCalories[1] + topThreeCalories[2],
	}
}

func main() {
	puzzleInput, _ := ioutil.ReadFile("input.txt")
	s := solve(string(puzzleInput))
	fmt.Println("Part one: ", s.partOne)
	fmt.Println("Part two: ", s.partTwo)
}
