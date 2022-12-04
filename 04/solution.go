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
	var s1, s2, f1, f2 int
	fmt.Sscanf(ps, "%d-%d,%d-%d", &s1, &f1, &s2, &f2)
	var p [2]sectionAssignment
	p[0] = sectionAssignment{firstSection: s1, lastSection: f1}
	p[1] = sectionAssignment{firstSection: s2, lastSection: f2}
	return p
}

func solve(input string) aoc.Solution[int, int] {
	partOne := 0
	partTwo := 0
	for _, ps := range strings.Split(input, "\n") {
		p := parsePair(ps)
		if oneContainsOther(&p) {
			partOne += 1
		}
		if rangesOverlap(&p) {
			partTwo += 1
		}
	}
	return aoc.Solution[int, int]{PartOne: partOne, PartTwo: partTwo}
}

func main() {
	puzzleInput := aoc.LoadInput("input.txt")
	timedSolve := aoc.Timer("Day four", solve)
	timedSolve(puzzleInput)
}
