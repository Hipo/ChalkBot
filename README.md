# ChalkBot

Read about on [the Hipo Engineering Blog](http://engineering.hipolabs.com/chalkbot/)

## Usage
```sh
python draw.py hipo.json > commands
python simulator.py < commands
python arduino_serial.py commands
```


### To generate the gif:
```sh
cd output
convert -delay 10 -loop 0 frame*.png animation.gif
```

![](http://engineering.hipolabs.com/content/images/2016/05/hipo.gif)
