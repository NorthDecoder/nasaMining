# Diagrams

## Data aquisition

```mermaid
stateDiagram-v2
    [*] --> inputs
    inputs -->url=data.nasa.gov/data.json
    inputs -->nasa.json
    url=data.nasa.gov/data.json --> wget_url
    wget_url --> ~/nasaMining/data/nasa.json
    nasa.json --> wget_url
    ~/nasaMining/data/nasa.json --> [*]
```


## Keyword preprocessing

## Frontend


### Reference

- [mermiad-js](https://mermaid-js.github.io/mermaid/#/) specifications
- [mermaid.live](https://mermaid.live) online editor



