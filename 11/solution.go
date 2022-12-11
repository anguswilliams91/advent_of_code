package main

import (
	"aoc"
	"regexp"
	"sort"
	"strconv"
	"strings"
)

type monkey struct {
	items      []int
	operation  func(int) int
	factor     int
	goodMonkey int
	badMonkey  int
}

type monkeys []*monkey

func (m *monkey) inspect(isPartOne bool, productOfFactors int) (int, int) {
	item := m.items[0]
	m.items = m.items[1:]
	item = m.operation(item)
	if isPartOne {
		item = item / 3
	}
	// Each monkey's factor is a unique prime, so we just need to
	// keep track of the modulus of the item value w.r.t. the
	// product of those factors.
	item = item % productOfFactors
	if item%m.factor == 0 {
		return m.goodMonkey, item
	} else {
		return m.badMonkey, item
	}
}

func monkeyBusiness(ms monkeys, rounds int, isPartOne bool) int {
	n := make([]int, len(ms))
	productOfFactors := 1
	for _, m := range ms {
		productOfFactors *= m.factor
	}
	for r := 0; r < rounds; r++ {
		for i, m := range ms {
			for len(m.items) > 0 {
				throwTo, item := m.inspect(isPartOne, productOfFactors)
				ms[throwTo].items = append(ms[throwTo].items, item)
				n[i]++
			}
		}
	}
	sort.Slice(
		n, func(i, j int) bool { return n[i] > n[j] },
	)
	return n[0] * n[1]
}

func parseItems(s string) []int {
	items := []int{}
	re := regexp.MustCompile(`\d+`)
	for _, g := range re.FindAllStringSubmatch(s, -1) {
		item, _ := strconv.Atoi(g[0])
		items = append(items, item)
	}
	return items
}

func parseOperation(s string) func(int) int {
	rhs := strings.TrimSpace(strings.Split(s, "=")[1])
	terms := strings.Split(rhs, " ")
	var f func(int) int
	if terms[0] == terms[2] {
		f = func(x int) int { return x * x }
	} else {
		val, _ := strconv.Atoi(terms[2])
		switch terms[1] {
		case "*":
			f = func(x int) int { return x * val }
		case "+":
			f = func(x int) int { return x + val }
		}
	}
	return f
}

func parseInt(s string) int {
	re := regexp.MustCompile(`\d+`)
	factor, _ := strconv.Atoi(re.FindStringSubmatch(s)[0])
	return factor
}

func parseMonkey(s string) monkey {
	lines := strings.Split(s, "\n")
	return monkey{
		items:      parseItems(lines[1]),
		operation:  parseOperation(lines[2]),
		factor:     parseInt(lines[3]),
		goodMonkey: parseInt(lines[4]),
		badMonkey:  parseInt(lines[5]),
	}
}

func parseMonkeys(s string) monkeys {
	ms := monkeys{}
	for _, l := range strings.Split(s, "\n\n") {
		m := parseMonkey(l)
		ms = append(ms, &m)
	}
	return ms
}

func solve(input string) aoc.Solution[int, int] {
	return aoc.Solution[int, int]{
		PartOne: monkeyBusiness(parseMonkeys(input), 20, true),
		PartTwo: monkeyBusiness(parseMonkeys(input), 10000, false),
	}
}

func main() {
	puzzleInput := aoc.LoadInput("input.txt")
	timedSolve := aoc.Timer("Day eleven", solve)
	timedSolve(puzzleInput)
}
