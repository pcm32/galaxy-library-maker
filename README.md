# galaxy-library-maker

This set of scripts facilitate the create of Galaxy libraries from files filesystem that the Galaxy
process has access to (currently this is the only mechanism supported, more could be added).

## Installation

Currently, a git clone + local pip install is required. We will add this to pypi soon.

- Clone this repo and cd inside.
- Create a python3 virtual environment:

```
python3 -m venv myVenvName
source myVenvName/bin/activate
pip install --upgrade pip
pip install wheel
```
- Install this package
```
pip install .
```

## Requirements for running

### Galaxy API key

You need to obtain a Galaxy API Key on the instance where you want the files loaded as Galaxy Libraries.
To obtain an API key, in the main Galaxy screen, go to User -> Preferences, and there click on
Manage API key. Copy the key text (or press `Create a new key` if there is none).

### YAML authentication file for Galaxy

You will need a YAML auth file for Galaxy, following the formatting from parsec:

```
__default: instance_a

instance_a:
    key: "94c9894706fd97b36dbd1acdaa88b749"
    url: "http://localhost:8080/"

instance_b:
    key: "kajshdkajsdhaksjh3ek3jeh327ycei"
    url: "http://my.galaxy.ins/"
```

Paste the Galaxy key and the appropiate URL (where you access Galaxy). You can have more than one instance
in the same YAML if desired (although will be only connection to one at once).

### Library definition YAML file

Libraries to be added to Galaxy are defined for this package in a YAML that follows this schema:

```
---
- library: 'My data project 1'
  desc: 'Descriptio about my data project'
  synopsis: 'A lot of expression data'
  base_dir: /path/to/files/on/a/filesystem/that/galaxy/can/see/and/read
  recursive: true
  extensions:
    - txt: txt
    - gtf: gtf
- library: 'Another project'
  desc: 'Desc about another project'
  synopsis: 'More cool data'
  base_dir: /other/path
  recursive: true
  extensions:
    - _sce.rds: rdata.sce
    - _tab.txt: tabular
```

You can have as many libraries on the same YAML, each one will become a separate library in Galaxy,
where all files that respond to the extensions listed in `extensions` will be made available, in the same
directory structure starting from the `base_dir`.

How do I know which datatypes are available in my Galaxy instance to use in the extensions part?

Galaxy datatypes are instance dependant and as such you need to know which datatypes are available in your instance.
To do this, you can execute the `get-datatypes.py` script:

```
get-datatypes.py -C creds.yaml -G instance_a
```

## Running

Assuming the above examples are available in creds.yaml and libs_def.yaml, and that the Galaxy instance where
those directories are available is `instance_a` (and that the virtualenv is activated):

```
load-into-galaxy-library.py -C creds.yaml -G instance_a -l libs_def.yaml
```

## Testing the package

Make sure that you have docker installed and that you can execute it without sudo, then run:

```
bash run_tests_with_containers.sh
```
