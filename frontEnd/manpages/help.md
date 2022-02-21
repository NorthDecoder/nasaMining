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

```

## Code Usage


```javascript
// wogger is winston logger!
// wogger javascript syntax
const wogger = require('../utilities/wogger.js');
wogger.info( 'My message here' + aVariableHere )
wogger.debug( 'A debugging message here' )

```


## Reference

1. winston logging levels [:link:](https://github.com/winstonjs/winston#logging-levels)
