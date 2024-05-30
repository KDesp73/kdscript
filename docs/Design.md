# Design

## Pre-defined methods

- echo "Hello World"
- exit `exit-code` (int)

- input() -- Should change
- val(expression) -- Should change
- str(expression) -- Should change

## Blocks

- if-else

```
if condition {

} else {

}

if condition {

} else if condition {

} else {

}
```

- while

```
while condition {

}
```

- do-while

```
do {

} while condition
```

- for

```
for i in 2..3 {

}
```

## Functions 

```
# Declaration
func name {

}

# Call
call name

# Call with arguments
call name <- x, 2, 3

# Get return value
a = call name <- 1.3
```

## Casting

```
a = 5 as float
```

## Preprocessor

@ indicates preprocessor tag

```
@import "path/to/file" -- Include methods from file
@alias A 2
@run "path/to/file" -- Run file as script
@export a
```

## Comments

```
# Single line comment

-#
Multi-
line
Comment
#-
```
