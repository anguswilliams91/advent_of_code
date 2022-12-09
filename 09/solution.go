package main

import (
	"aoc"
	"fmt"
	"image"
	"strings"
)

type rope struct {
	knots   []image.Point
	length  int
	visited map[image.Point]bool
}

type motion struct {
	direction string
	distance  int
}

func (r *rope) init(n int) {
	r.knots = []image.Point{}
	for i := 0; i < n; i++ {
		r.knots = append(r.knots, image.Point{0, 0})
	}
	r.length = n
	r.visited = make(map[image.Point]bool)
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func sign(x int) int {
	if x > 0 {
		return 1
	} else if x < 0 {
		return -1
	} else {
		return 0
	}
}

func unit(p image.Point) image.Point {
	return image.Point{sign(p.X), sign(p.Y)}
}

func pull(p image.Point, q image.Point) image.Point {
	if d := p.Sub(q); abs(d.X) > 1 || abs(d.Y) > 1 {
		return q.Add(unit(d))
	}
	return q
}

func (r *rope) move(m motion) {
	var d image.Point
	switch m.direction {
	case "U":
		d = image.Point{0, 1}
	case "D":
		d = image.Point{0, -1}
	case "L":
		d = image.Point{-1, 0}
	case "R":
		d = image.Point{1, 0}
	}
	for i := 1; i <= m.distance; i++ {
		r.knots[0] = r.knots[0].Add(d)
		for j := 1; j < r.length; j++ {
			r.knots[j] = pull(r.knots[j-1], r.knots[j])
		}
		r.visited[r.knots[r.length-1]] = true
	}
}

func parseInput(input string) []motion {
	ms := []motion{}
	for _, s := range strings.Split(input, "\n") {
		var m motion
		fmt.Sscanf(
			s,
			"%v %d",
			&m.direction,
			&m.distance,
		)
		ms = append(ms, m)
	}
	return ms
}

func solve(input string) aoc.Solution[int, int] {
	ms := parseInput(input)
	r2 := rope{}
	r10 := rope{}
	r2.init(2)
	r10.init(10)
	for _, m := range ms {
		r2.move(m)
		r10.move(m)
	}
	return aoc.Solution[int, int]{
		PartOne: len(r2.visited),
		PartTwo: len(r10.visited),
	}
}

func main() {
	puzzleInput := aoc.LoadInput("input.txt")
	timedSolve := aoc.Timer("Day nine", solve)
	timedSolve(puzzleInput)
}
