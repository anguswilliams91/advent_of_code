package main

import (
	"aoc"
	"fmt"
	"image"
	"log"
	"sort"
	"strings"
)

const (
	yPartOne = 2000000
	xyMin    = 0
	xyMax    = 4000000
)

type interval struct{ min, max int }

func parseInput(input string) map[image.Point]image.Point {
	sensors := make(map[image.Point]image.Point)
	for _, l := range strings.Split(input, "\n") {
		var s, b image.Point
		fmt.Sscanf(
			l,
			"Sensor at x=%d, y=%d: closest beacon is at x=%d, y=%d",
			&s.X, &s.Y, &b.X, &b.Y,
		)
		sensors[s] = b
	}
	return sensors
}

func abs(a int) int {
	if a < 0 {
		return -a
	}
	return a
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func L1(p, q image.Point) int {
	return abs(p.X-q.X) + abs(p.Y-q.Y)
}

func ruleOutLocations(sensor, beacon image.Point, y int) (interval, bool) {
	d := L1(sensor, beacon)
	if dy := abs(sensor.Y - y); dy <= d {
		return interval{dy - d + sensor.X, d - dy + sensor.X}, true
	}
	return interval{}, false
}

func merge(rs []interval) []interval {
	sort.Slice(rs, func(i, j int) bool { return rs[i].min < rs[j].min })
	merged := []interval{}
	for _, r := range rs {
		if len(merged) == 0 || merged[len(merged)-1].max < r.min {
			merged = append(merged, r)
		} else {
			merged[len(merged)-1].max = max(merged[len(merged)-1].max, r.max)
		}
	}
	return merged
}

func numExcludedPoints(rs []interval, sensors map[image.Point]image.Point, y int) int {
	n := 0
	seen := map[image.Point]bool{}
	for _, r := range rs {
		n += r.max - r.min + 1
		for _, b := range sensors {
			_, ok := seen[b]
			if !ok && b.Y == y && b.X >= r.min && b.X <= r.max {
				n -= 1
				seen[b] = true
			}
		}
	}
	return n
}

func getMergedIntervals(m map[image.Point]image.Point, y int) []interval {
	rs := []interval{}
	for s, b := range m {
		c, hasPoints := ruleOutLocations(s, b, y)
		if hasPoints {
			rs = append(rs, c)
		}
	}
	return merge(rs)
}

func partOne(m map[image.Point]image.Point) int {
	merged := getMergedIntervals(m, yPartOne)
	return numExcludedPoints(merged, m, yPartOne)
}

func PartTwo(m map[image.Point]image.Point) int {
	// TODO: This is really slow ~10s, speed it up!
	for y := xyMin; y <= xyMax; y++ {
		merged := getMergedIntervals(m, y)
		p := interval{xyMin, xyMax}
		found := false
		for _, r := range merged {
			if !(r.min <= xyMin && r.max >= xyMax) {
				found = true
				if r.max > p.min && r.max < xyMax {
					p.min = r.max
				}
				if r.min < p.max && r.min > xyMin {
					p.max = r.min
				}
			}
		}
		if found {
			return (p.min+1)*4000000 + y
		}

	}
	log.Fatal("Didn't find a solution!")
	return -1
}

func solve(input string) aoc.Solution[int, int] {
	m := parseInput(input)
	return aoc.Solution[int, int]{
		PartOne: partOne(m),
		PartTwo: PartTwo(m),
	}
}

func main() {
	puzzleInput := aoc.LoadInput("input.txt")
	timedSolve := aoc.Timer("Day fifteen", solve)
	timedSolve(puzzleInput)
}
