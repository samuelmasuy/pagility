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
			print("Field: {}".format(obj['field']))
			print("url: {}".format(obj['url']))
			print("title: {}".format(obj['title']))
			print("text: {}".format(obj['text']))
```
