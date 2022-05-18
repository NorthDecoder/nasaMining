# Inspecing the structure of nasa.json

Prepare the updated `nasa.json` as noted in the MongoWork
[initialization](https://github.com/NorthDecoder/nasaMining/blob/develop/docs/installation.md#initialization)
part of the installation instructions.

## Find the nasa data json files

```bash
cd ~/nasaMining/data
ls -al nasa*.json
```

----

## Exploring the JSON with [jq](https://github.com/stedolan/jq) installed

> for example on Fedora `sudo dnf install jq` .

Show the keys:

```bash
jq 'keys' nasa.json
```

Show the values of the key 'dataset':

```bash
cat nasa.json | jq '.dataset'
```

> displays the entire huge data set, type `ctrl+c` to cancel!

Show the original keyword array of each of the documents:

```bash
cat nasa.json | jq '.dataset' | jq '.[]' | jq '.keyword'
```

----

## Understanding the structure of the nasa_keywords.json with ngram_keywords added

After following the [readme](https://github.com/NorthDecoder/nasaMining/blob/develop/readme.md#keyword-extraction)
instuctions and running the `keywords/extract.py` script look at the new
keywords:

```bash
jq 'keys' nasa_keywords.json
```

> Note the keys are id numbers from 1 to around 16628 that are an index into
> the array of documents. A hint to access the elements of the array.

Try looking at all the records

```bash
cat nasa_keywords.json | jq .
```

> notice there is a new key `ngram_keywords` and values added to a copy of the
> original 'nasa.json' file, in the file 'nasa_keywords.json'.

Look at the ngram_keywords

```bash
cat nasa_keywords.json | jq '.[]' | jq '.ngram_keywords'
```

Compare 'keyword' to 'ngram_keywords'

```bash
cat nasa_keywords.json | jq -r '.[] | "\(.keyword) \(.ngram_keywords)"' | sed '/e/G'
```

Add the title, with newline after each data element, and space after 3 lines
and only print the first hundred documents for reference.

```bash
cat nasa_keywords.json | jq -r '.[] | "\(.title) \(.keyword) \(.ngram_keywords)"'\
                       | sed 's/\[/\n\[/g' | sed '0~3 a\\' | head -100
```

> Eventually this has a little flaw. If the title has an start bracket `[`
> the new line created by sed will throw the three line spacing count off?

That should be enough exploration to help with understanding what is in the file
'nasa_keywords.json' .
