package main

import (
	"aoc"
	"fmt"
	"regexp"
	"strings"
)

const stackRegex = "([ ]{3}|\\[([A-Z])\\])([ ]|\n){0,1}"

type stack []string
type stacks map[int]stack
type instruction struct {
	num  int
	from int
	to   int
}

func parseStacks(input string) ([]string, stacks) {
	s := stacks{}
	r := regexp.MustCompile(stackRegex)
	ls := strings.Split(input, "\n")
	l := -1
	for j, line := range ls {
		m := r.FindAllSubmatch([]byte(line), -1)
		if len(m) > 0 {
			for i, g := range m {
				if c := g[2]; len(c) > 0 {
					s[i+1] = append(s[i+1], string(c[0]))
				}
			}
		} else {
			l = j
			break
		}
	}
	return ls[l+1:], s
}

func parseInstructions(input []string) []instruction {
	instructions := []instruction{}
	for _, s := range input {
		i := instruction{}
		fmt.Sscanf(
			s,
			"move %d from %d to %d",
			&i.num,
			&i.from,
			&i.to,
		)
		instructions = append(instructions, i)
	}
	return instructions
}

func (s stacks) crateMover9000(instructions []instruction) stacks {
	for _, i := range instructions {
		n := 0
		for n < i.num {
			toMove := s[i.from][0]
			s[i.from] = s[i.from][1:]
			s[i.to] = append(stack{toMove}, s[i.to]...)
			n++
		}
	}
	return s
}

func (s stacks) crateMover9001(instructions []instruction) stacks {
	for _, i := range instructions {
		toMove := make(stack, i.num)
		copy(toMove, s[i.from][:i.num])
		s[i.to] = append(toMove, s[i.to]...)
		s[i.from] = s[i.from][i.num:]
	}
	return s
}

func (s stacks) copy() stacks {
	sNew := stacks{}
	for k, v := range s {
		sNew[k] = make(stack, len(v))
		copy(sNew[k], v)
	}
	return sNew
}

func solve(input string) aoc.Solution[string, string] {
	rest, s9000 := parseStacks(input)
	s9001 := s9000.copy()
	instructions := parseInstructions(rest)
	s9000 = s9000.crateMover9000(instructions)
	s9001 = s9001.crateMover9001(instructions)
	var parts [2]string
	for i, s := range []stacks{s9000, s9001} {
		for j := 1; j <= len(s9000); j++ {
			parts[i] += s[j][0]
		}
	}
	return aoc.Solution[string, string]{PartOne: parts[0], PartTwo: parts[1]}
}

func main() {
	puzzleInput := aoc.LoadInput("input.txt")
	timedSolve := aoc.Timer("Day five", solve)
	timedSolve(puzzleInput)
}
