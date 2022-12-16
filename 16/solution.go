package main

import (
	"aoc"
	"encoding/json"
	"fmt"
	"regexp"
	"sort"
	"strings"
)

const (
	partOneTime = 30
	partTwoTime = 26
)

type valve struct {
	name       string
	flowRate   int
	neighbours map[string]int
}

type graph map[string]*valve

// simplify removes nodes with flow rate zero that
// are not the starting node.
func (gp *graph) simplify() {
	g := *gp
	toDelete := []string{}
	for name, valve := range g {
		if valve.flowRate == 0 && name != "AA" {
			for neighbour, d0 := range valve.neighbours {
				for n, d1 := range valve.neighbours {
					if n != neighbour {
						g[neighbour].neighbours[n] = d0 + d1
					}
				}
				delete(g[neighbour].neighbours, name)
			}
			toDelete = append(toDelete, name)
		}
	}
	for _, name := range toDelete {
		delete(g, name)
	}
}

func min(i, j int) int {
	if i < j {
		return i
	}
	return j
}

func max(i, j int) int {
	if i > j {
		return i
	}
	return j
}

// getDistances uses the Floyd-Warshall algorithm to get the minimum
// distance from each valve to every other valve.
// https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
func getDistances(g graph) map[string]map[string]int {
	distances := make(map[string]map[string]int)
	names := make([]string, len(g))
	i := 0
	for k := range g {
		names[i] = k
		i++
	}
	sort.Slice(names, func(i, j int) bool { return names[i] < names[j] })
	for _, i := range names {
		distances[i] = make(map[string]int)
		for _, j := range names {
			if d, ok := g[i].neighbours[j]; ok {
				distances[i][j] = d
			} else {
				// 1000 is practical "inf" for this problem.
				distances[i][j] = 1000
			}
		}
	}
	for _, i := range names {
		for _, j := range names {
			for _, k := range names {
				distances[i][j] = min(distances[i][j], distances[i][k]+distances[k][j])
			}
		}
	}
	return distances
}

func parseInput(input string) graph {
	g := make(graph)
	for _, l := range strings.Split(input, "\n") {
		s := strings.Split(l, "; ")
		var name string
		var flowRate int
		fmt.Sscanf(s[0], "Valve %s has flow rate=%d", &name, &flowRate)
		if v, ok := g[name]; !ok {
			g[name] = &valve{
				name: name, flowRate: flowRate,
				neighbours: make(map[string]int),
			}
		} else {
			v.flowRate = flowRate
		}
		names := regexp.MustCompile("[A-Z]{2}").FindAll([]byte(s[1]), -1)
		for _, n := range names {
			ns := string(n)
			if _, ok := g[ns]; !ok {
				g[ns] = &valve{name: ns, neighbours: make(map[string]int)}
			}
			if _, ok := g[ns].neighbours[name]; !ok {
				g[ns].neighbours[name] = 1
			}
			if _, ok := g[name].neighbours[ns]; !ok {
				g[name].neighbours[ns] = 1
			}
		}
	}
	return g
}

type state struct {
	valve            string
	time             int
	opened           map[string]bool
	pressureReleased int
}

type queue[T any] []*T

func (q *queue[T]) pop() T {
	head := (*q)[0]
	*q = (*q)[1:]
	return *head
}

func (q *queue[T]) push(v T) {
	*q = append(*q, &v)
}

func copy[T comparable, U any](m map[T]U) map[T]U {
	new := make(map[T]U)
	for k, v := range m {
		new[k] = v
	}
	return new
}

func getPressures(g graph, maxTime int) map[string]int {
	distances := getDistances(g)
	s := state{
		valve:            "AA",
		time:             maxTime,
		opened:           map[string]bool{"AA": true},
		pressureReleased: 0,
	}
	pressures := make(map[string]int)
	q := queue[state]{&s}
	for len(q) > 0 {
		c := q.pop()
		// Can't use a map as a key to another map in
		// Golang, so convert to string using JSON.
		k, _ := json.Marshal(c.opened)
		pressures[string(k)] = max(
			pressures[string(k)],
			c.pressureReleased,
		)
		for n, v := range g {
			t := c.time - distances[c.valve][n] - 1
			if _, ok := c.opened[n]; ok || t <= 0 {
				continue
			}
			opened := copy(c.opened)
			opened[n] = true
			next := state{
				valve:            n,
				time:             t,
				opened:           opened,
				pressureReleased: c.pressureReleased + t*v.flowRate,
			}
			q.push(next)
		}
	}
	return pressures
}

func partOne(g graph) int {
	pressures := getPressures(g, partOneTime)
	maxPressure := 0
	for _, v := range pressures {
		if v > maxPressure {
			maxPressure = v
		}
	}
	return maxPressure
}

func memoized[T comparable, U any](expensive func(x T) U) func(x T) U {
	cache := make(map[T]U)
	return func(x T) U {
		if r, ok := cache[x]; ok {
			return r
		}
		y := expensive(x)
		cache[x] = y
		return y
	}
}

func noOverlapExcept(p map[string]bool, q map[string]bool, exception string) bool {
	for k := range p {
		if _, ok := q[k]; ok && k != exception {
			return false
		}
	}
	return true
}

func partTwo(g graph) int {
	pressures := getPressures(g, partTwoTime)
	maxPressure := 0
	getVisited := memoized(
		func(s string) map[string]bool {
			v := make(map[string]bool)
			json.Unmarshal([]byte(s), &v)
			return v
		},
	)
	for v1, p1 := range pressures {
		for v2, p2 := range pressures {
			if v1 != v2 {
				if noOverlapExcept(getVisited(v1), getVisited(v2), "AA") {
					if p := p1 + p2; p > maxPressure {
						maxPressure = p
					}
				}
			}
		}
	}
	return maxPressure
}

func solve(input string) aoc.Solution[int, int] {
	g := parseInput(input)
	g.simplify()
	return aoc.Solution[int, int]{
		PartOne: partOne(g),
		PartTwo: partTwo(g),
	}
}

func main() {
	puzzleInput := aoc.LoadInput("input.txt")
	timedSolve := aoc.Timer("Day sixteen", solve)
	timedSolve(puzzleInput)
}
