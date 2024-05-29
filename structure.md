# About Victoria 3's savefiles

Nothing really important here, just information that will help me build a parser for the files.

## Declaration
Seems to be a weird spinoff of json and works as follows:
```[identifier] = [data]```
Different identifiers are ALWAYS separated by new lines

## Types

- Arrays: Are declared between curly braces, the data stored inside is separated by spaces and doesn't have identifiers.
- Objects: Declared with curly braces similar to objects but the data stored inside has identifiers and can be of any type
- Booleans: `yes` or `no`
- Integers
- Floats
- Strings

NB: Some arrays seem to have data associated with an identifier.

### Extract

```
176 = {
    is_main_tag=[Boolean]
    definition=[String]
    government=[government]
    ruler=[ruler_id]
    heir=[heir_id]
	capital=[capital_id]
	budget={
	    weekly_income=[Array:Float]
	    weekly_expenses=[Array:Float]
	    building_budget={
	        expenses=[Float]
	        incomes=[Float]
	        gov_goods_expenses=[Array:Float]
	        ...
	    }
	    credit=[Float]
	    investment_pool=[Float]
	    weekly_investment_pool_change_from_construction=[Float]
	    gdp={
	        ...
	        [values]=[Array:Float]
	    }
	}
	...
}
```

Somebody fucked up the indentation going onwards, when fixed it looks like this:
```
gdp={
	sample_rate=28
	count=5214
	channels={
		0={
			date=1935.12.28
			index=5214
			values={data}
		}
	}
}
```

The identifier '0' always is inside the channels object.

`This should be enough for anyone to parse everything in the files and try to find data like that because manually looking inside the file is utterly painful and should be considered a crime considering the bad indentation and infinite amount of data.`