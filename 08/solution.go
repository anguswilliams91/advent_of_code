package main

import (
	"aoc"
	"strings"
)

type treeLine []int
type treePatch []treeLine
type treeCoord struct {
	row int
	col int
}
type treeSet map[treeCoord]bool

func (t treePatch) getCol(idx int) treeLine {
	ts := treeLine{}
	for _, row := range t {
		ts = append(ts, row[idx])
	}
	return ts
}

func (t treeSet) addVisible(ts treeLine, isRow bool, idx int) {
	s := len(ts)
	getCoord := func(i int) treeCoord {
		if isRow {
			return treeCoord{row: idx, col: i}
		} else {
			return treeCoord{row: i, col: idx}
		}
	}
	// Left-to-right scan, stopping if we hit a tree with height 9.
	maxHeight := ts[0]
	lastVisible := 0
	for c := 1; c < s-1; c++ {
		if h := ts[c]; h > maxHeight {
			t[getCoord(c)] = true
			maxHeight = h
			lastVisible = c
			if h == 9 {
				break
			}
		}
	}
	// Right-to-left scan, up to the last visible tree from the
	// left-to-right scan.
	maxHeight = ts[s-1]
	for c := s - 2; c > lastVisible; c-- {
		if h := ts[c]; h > maxHeight {
			t[getCoord(c)] = true
			maxHeight = h
			if h == 9 {
				break
			}
		}
	}
}

func (t treePatch) countVisibleTrees() int {
	s := len(t[0])
	v := make(treeSet)
	for r := 1; r < s-1; r++ {
		v.addVisible(t[r], true, r)
	}
	for c := 1; c < s-1; c++ {
		v.addVisible(t.getCol(c), false, c)
	}
	return len(v) + 4*(s-1)
}

func (t treePatch) getScenicScore(r int, c int) int {
	h := t[r][c]
	s := len(t[0])
	// Look up
	col := t.getCol(c)
	up := 0
	for i := r - 1; i >= 0; i-- {
		up++
		if col[i] >= h {
			break
		}
	}
	// Look down
	down := 0
	for i := r + 1; i < s; i++ {
		down++
		if col[i] >= h {
			break
		}
	}
	// Look left
	left := 0
	for i := c - 1; i >= 0; i-- {
		left++
		if t[r][i] >= h {
			break
		}
	}
	// Look right
	right := 0
	for i := c + 1; i < s; i++ {
		right++
		if t[r][i] >= h {
			break
		}
	}
	return up * down * left * right
}

func (t treePatch) findBestScenicScore() int {
	s := len(t[0])
	best := 0
	for r := 1; r < s-1; r++ {
		for c := 1; c < s-1; c++ {
			curr := t.getScenicScore(r, c)
			if curr > best {
				best = curr
			}
		}
	}
	return best
}

func parseInput(input string) treePatch {
	ts := treePatch{}
	for _, i := range strings.Split(input, "\n") {
		row := treeLine{}
		for _, t := range i {
			row = append(row, int(t-'0'))
		}
		ts = append(ts, row)
	}
	return ts
}

func solve(input string) aoc.Solution[int, int] {
	ts := parseInput(input)
	return aoc.Solution[int, int]{
		PartOne: ts.countVisibleTrees(),
		PartTwo: ts.findBestScenicScore(),
	}
}

func main() {
	puzzleInput := aoc.LoadInput("input.txt")
	timedSolve := aoc.Timer("Day eight", solve)
	timedSolve(puzzleInput)
}
