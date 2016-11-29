# COMP 479 Project

# Read output from crawler

* Make sure to install jsonlines:

```bash
	pip install jsonlines
```

* Read the output as follows

```python
from __future__ import print_function

import glob, os

import jsonlines

os.chdir("sample_output")
for f in glob.glob("*.jsonl"):
	with jsonlines.open(f) as reader:
		for obj in reader:
			# WARNING: The string in obj are encoded with unicode.
			print(u"Field: {}".format(obj['field']))
			print(u"url: {}".format(obj['url']))
			print(u"title: {}".format(obj['title']))
			print(u"text: {}".format(obj['text']))

```
