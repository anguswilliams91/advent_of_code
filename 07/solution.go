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
	files    map[string][]int
	size     map[string]int
}

func (t *directoryTree) cd(curDir string, newDir string) string {
	if newDir == ".." {
		return t.parent[curDir]
	} else if newDir == "/" {
		return "/"
	} else {
		return curDir + "/" + newDir
	}
}

func (t *directoryTree) populateDirSize(dir string) {
	size := 0
	for _, s := range t.files[dir] {
		size += s
	}
	for _, c := range t.children[dir] {
		var cSize int
		if s, ok := t.size[c]; !ok {
			t.populateDirSize(c)
			cSize = t.size[c]
		} else {
			cSize = s
		}
		size += cSize
	}
	t.size[dir] = size
}

func browseFilesystem(input string) directoryTree {
	cdRe := regexp.MustCompile(cdPattern)
	dirRe := regexp.MustCompile(dirPattern)
	fileRe := regexp.MustCompile(filePattern)
	var curDir string
	t := directoryTree{
		parent:   make(map[string]string),
		children: make(map[string][]string),
		files:    make(map[string][]int),
		size:     make(map[string]int),
	}
	for _, out := range strings.Split(input, "\n") {
		if m := cdRe.FindAllStringSubmatch(out, -1); len(m) > 0 {
			dir := m[0][1]
			curDir = t.cd(curDir, dir)
		} else if m := dirRe.FindAllStringSubmatch(out, -1); len(m) > 0 {
			dir := curDir + "/" + m[0][1]
			t.parent[dir] = curDir
			t.children[curDir] = append(t.children[curDir], dir)
		} else if m := fileRe.FindAllStringSubmatch(out, -1); len(m) > 0 {
			size, _ := strconv.Atoi(m[0][1])
			t.files[curDir] = append(t.files[curDir], size)
		} else {
			continue
		}
	}
	t.populateDirSize("/")
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
	m := total
	for queue := t.children["/"]; len(queue) > 0; {
		dir := queue[0]
		queue = queue[1:]
		if s := t.size[dir]; s >= required {
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
