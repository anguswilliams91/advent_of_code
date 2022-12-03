package main

import (
	"aoc"
	"fmt"
	"strings"
)

func runeToPriority(r rune) int {
	if r >= 97 {
		// ASCII "a" has a decimal value of 97,
		// and a priority of 1.
		return int(r) - 96
	} else {
		// ASCII "A" has a decimal value of 65,
		// and a priority of 27.
		return int(r) - 38
	}
}

func getRepeatedItemPriority(items string) int {
	runes := []rune(items)
	n := len(runes)
	seen := make(map[rune]bool)
	priority := 0
	for i, r := range runes {
		if i < n/2 {
			seen[r] = true
		} else {
			if seen[r] {
				priority = runeToPriority(r)
				break
			}
		}
	}
	return priority
}

func getCommonItemPriority(elfGroup []string) int {
	inFirst := make(map[rune]bool)
	inFirstSecond := make(map[rune]bool)
	priority := 0
	for _, r := range []rune(elfGroup[0]) {
		inFirst[r] = true
	}
	for _, r := range []rune(elfGroup[1]) {
		if inFirst[r] {
			inFirstSecond[r] = true
		}
	}
	for _, r := range []rune(elfGroup[2]) {
		if inFirstSecond[r] {
			priority = runeToPriority(r)
			break
		}
	}
	return priority
}

func solve(input string) aoc.Solution[int, int] {
	partOne := 0
	partTwo := 0
	var elfGroup []string
	for i, backpack := range strings.Split(input, "\n") {
		partOne += getRepeatedItemPriority(backpack)
		elfGroup = append(elfGroup, backpack)
		if (i+1)%3 == 0 {
			partTwo += getCommonItemPriority(elfGroup)
			elfGroup = []string{}
		}
	}
	return aoc.Solution[int, int]{PartOne: partOne, PartTwo: partTwo}
}

func main() {
	defer aoc.Timer("Day 3")()
	input := aoc.LoadInput("input.txt")
	solution := solve(input)
	fmt.Println("Part 1: ", solution.PartOne)
	fmt.Println("Part 2: ", solution.PartTwo)
}
