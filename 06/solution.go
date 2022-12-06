package main

import (
	"aoc"
	"fmt"
	"log"
)

func findStart(input string, length int) (int, error) {
	rs := []rune(input)
	seen := make(map[rune]int)
	for j, r := range rs {
		seen[r]++
		if j > length-1 {
			first := rs[j-length]
			seen[first]--
			if seen[first] == 0 {
				delete(seen, first)
			}
		}
		if len(seen) == length {
			return j + 1, nil
		}
	}
	return -1, fmt.Errorf("Didn't find a start-of-(packet|message) marker.")
}

func solve(input string) aoc.Solution[int, int] {
	firstPacket, err := findStart(input, 4)
	if err != nil {
		log.Fatal(err)
	}
	firstMessage, err := findStart(input, 14)
	if err != nil {
		log.Fatal(err)
	}
	return aoc.Solution[int, int]{PartOne: firstPacket, PartTwo: firstMessage}
}

func main() {
	puzzleInput := aoc.LoadInput("input.txt")
	timedSolve := aoc.Timer("Day six", solve)
	timedSolve(puzzleInput)
}
