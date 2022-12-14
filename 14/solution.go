package main

import (
	"aoc"
	"fmt"
	"image"
	"strings"
)

type cave struct {
	blocked map[image.Point]bool
	bottom  int
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func sign(x int) int {
	if x < 0 {
		return -1
	} else if x > 0 {
		return 1
	}
	return 0
}

func max(a int, b int) int {
	if a > b {
		return a
	} else if a < b {
		return b
	}
	return a
}

func unit(p image.Point) image.Point {
	return image.Point{sign(p.X), sign(p.Y)}
}

func parseInput(input string) cave {
	blocked := map[image.Point]bool{}
	bottom := 0
	for _, l := range strings.Split(input, "\n") {
		q := image.Point{}
		for i, s := range strings.Split(l, "->") {
			var r, c int
			fmt.Sscanf(s, "%d,%d", &r, &c)
			p := image.Point{r, c}
			blocked[p] = true
			if i != 0 {
				d := p.Sub(q)
				for i := 1; i < max(abs(d.X), abs(d.Y)); i++ {
					blocked[q.Add(unit(d).Mul(i))] = true
				}
			}
			q = p
			if p.Y > bottom {
				bottom = p.Y
			}
		}
	}
	return cave{blocked: blocked, bottom: bottom}
}

func fillWithSand(input string, hasFloor bool) int {
	c := parseInput(input)
	n := 0
	notFilled := true
	canFallTo := func(p image.Point) bool {
		_, ok := c.blocked[p]
		return !ok && (!hasFloor || p.Y < c.bottom+2)
	}
	for notFilled {
		p := image.Point{500, 0}
		for true {
			if !hasFloor && p.Y > c.bottom {
				notFilled = false
				break
			}
			if canFallTo(p.Add(image.Point{0, 1})) {
				p = p.Add(image.Point{0, 1})
			} else if canFallTo(p.Add(image.Point{-1, 1})) {
				p = p.Add(image.Point{-1, 1})
			} else if canFallTo(p.Add(image.Point{1, 1})) {
				p = p.Add(image.Point{1, 1})
			} else {
				c.blocked[p] = true
				n += 1
				if hasFloor && p.Eq(image.Point{500, 0}) {
					notFilled = false
				}
				break
			}
		}
	}
	return n
}

func solve(input string) aoc.Solution[int, int] {
	return aoc.Solution[int, int]{
		PartOne: fillWithSand(input, false),
		PartTwo: fillWithSand(input, true),
	}
}

func main() {
	puzzleInput := aoc.LoadInput("input.txt")
	timedSolve := aoc.Timer("Day twelve", solve)
	timedSolve(puzzleInput)
}
