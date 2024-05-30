# kd interpreter

## Install

```sh
./install.sh
```


## Usage

1. Write your script
2. Run with: 

```sh
kdscript filename.kd
```

## Example Script

```
# Method to print a star pyramid of user defined height
func printPyramid {
    i = 1
    while i <= _1 {
        spaces = _1 - i
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

echo "Enter height: "
height = val(input())

call printPyramid <- height
```

## LICENSE

[GNU](./LICENSE)

## Author

[KDesp73](https://github.com/KDesp73)

