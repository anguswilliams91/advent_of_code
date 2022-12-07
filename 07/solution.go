package main

import (
	"aoc"
	"regexp"
	"strconv"
	"strings"
)

const cdPattern string = "\\$ cd (\\/|\\S+|\\.\\.)$"
const dirPattern string = "dir (\\/|\\S+)$"
const filePattern string = "(\\d+) \\S+$"

type directoryTree struct {
	parent map[string]string
	size   map[string]int
}

func cd(curDir string, newDir string, t *directoryTree) string {
	if newDir == ".." {
		return t.parent[curDir]
	} else if newDir == "/" {
		return "/"
	} else {
		return curDir + "/" + newDir
	}
}

func (t *directoryTree) propagateFileSize(size int, dir string) {
	t.size[dir] += size
	p, ok := t.parent[dir]
	for ok {
		t.size[p] += size
		p, ok = t.parent[p]
	}
}

func browseFilesystem(input string) directoryTree {
	cdRe := regexp.MustCompile(cdPattern)
	dirRe := regexp.MustCompile(dirPattern)
	fileRe := regexp.MustCompile(filePattern)
	var curDir string
	t := directoryTree{parent: make(map[string]string), size: make(map[string]int)}
	for _, out := range strings.Split(input, "\n") {
		if m := cdRe.FindAllStringSubmatch(out, -1); len(m) > 0 {
			dir := m[0][1]
			curDir = cd(curDir, dir, &t)
		} else if m := dirRe.FindAllStringSubmatch(out, -1); len(m) > 0 {
			dir := curDir + "/" + m[0][1]
			t.parent[dir] = curDir
		} else if m := fileRe.FindAllStringSubmatch(out, -1); len(m) > 0 {
			size, _ := strconv.Atoi(m[0][1])
			t.propagateFileSize(size, curDir)
		} else {
			continue
		}
	}
	return t
}

func (t *directoryTree) sumDirSizesBelowThreshold(threshold int) int {
	sum := 0
	for _, size := range t.size {
		if size <= threshold {
			sum += size
		}
	}
	return sum
}

func (t *directoryTree) findSmallestDirToDelete(total int, updateSize int) int {
	required := updateSize - total + t.size["/"]
	m := t.size["/"]
	for _, size := range t.size {
		if size >= required && size < m {
			m = size
		}
	}
	return m
}

func solve(input string) aoc.Solution[int, int] {
	t := browseFilesystem(input)
	return aoc.Solution[int, int]{
		PartOne: t.sumDirSizesBelowThreshold(100000),
		PartTwo: t.findSmallestDirToDelete(70000000, 30000000),
	}
}

func main() {
	puzzleInput := aoc.LoadInput("input.txt")
	timedSolve := aoc.Timer("Day seven", solve)
	timedSolve(puzzleInput)
}
