package aoc

import (
	"fmt"
	"io/ioutil"
	"log"
	"math"
	"time"
)

type Solution[T, U any] struct {
	PartOne T
	PartTwo U
}

type intSlice []int64

// LoadInput loads a puzzle's input from a path p into a string.
func LoadInput(p string) string {
	input, err := ioutil.ReadFile(p)
	if err != nil {
		log.Fatal("Couldn't load puzzle input.")
	}
	return string(input)
}

// Timer returns a function that runs a solution up to 100 times
// and measures the mean runtime and the standard deviation.
func Timer[T, U any](name string, solution func(string) Solution[T, U]) func(string) {
	return func(input string) {
		var ns intSlice
		var totalDuration time.Duration
		for i := 0; i < 100; i++ {
			start := time.Now()
			s := solution(input)
			t := time.Since(start)
			if i == 0 {
				fmt.Println("Part one: ", s.PartOne)
				fmt.Println("Part two: ", s.PartTwo)
			}
			ns = append(ns, t.Nanoseconds())
			totalDuration += t
			if totalDuration > 10*time.Second {
				break
			}
		}
		if len(ns) >= 3 {
			fmt.Printf(
				"%s runtime from %v trials = %s +/- %s\n",
				name,
				len(ns),
				time.Duration(ns.avg())*time.Nanosecond,
				time.Duration(ns.std())*time.Nanosecond,
			)
		} else {
			fmt.Printf(
				"%s runtime from %v trials = %s\n",
				name,
				len(ns),
				time.Duration(ns.avg())*time.Nanosecond,
			)
		}

	}
}

func (xs intSlice) avg() int64 {
	var t int64 = 0
	for _, x := range xs {
		t += x
	}
	return t / int64(len(xs))
}

func (xs intSlice) std() int64 {
	mean := xs.avg()
	sumSq := 0
	for _, x := range xs {
		sumSq += int(math.Pow(float64(x-mean), 2))
	}
	return int64(math.Sqrt(float64(sumSq) / float64(len(xs)-1)))
}

type number interface {
	int | int8 | int16 | int32 | int64 | float32 | float64
}

// Min finds the minimum of two numbers.
func Min[T number](i, j T) T {
	if i < j {
		return i
	}
	return j
}

// Max finds the maximum of two numbers.
func Max[T number](i, j T) T {
	if i > j {
		return i
	}
	return j
}

// Abs returns the absolute value of a number.
func Abs[T number](i T) T {
	if i < 0 {
		return -i
	}
	return i
}

// Sign returns the sign of a number.
func Sign[T number](x T) T {
	if x > 0 {
		return 1
	} else if x < 0 {
		return -1
	} else {
		return 0
	}
}

// Divmod returns the result of integer division plus the modulus.
func Divmod(i, j int) (int, int) {
	return i / j, i % j
}

type Queue[T any] []T

// Pop removes the first item from a Queue
// and returns it.
func (q *Queue[T]) Pop() T {
	head := (*q)[0]
	*q = (*q)[1:]
	return head
}

// Push sends a new value to the back of
// the Queue.
func (q *Queue[T]) Push(v T) {
	*q = append(*q, v)
}

// Memoized returns a memoized version of `expensive`.
func Memoized[T comparable, U any](expensive func(x T) U) func(x T) U {
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
