package main

import (
	"aoc"
	"fmt"
	"strings"
)

type sectionAssignment struct {
	firstSection int
	lastSection  int
}

func rangesOverlap(p *[2]sectionAssignment) bool {
	a, b := p[0], p[1]
	return a.firstSection <= b.lastSection && b.firstSection <= a.lastSection
}

func oneContainsOther(p *[2]sectionAssignment) bool {
	a, b := p[0], p[1]
	aContainsB := a.firstSection <= b.firstSection && a.lastSection >= b.lastSection
	bContainsA := b.firstSection <= a.firstSection && b.lastSection >= a.lastSection
	return aContainsB || bContainsA
}

func parsePair(ps string) [2]sectionAssignment {
	var p [2]sectionAssignment
	fmt.Sscanf(
		ps,
		"%d-%d,%d-%d",
		&p[0].firstSection,
		&p[0].lastSection,
		&p[1].firstSection,
		&p[1].lastSection,
	)
	return p
}

func solve(input string) aoc.Solution[int, int] {
	partOne := 0
	partTwo := 0
	for _, ps := range strings.Split(input, "\n") {
		p := parsePair(ps)
		if oneContainsOther(&p) {
			partOne++
		}
		if rangesOverlap(&p) {
			partTwo++
		}
	}
	return aoc.Solution[int, int]{PartOne: partOne, PartTwo: partTwo}
}

func main() {
	puzzleInput := aoc.LoadInput("input.txt")
	timedSolve := aoc.Timer("Day four", solve)
	timedSolve(puzzleInput)
}
