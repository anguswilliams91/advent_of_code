package aoc

import (
	"io/ioutil"
	"log"
)

type Solution[T, U any] struct {
	PartOne T
	PartTwo U
}

// Loads a puzzle's input from a path p into a string.
func LoadInput(p string) string {
	input, err := ioutil.ReadFile("input.txt")
	if err != nil {
		log.Fatal("Couldn't load puzzle input.")
	}
	return string(input)
}
