package main

import (
	"aoc"
	"image"
	"strings"
)

type heightMap struct {
	height map[image.Point]rune
	start  image.Point
	end    image.Point
}

type location struct {
	coords   image.Point
	distance int
}

type queue []location

func (q *queue) pop() location {
	head := (*q)[0]
	*q = (*q)[1:]
	return head
}

func (q *queue) push(p location) {
	*q = append(*q, p)
}

func newHeightMap() *heightMap {
	r := heightMap{}
	r.height = make(map[image.Point]rune)
	return &r
}

func parseInput(input string) *heightMap {
	hm := newHeightMap()
	for r, s := range strings.Split(input, "\n") {
		for c, v := range []rune(s) {
			p := image.Point{r, c}
			hm.height[p] = v
			if v == 'S' {
				hm.height[p] = 'a'
				hm.start = p
			} else if v == 'E' {
				hm.height[p] = 'z'
				hm.end = p
			}
		}
	}
	return hm
}

func findShortestRoute(hm *heightMap, fromAnywhere bool) int {
	var cond func(rune, rune) bool
	var finished func(location) bool
	var start image.Point
	if fromAnywhere {
		cond = func(h, h0 rune) bool { return h0-h <= 1 }
		finished = func(l location) bool { return hm.height[l.coords] == 'a' }
		start = hm.end
	} else {
		cond = func(h, h0 rune) bool { return h-h0 <= 1 }
		finished = func(l location) bool { return l.coords.Eq(hm.end) }
		start = hm.start
	}
	visited := make(map[image.Point]bool)
	q := queue{location{coords: start, distance: 0}}
	visited[start] = true
	for len(q) > 0 {
		p := q.pop()
		if finished(p) {
			return p.distance
		}
		for _, delta := range []image.Point{{-1, 0}, {1, 0}, {0, -1}, {0, 1}} {
			n := p.coords.Add(delta)
			if h, ok := hm.height[n]; ok {
				if cond(h, hm.height[p.coords]) && !visited[n] {
					visited[n] = true
					q.push(location{coords: n, distance: p.distance + 1})
				}
			}
		}
	}
	return -1
}

func solve(input string) aoc.Solution[int, int] {
	hm := parseInput(input)
	return aoc.Solution[int, int]{
		PartOne: findShortestRoute(hm, false),
		PartTwo: findShortestRoute(hm, true),
	}
}

func main() {
	puzzleInput := aoc.LoadInput("input.txt")
	timedSolve := aoc.Timer("Day twelve", solve)
	timedSolve(puzzleInput)
}
