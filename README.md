# simplesitecheck
A simple site checker that runs a command on positive or negative regex match.

## Getting Started
The only dependency is Python 3.6+.

From any directory containing check.py and a config.json run with:

```bash
python check.py
```

This will run once, executing each site setup in your config file. See [configuration]() for setting up config.json

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
            "negative_test_regex": "example",
            "positive_test_regex": "slartibartfast",
            "command_on_fail": [
                "date",
                "-u"
            ],
            "seconds_between_retest": 100,
            "mailgun_config": {
                "api_key": "",
                "target_emails": [
                    "example@example.com"
                ]
            }
        }
    ]
}
```

### Site level configuration elements
#### site: name
A name for this site congiguration, this is only used for logging.

#### site: description
A simple description of what you are chekcing for to be kind to your future self. This is not used by the script.

#### site: target_uri
The uri to be checked

#### site: negative_test_regex
The check will be considered failing if this regex DOES match on the page.

#### site: positive_test_regex
The check will be considered failing if this regex DOES NOT match on the page.

#### site: command_on_fail
A single string or an array of strings which will be passed to Python's subprocess.call if the test fails.


### Top level configuration elements
#### log directory
This should be a valid absolute path where the log file should be created or appended to.

#### log level
simplesitecheck follows [Python's log level convention](https://docs.python.org/3/library/logging.html#levels).
