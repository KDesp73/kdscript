# kd interpreter

## Usage

1. Write your script
2. Run with: 

```sh
python3 src/main.py filename.kd
```

## Example Script

```
# Method to print a star pyramid of user defined height
func printPyramid {
    echo "Enter height: "
    height = val(input())
    i = 1
    while i <= height {
        spaces = height - i
        while spaces > 0 {
            echo " "
            spaces = spaces - 1
        }

        stars = 2 * i - 1
        while stars > 0 {
            echo "*"
            stars = stars - 1
        }

        echo "\n"
        i = i + 1
    }
}

call printPyramid
```

## LICENSE

[GNU](./LICENSE)

## Author

[KDesp73](https://github.com/KDesp73)

