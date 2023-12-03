package main

import (
	"aoc"
	"strconv"
	"strings"
)

const (
	noopCycles  int = 1
	addXCycles  int = 2
	firstCycle  int = 20
	imageWidth  int = 40
	imageHeight int = 6
)

type cpu struct {
	register     int
	prevRegister int
	cycles       int
}

type instruction struct {
	name      string
	increment int
}

func (c *cpu) do(i instruction) {
	c.prevRegister = c.register
	switch i.name {
	case "noop":
		c.cycles += noopCycles
	case "addx":
		c.cycles += addXCycles
		c.register += i.increment
	}
}

func parseInput(input string) []instruction {
	instructions := []instruction{}
	for _, s := range strings.Split(input, "\n") {
		i := instruction{}
		if s == "noop" {
			i.name = s
		} else {
			i.name = "addx"
			i.increment, _ = strconv.Atoi(strings.Split(s, " ")[1])
		}
		instructions = append(instructions, i)
	}
	return instructions
}

func newImage() []string {
	pixels := []string{}
	for i := 0; i < imageHeight*imageWidth; i++ {
		pixels = append(pixels, ".")
	}
	return pixels
}

func renderImage(img []string) string {
	rendered := "\n"
	for i, pixel := range img {
		rendered += pixel
		if (i+1)%imageWidth == 0 {
			rendered += "\n"
		}
	}
	return rendered
}

func (c *cpu) runProgram(instructions []instruction) (int, string) {
	sum := 0
	img := newImage()
	cycles := map[string]int{"noop": noopCycles, "addx": addXCycles}
	for _, i := range instructions {
		c.do(i)
		// Calculates signal strengths
		if d := (c.cycles - firstCycle); d%imageWidth == 0 {
			sum += c.prevRegister * c.cycles
		} else if d%imageWidth < cycles[i.name] && d > 0 {
			sum += c.prevRegister * (c.cycles - d%imageWidth)
		}
		// Displays sprite
		for j := 0; j < cycles[i.name]; j++ {
			isSprite := (c.cycles - j - 1) % imageWidth
			if isSprite >= c.prevRegister-1 && isSprite <= c.prevRegister+1 {
				img[c.cycles-j-1] = "#"
			}
		}
	}
	return sum, renderImage(img)
}

func solve(input string) aoc.Solution[int, string] {
	c := cpu{register: 1, prevRegister: -1}
	instructions := parseInput(input)
	partOne, partTwo := c.runProgram(instructions)
	return aoc.Solution[int, string]{PartOne: partOne, PartTwo: partTwo}
}

func main() {
	puzzleInput := aoc.LoadInput("input.txt")
	timedSolve := aoc.Timer("Day ten", solve)
	timedSolve(puzzleInput)
}
