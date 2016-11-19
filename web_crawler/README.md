# Web crawler

## Install

Please use a `virtualenv` to install the dependencies.
See the [doc](https://virtualenv.pypa.io/en/stable/installation/) on how to
use.

### Dependencies

* Scrapy
```
pip install Scrapy
```
* Boilerpipe
```
pip install JPype1
pip install charade
pip install chardet
git clone https://github.com/misja/python-boilerpipe.git
cd python-boilerpipe
python setup.py install
cd ../
rm -rf python-boilerpipe
```
* Goose
```
pip install goose-extractor
```

## Usage

Please see `crawl.py` for reference.

Outputs in *jsonlines* format, in `./output` folder.

## Spiders

* artsci_biology
 - http://www.concordia.ca/artsci/biology.html
 - boilerpipe library
* artsci_biology_xpath
 - http://www.concordia.ca/artsci/biology.html
 - xpath selector
* artsci_biology_goose
 - http://www.concordia.ca/artsci/biology.html
 - Goose Extractor library.
* artsci_chemistry
 - http://www.concordia.ca/artsci/chemistry.html
 - boilerpipe library
* artsci_exercise_science
 - http://www.concordia.ca/artsci/exercise-science.html
 - boilerpipe library
* artsci_geography
 - http://www.concordia.ca/artsci/geography-planning-environment.html
 - boilerpipe library
* artsci_math
 - http://www.concordia.ca/artsci/math-stats.html
 - boilerpipe library
* artsci_physics
 - http://www.concordia.ca/artsci/physics.html
 - boilerpipe library
* artsci_psychology
 - http://www.concordia.ca/artsci/psychology.html
 - boilerpipe library
* artsci_science_college
 - http://www.concordia.ca/artsci/science-college.html
 - boilerpipe library
