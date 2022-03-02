# Command line help
> for nasaMining/frontEnd/server.js

## CLI Usage

```bash
cd nasaMining/frontEnd/

# print this page
node server.js help
node server.js --help
node server.js --man=help


# set winston logger format
node server.js --logformat=simple
node server.js --logformat=json

# set winston log level (1)
node server.js --loglevel=info
node server.js --loglevel=debug

# set debug levels ( not part of winston )
noder server.js --debuglevels=1
noder server.js --debuglevels=1,2
noder server.js --debuglevels=1,2,3


# a combination of arguments
node server.js --debuglevels=1 --loglevel=debug --logformat=simple
```

## Code Usage


### wogger is winston logger!

```javascript
// wogger javascript syntax
const wogger = require('../utilities/wogger.js');
wogger.info( 'My message here' + aVariableHere )
wogger.debug( 'A debugging message here' + anthotherVar )

```

### Setting debuglevels

```javascript
var debugLevels = [1] //default to at least one level
//var debugLevels = [1,2,3]
//var debugLevels = [2,3]
//var debugLevels = [3]
//var debugLevels = [1]
commandLineArgs.forEach( argument => instruction(argument) )

function instruction(cla) {
    var [ leftValue, rightValue ] = cla.split("=")
    switch(leftValue){
      case '--debuglevels':
        characterArray= rightValue.split( ',' )
        debugLevels = characterArray.map(x => parseInt(x))
        break;
    }
}


debugLevelOne   = debugLevels.filter( level => level === 1 )
debugLevelTwo   = debugLevels.filter( level => level === 2 )
debugLevelThree = debugLevels.filter( level => level === 3 )

if ( debugLevelOne[0] != undefined ){
   wogger.debug("\ndebug level 1")
   wogger.debug("serverMongo:" + serverMongo)
}


```


## Reference

1. winston logging levels [:link:](https://github.com/winstonjs/winston#logging-levels)
