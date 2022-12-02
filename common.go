package aoc

import (
	"io/ioutil"
	"log"
	"time"
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

// Creates a timer to check how long solutions take.
func Timer(name string) func() {
    start := time.Now()
    return func() {
        fmt.Printf("%s Took %v\n", name, time.Since(start))
    }
}