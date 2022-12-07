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
	parent   map[string]string
	children map[string][]string
	size     map[string]int
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
	t := directoryTree{
		parent:   make(map[string]string),
		children: make(map[string][]string),
		size:     make(map[string]int),
	}
	for _, out := range strings.Split(input, "\n") {
		if m := cdRe.FindAllStringSubmatch(out, -1); len(m) > 0 {
			dir := m[0][1]
			curDir = cd(curDir, dir, &t)
		} else if m := dirRe.FindAllStringSubmatch(out, -1); len(m) > 0 {
			dir := curDir + "/" + m[0][1]
			t.parent[dir] = curDir
			t.children[curDir] = append(t.children[curDir], dir)
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

// Uses breadth-first search to find the smallest directory that can be deleted.
func (t *directoryTree) findSmallestDirToDelete(total int, updateSize int) int {
	required := updateSize - total + t.size["/"]
	m := t.size["/"]
	queue := t.children["/"]
	for len(queue) > 0 {
		dir := queue[0]
		queue = queue[1:]
		s := t.size[dir]
		if s >= required {
			if s < m {
				m = s
			}
			if s > required {
				queue = append(queue, t.children[dir]...)
			}
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
