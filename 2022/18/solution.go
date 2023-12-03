package main

import (
	"aoc"
	"fmt"
	"strings"
)

type point struct {
	X int
	Y int
	Z int
}

type droplet map[point]struct{}

func parseInput(input string) droplet {
	d := droplet{}
	for _, s := range strings.Split(input, "\n") {
		var k point
		fmt.Sscanf(s, "%d,%d,%d", &k.X, &k.Y, &k.Z)
		d[k] = struct{}{}
	}
	return d
}

func (p *point) getNeighbours() []point {
	return []point{
		{p.X + 1, p.Y, p.Z},
		{p.X - 1, p.Y, p.Z},
		{p.X, p.Y + 1, p.Z},
		{p.X, p.Y - 1, p.Z},
		{p.X, p.Y, p.Z + 1},
		{p.X, p.Y, p.Z - 1},
	}
}

func (dp *droplet) getSurfaceArea() int {
	d := *dp
	surfaceArea := 0
	for p := range d {
		for _, n := range p.getNeighbours() {
			if _, ok := d[n]; !ok {
				surfaceArea++
			}
		}
	}
	return surfaceArea
}

type boundingBox struct {
	minX, minY, minZ, maxX, maxY, maxZ int
}

func (dp *droplet) getBoundingBox() boundingBox {
	d := *dp
	minX, maxX := 10000, -10000
	minY, maxY := 10000, -10000
	minZ, maxZ := 10000, -10000
	for p := range d {
		minX = aoc.Min(minX, p.X)
		minY = aoc.Min(minY, p.Y)
		minZ = aoc.Min(minZ, p.Z)
		maxX = aoc.Max(maxX, p.X)
		maxY = aoc.Max(maxY, p.Y)
		maxZ = aoc.Max(maxZ, p.Z)
	}
	return boundingBox{minX - 1, minY - 1, minZ - 1, maxX + 1, maxY + 1, maxZ + 1}
}

func (bb *boundingBox) contains(p point) bool {
	xOk := (p.X >= bb.minX) && (p.X <= bb.maxX)
	yOk := (p.Y >= bb.minY) && (p.Y <= bb.maxY)
	zOk := (p.Z >= bb.minZ) && (p.Z <= bb.maxZ)
	return xOk && yOk && zOk
}

func (dp *droplet) getOutsideSurfaceArea() int {
	d := *dp
	bb := dp.getBoundingBox()
	area := 0
	q := aoc.Queue[point]{}
	q.Push(point{bb.maxX, bb.maxY, bb.maxZ})
	seen := map[point]struct{}{}
	for len(q) > 0 {
		p := q.Pop()
		for _, n := range p.getNeighbours() {
			_, onDroplet := d[n]
			if _, visited := seen[n]; bb.contains(n) && !onDroplet && !visited {
				seen[n] = struct{}{}
				q.Push(n)
			}
			if onDroplet {
				area++
			}
		}
	}
	return area
}

func solve(input string) aoc.Solution[int, int] {
	d := parseInput(input)
	return aoc.Solution[int, int]{
		PartOne: d.getSurfaceArea(),
		PartTwo: d.getOutsideSurfaceArea(),
	}
}

func main() {
	puzzleInput := aoc.LoadInput("input.txt")
	timedSolve := aoc.Timer("Day eighteen", solve)
	timedSolve(puzzleInput)
}
