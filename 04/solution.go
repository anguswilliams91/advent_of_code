package main

import (
	"aoc"
	"strconv"
	"strings"
)

type sectionAssignment struct {
	firstSection int
	lastSection  int
}

func checkOverlap(p *[2]sectionAssignment) bool {
	a, b := p[0], p[1]
	aFirstInB := b.firstSection <= a.firstSection && b.lastSection >= a.firstSection
	aLastInB := b.firstSection <= a.lastSection && b.lastSection >= a.lastSection
	aContainsB := a.firstSection <= b.firstSection && a.lastSection >= b.lastSection
	return aFirstInB || aLastInB || aContainsB
}

func checkFullyContains(p *[2]sectionAssignment) bool {
	a, b := p[0], p[1]
	aContainsB := a.firstSection <= b.firstSection && a.lastSection >= b.lastSection
	bContainsA := b.firstSection <= a.firstSection && b.lastSection >= a.lastSection
	return aContainsB || bContainsA
}

func parsePair(ps string) [2]sectionAssignment {
	var p [2]sectionAssignment
	for i, s := range strings.Split(ps, ",") {
		ns := strings.Split(s, "-")
		f, _ := strconv.Atoi(ns[0])
		l, _ := strconv.Atoi(ns[1])
		p[i] = sectionAssignment{firstSection: f, lastSection: l}
	}
	return p
}

func solve(input string) aoc.Solution[int, int] {
	partOne := 0
	partTwo := 0
	for _, ps := range strings.Split(input, "\n") {
		p := parsePair(ps)
		if checkFullyContains(&p) {
			partOne += 1
		}
		if checkOverlap(&p) {
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
