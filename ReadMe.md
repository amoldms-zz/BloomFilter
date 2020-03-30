# Bloom Filter with Spell checker

Bloom Filter is probabilistic data structure designed to check, quickly and memory-efficiently, whether an element is present in a set. This is very useful in applications like spell checker, domain availability checker, azure resource name availability checker, database systems, web crawler service etc.

# Project structure

 README.md
 License.md
 requirements.txt
 apps/spell_checker.py
 apps/other_apps.py
 bloom_filter/bloomfilter.py
 bloom_filter/bloomfilter_interface.py
 middletier/spell_service.py
 middletier/logger.py
 middletier/dal/filesystem_dal.py
 data/dictionary.csv
 data/test_document.csv

# Prerequisites

- Python 3.6+
- Package requirements listed in requirements.txt
- File with dictionary words (sample included)
- Document to be spell checked (sample included)

# Running the spell checker:

  python -m apps.spell_checker 
  python -m apps.spell_checker -f "data/test_document.csv"

# Authors

  Amol Dhaygude

# License

This project is licensed under the MIT License - see the LICENSE.md file for details.
