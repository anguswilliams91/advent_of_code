package main

import (
	"aoc"
	"fmt"
	"math"
	"strings"
)

const (
	ore      = 0
	clay     = 1
	obsidian = 2
	geode    = 3
)

type resources [4]int

type blueprint struct {
	id             int
	robotPrices    [4][4]int
	resourceLimits resources
}

func parseInput(input string) []blueprint {
	bs := []blueprint{}
	for _, s := range strings.Split(input, "\n") {
		b := blueprint{
			resourceLimits: resources{},
			robotPrices:    [4][4]int{},
		}
		fmt.Sscanf(
			s,
			"Blueprint %d: Each ore robot costs %d ore. Each clay robot costs %d ore. Each obsidian robot costs %d ore and %d clay. Each geode robot costs %d ore and %d obsidian.",
			&b.id,
			&b.robotPrices[ore][ore],
			&b.robotPrices[clay][ore],
			&b.robotPrices[obsidian][ore],
			&b.robotPrices[obsidian][clay],
			&b.robotPrices[geode][ore],
			&b.robotPrices[geode][obsidian],
		)
		b.resourceLimits[ore] = aoc.Max(
			b.robotPrices[ore][ore],
			b.robotPrices[clay][ore],
			b.robotPrices[clay][ore],
			b.robotPrices[geode][ore],
		)
		b.resourceLimits[clay] = b.robotPrices[obsidian][clay]
		b.resourceLimits[obsidian] = b.robotPrices[geode][obsidian]
		b.resourceLimits[geode] = math.MaxInt
		bs = append(bs, b)
	}
	return bs
}

func (m *resources) sub(other resources) resources {
	new := resources{}
	for k, v := range *m {
		new[k] = v - other[k]
	}
	return new
}

func (m *resources) add(other resources) resources {
	new := resources{}
	for k, v := range *m {
		new[k] = v + other[k]
	}
	return new
}

func (m *resources) isPositive() bool {
	for _, v := range *m {
		if v < 0 {
			return false
		}
	}
	return true
}

type state struct {
	robots      resources
	resources   resources
	minutesLeft int
}

func getUpperBound(s state) int {
	geodes := s.resources[geode]
	geodes += s.robots[geode] * s.minutesLeft
	// Assume we can build a geode making robot every turn from now.
	geodes += (s.minutesLeft - 1) * s.minutesLeft / 2
	return geodes
}

func getNextStates(s state, b blueprint, bound int, seen *map[state]struct{}) []state {
	next := []state{}
	for _, r := range []int{geode, obsidian, clay, ore} {
		n := s.resources.sub(b.robotPrices[r])
		if n.isPositive() && s.robots[r] < b.resourceLimits[r] {
			newRobots := s.robots
			newRobots[r] += 1
			rs := state{
				robots:      newRobots,
				resources:   n.add(s.robots),
				minutesLeft: s.minutesLeft - 1,
			}
			if _, ok := (*seen)[rs]; !ok && getUpperBound(rs) > bound {
				next = append(next, rs)
				(*seen)[rs] = struct{}{}
				if r == geode {
					return next
				}
			}
		}
	}
	ns := state{
		robots:      s.robots,
		resources:   s.resources.add(s.robots),
		minutesLeft: s.minutesLeft - 1,
	}
	if _, ok := (*seen)[ns]; !ok && getUpperBound(ns) > bound {
		next = append(next, ns)
		(*seen)[ns] = struct{}{}
	}
	return next
}

func getMostGeodes(b blueprint, totalMinutes int) int {
	initState := state{
		robots:      resources{ore: 1, clay: 0, obsidian: 0, geode: 0},
		resources:   resources{ore: 0, clay: 0, obsidian: 0, geode: 0},
		minutesLeft: totalMinutes,
	}
	mostGeodes := 0
	ss := aoc.Stack[state]{initState}
	seen := map[state]struct{}{initState: {}}
	for len(ss) > 0 {
		s := ss.Pop()
		if s.minutesLeft == 1 {
			mostGeodes = aoc.Max(mostGeodes, s.resources.add(s.robots)[geode])
			continue
		}
		nextStates := getNextStates(s, b, mostGeodes, &seen)
		ss.Push(nextStates...)
	}
	return mostGeodes
}

func solve(input string) aoc.Solution[int, int] {
	bs := parseInput(input)
	qualityScoreSum := 0
	mostGeodesProduct := 1
	i := 0
	for _, b := range bs {
		qualityScoreSum += b.id * getMostGeodes(b, 24)
		if i < 3 {
			mostGeodesProduct *= getMostGeodes(b, 32)
			fmt.Println(mostGeodesProduct)
		}
		i++
	}
	return aoc.Solution[int, int]{
		PartOne: qualityScoreSum,
		PartTwo: mostGeodesProduct,
	}
}

func main() {
	puzzleInput := aoc.LoadInput("input.txt")
	timedSolve := aoc.Timer("Day nineteen", solve)
	timedSolve(puzzleInput)
}
