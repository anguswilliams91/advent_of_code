package main

import (
	"aoc"
	"encoding/json"
	"sort"
	"strings"
)

const (
	no        = 0
	ambiguous = 1
	yes       = 2
)

type packet []interface{}
type pair [2]packet

func parseInput(input string) ([]*pair, []string) {
	pairs := []*pair{}
	all := []string{"[[2]]", "[[6]]"}
	for _, ls := range strings.Split(input, "\n\n") {
		ps := pair{}
		for i, l := range strings.Split(ls, "\n") {
			p := packet{}
			json.Unmarshal([]byte(l), &p)
			ps[i] = p
			all = append(all, l)
		}
		pairs = append(pairs, &ps)
	}
	return pairs, all
}

func (p *packet) pop() (any, bool) {
	head := (*p)[0]
	(*p)[0] = nil
	*p = (*p)[1:]
	_, ok := head.(float64)
	if ok {
		return head, true
	} else {
		return head, false
	}
}

func wrap(x any) []interface{} {
	return []interface{}{x}
}

func (ps *pair) compare() int {
	isEmpty0 := len(ps[0]) == 0
	isEmpty1 := len(ps[1]) == 0
	if isEmpty0 && !isEmpty1 {
		return yes
	} else if !isEmpty0 && isEmpty1 {
		return no
	} else if isEmpty0 && isEmpty1 {
		return ambiguous
	}
	v0, isNum0 := ps[0].pop()
	v1, isNum1 := ps[1].pop()
	if isNum0 && isNum1 {
		if v0.(float64) < v1.(float64) {
			return yes
		} else if v0.(float64) > v1.(float64) {
			return no
		} else {
			return ps.compare()
		}
	} else if isNum0 && !isNum1 {
		ps[0] = append(wrap(wrap(v0)), ps[0]...)
		ps[1] = append(wrap(v1), ps[1]...)
		return ps.compare()
	} else if !isNum0 && isNum1 {
		ps[0] = append(wrap(v0), ps[0]...)
		ps[1] = append(wrap(wrap(v1)), ps[1]...)
		return ps.compare()
	} else {
		v0 := v0.([]interface{})
		v1 := v1.([]interface{})
		n1 := len(v1)
		for i, subP0 := range v0 {
			if i == n1 {
				return no
			}
			qs := pair{packet{subP0}, packet{v1[i]}}
			out := qs.compare()
			if out == yes || out == no {
				return out
			}
		}
		if len(v0) < len(v1) {
			return yes
		}
		return ps.compare()

	}
}

func compare(s string, t string) bool {
	p := packet{}
	q := packet{}
	json.Unmarshal([]byte(s), &p)
	json.Unmarshal([]byte(t), &q)
	ps := pair{p, q}
	out := ps.compare()
	if out == yes || out == ambiguous {
		return true
	} else {
		return false
	}
}

func solve(input string) aoc.Solution[int, int] {
	pairs, all := parseInput(input)
	partOne := 0
	for i, pair := range pairs {
		state := pair.compare()
		if state == yes {
			partOne += i + 1
		}
	}
	sort.Slice(all, func(i, j int) bool {
		return compare(all[i], all[j])
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
	timedSolve := aoc.Timer("Day twelve", solve)
	timedSolve(puzzleInput)
}
