# simplesitecheck
A simple site checker that runs a command on positive or negative regex match.

## Getting Started
The only dependency is Python 3.6+.

From any directory containing check.py and a config.json run with:

```bash
python check.py
```

This will run once, executing each site setup in your config file. See [configuration](https://github.com/kajuberdut/simplesitecheck/blob/master/README.md#configuration) for setting up config.json

In a production environment running once is not that helpful, in this case it would be best to [setup a cron job](https://lifehacker.com/learn-to-use-cron-from-the-command-line-399503) that runs at an interval of your chosing.


## configuration

Configuration files are normal json files which at minimum should have a root object with a 'sites' key containing an array of site configurations.
The root object can also contain a 'log_dir' and 'log_level'.

```json
{
    "log_dir": ".",
    "log_level": "DEBUG",
    "sites": [
        {
            "name": "Example Config",
            "description": "This is a sample description of what this config entry is checking.",
            "target_uri": "http://example.com",
            "test_type": "positive",
            "regex": "example",
            "command_on_fail": [
                "date",
                "-u"
            ],
        }
    ]
}
```

### Top level configuration elements
#### log directory
This should be a valid absolute path where the log file should be created or appended to.

#### log level
simplesitecheck follows [Python's log level convention](https://docs.python.org/3/library/logging.html#levels).

### Site level configuration elements
#### name
A name for this site congiguration, this is only used for logging.

#### description
A simple description of what you are chekcing for to be kind to your future self. This is not used by the script.

#### target_uri
The uri to be checked

#### test_type
Valid values are "positive" or "negative".
##### positive
The check fails if the regex DOES NOT match the page.
##### negative
The check fails if this regex DOES match on the page.

#### regex
The regex to be looked for in the page HTML.

#### command_on_fail
A single string or an array of strings which will be passed to Python's subprocess.call if the check fails.


