package main

import (
	"aoc"
	"image"
)

type rock []image.Point

type terrain struct {
	blocked   map[image.Point]bool
	maxHeight int
}

func parseInput(input string) []image.Point {
	jets := []image.Point{}
	for _, s := range []rune(input) {
		var j image.Point
		if s == '>' {
			j = image.Point{1, 0}
		} else {
			j = image.Point{-1, 0}
		}
		jets = append(jets, j)
	}
	return jets
}

func (r *rock) moveByJet(j image.Point, t terrain) {
	old := *r
	new := []image.Point{}
	for _, p := range old {
		n := p.Add(j)
		_, ok := t.blocked[n]
		if n.X > 6 || n.X < 0 || ok {
			return
		}
		new = append(new, n)
	}
	*r = new
}

func (r *rock) fall(t terrain) bool {
	old := *r
	new := []image.Point{}
	for _, p := range old {
		n := p.Add(image.Point{0, -1})
		if _, ok := t.blocked[n]; ok {
			return false
		}
		new = append(new, n)
	}
	*r = new
	return true
}

func initShape(shape string, height int) rock {
	var r rock
	switch shape {
	case "-":
		r = rock{
			{2, height},
			{3, height},
			{4, height},
			{5, height},
		}
	case "+":
		r = rock{
			{3, height + 2},
			{2, height + 1},
			{3, height + 1},
			{4, height + 1},
			{3, height},
		}
	case "⅃":
		r = rock{
			{4, height + 2},
			{4, height + 1},
			{2, height},
			{3, height},
			{4, height},
		}
	case "|":
		r = rock{
			{2, height + 3},
			{2, height + 2},
			{2, height + 1},
			{2, height},
		}
	case "□":
		r = rock{
			{2, height + 1},
			{3, height + 1},
			{2, height},
			{3, height},
		}
	}
	return r
}

type repeatedState struct {
	relativeHeights [7]int
	currentShape    int
	currentJet      int
}

type state struct {
	height      int
	rocksThrown int
}

func (t *terrain) getRelativeHeights() [7]int {
	heights := [7]int{0, 0, 0, 0, 0, 0, 0}
	for p, _ := range t.blocked {
		heights[p.X] = aoc.Max(heights[p.X], p.Y)
	}
	for i, v := range heights {
		heights[i] = t.maxHeight - v
	}
	return heights
}

func getHeightAfter(numRocks int, jets []image.Point) int {
	floor := map[image.Point]bool{}
	for i := 0; i < 7; i++ {
		floor[image.Point{i, 0}] = true
	}
	t := terrain{blocked: floor, maxHeight: 0}
	shapes := []string{"-", "+", "⅃", "|", "□"}
	currentJet := 0
	numJets := len(jets)
	currentShape := 0
	seen := map[repeatedState]state{}
	heights := []int{}
	for n := 0; n < numRocks; n++ {
		if n > 0 {
			cur := repeatedState{
				relativeHeights: t.getRelativeHeights(),
				currentShape:    currentShape,
				currentJet:      currentJet,
			}
			if prev, ok := seen[cur]; ok {
				period := n - prev.rocksThrown
				heightPerCycle := t.maxHeight - prev.height
				repeats, remainder := aoc.Divmod(numRocks-prev.rocksThrown, period)
				return heightPerCycle*repeats + heights[prev.rocksThrown+remainder-1]
			}
			seen[cur] = state{height: t.maxHeight, rocksThrown: n}
		}
		r := initShape(shapes[currentShape], t.maxHeight+4)
		falling := true
		for falling {
			r.moveByJet(jets[currentJet], t)
			currentJet = (currentJet + 1) % numJets
			falling = r.fall(t)
		}
		for _, p := range r {
			t.maxHeight = aoc.Max(t.maxHeight, p.Y)
			t.blocked[p] = true
		}
		currentShape = (currentShape + 1) % 5
		heights = append(heights, t.maxHeight)
	}
	return t.maxHeight
}

func solve(input string) aoc.Solution[int, int] {
	jets := parseInput(input)
	return aoc.Solution[int, int]{
		PartOne: getHeightAfter(2022, jets),
		PartTwo: getHeightAfter(1000000000000, jets),
	}
}

func main() {
	puzzleInput := aoc.LoadInput("input.txt")
	timedSolve := aoc.Timer("Day seventeen", solve)
	timedSolve(puzzleInput)
}
