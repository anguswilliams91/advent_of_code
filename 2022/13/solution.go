package main

import (
	"aoc"
	"encoding/json"
	"sort"
	"strings"
)

type pair [2]any

func parseInput(input string) ([]*pair, []string) {
	pairs := []*pair{}
	all := []string{"[[2]]", "[[6]]"}
	for _, ls := range strings.Split(input, "\n\n") {
		s := strings.Split(ls, "\n")
		var p, q any
		json.Unmarshal([]byte(s[0]), &p)
		json.Unmarshal([]byte(s[1]), &q)
		ps := pair{p, q}
		all = append(all, s...)
		pairs = append(pairs, &ps)
	}
	return pairs, all
}

func compare(p any, q any) int {
	ps, pok := p.([]any)
	qs, qok := q.([]any)
	switch {
	case !pok && !qok:
		return int(p.(float64) - q.(float64))
	case !qok:
		qs = []any{q}
	case !pok:
		ps = []any{p}
	}
	for i := 0; i < len(ps) && i < len(qs); i++ {
		if c := compare(ps[i], qs[i]); c != 0 {
			return c
		}
	}
	return len(ps) - len(qs)
}

func stringCompare(s string, t string) bool {
	var p, q any
	json.Unmarshal([]byte(s), &p)
	json.Unmarshal([]byte(t), &q)
	if c := compare(p, q); c < 0 {
		return true
	} else {
		return false
	}
}

func solve(input string) aoc.Solution[int, int] {
	pairs, all := parseInput(input)
	partOne := 0
	for i, pair := range pairs {
		if c := compare(pair[0], pair[1]); c <= 0 {
			partOne += i + 1
		}
	}
	sort.Slice(all, func(i, j int) bool {
		return stringCompare(all[i], all[j])
	})
	key := 1
	for i, s := range all {
		if s == "[[2]]" || s == "[[6]]" {
			key *= (i + 1)
		}
	}
	return aoc.Solution[int, int]{PartOne: partOne, PartTwo: key}
}

func main() {
	puzzleInput := aoc.LoadInput("input.txt")
	timedSolve := aoc.Timer("Day thirteen", solve)
	timedSolve(puzzleInput)
}
