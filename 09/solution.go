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
	visited map[int]map[image.Point]bool
}

type motion struct {
	direction string
	distance  int
}

func (r *rope) init(n int) {
	r.knots = []image.Point{}
	r.visited = make(map[int]map[image.Point]bool)
	for i := 0; i < n; i++ {
		r.knots = append(r.knots, image.Point{0, 0})
		if i == 1 || i == n-1 {
			r.visited[i] = make(map[image.Point]bool)
		}
	}
	r.length = n
}

func unit(p image.Point) image.Point {
	return image.Point{aoc.Sign(p.X), aoc.Sign(p.Y)}
}

func pull(p image.Point, q image.Point) image.Point {
	if d := p.Sub(q); aoc.Abs(d.X) > 1 || aoc.Abs(d.Y) > 1 {
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
			p := pull(r.knots[j-1], r.knots[j])
			r.knots[j] = p
			if j == 1 || j == r.length-1 {
				r.visited[j][p] = true
			}
		}
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
	r := rope{}
	r.init(10)
	for _, m := range ms {
		r.move(m)
	}
	return aoc.Solution[int, int]{
		PartOne: len(r.visited[1]),
		PartTwo: len(r.visited[r.length-1]),
	}
}

func main() {
	puzzleInput := aoc.LoadInput("input.txt")
	timedSolve := aoc.Timer("Day nine", solve)
	timedSolve(puzzleInput)
}
