import string
from bloom_filter.bloomfilter import BloomFilter
from pip._vendor.colorama import Fore
import middletier.dal.filesystem_dal as filedal
import middletier.logger as logger
import sys


def prepare_dictionary_bloom():
    """ Adds dictionary words to bloom filter object
    ...
    Parameters
    ----------
    bloom_filter : object
        The bloom filter object
    filepath : string
        The dictionary file path

    """
    try:
        # Get parameters for bloom filter and data file locations
        num_words, probability, case_sensitive, dictionary_path = get_config_parameters()

        # Instantiate a bloom filter object
        bloom_filter = BloomFilter(num_words, probability, case_sensitive)
        vebose_info(bloom_filter)

        # Get list of dictionary words to be added to bloom filter
        word_list = get_words(dictionary_path)

        # Add all items from dictionary to bloom filter
        bloom_filter.bulk_add(word_list)

        # Check bloom filter counter
        if bloom_filter.counter > 0.95 * bloom_filter.items_count or bloom_filter.delete_threshold:
            refresh_bloom_filter()

        return bloom_filter
    except Exception as e:
        logger.log(str(e))
        sys.exit(1)

def get_words(filepath):
    """ Reads and processes dictionary file, returns dictionary word list
    ...
    Parameters
    ----------
    filepath : string
        The dictionary file path

    Returns
    -------
    set
        Set of unique dictionary words
    """
    # Add all items from dictionary to bloom filter
    try:
        document = filedal.get_data(filepath)
        words = set(tokenize_words(document))
        return words
    except RuntimeError as e:
        logger.log(str(e))
    except Exception as e:
        logger.log(str(e))
        sys.exit(1)


def tokenize_words(text):
    """ Tokenize words
    ...
    Parameters
    ----------
    text : string
        The content of dictionary file and test document to be spell checked

    Returns
    -------
    list
        List of tokenized words
    """
    # Tokenize words from paragraph, Strip punctuations and digits from paragraph text
    try:
        text = text.translate(str.maketrans('', '', string.punctuation)). \
            translate(str.maketrans('', '', string.digits))
        word_list = [word for word in text.split()]
        return word_list
    except RuntimeError as e:
        logger.log(str(e))
    except Exception as e:
        logger.log(str(e))
        sys.exit(1)


def spell_check(bloom_filter, filepath):
    """ Runs spell checker of document to be spell checked
    ...
    Parameters
    ----------
    bloom_filter : object
        The bloom filter object
    filepath : string
        The file path for document to be spell checked
    """
    test_words = get_words(filepath)
    for word in test_words:
        if not (bloom_filter.contain(word)):
            handle_misspelled(bloom_filter, word)
    logger.log(Fore.GREEN + "Spell check complete. Great language skills!!")


def handle_misspelled(bloom_filter, word):
    """ Prompt user for misspelled words add/ignore
        Add user suggested word to bloom filter
    ...
    Parameters
    ----------
    bloom_filter : object
        The bloom filter object
    word : string
        The misspelled word

    """
    try:
        print(Fore.RED + "Misspelled word:", word)
        user_input = input(Fore.BLUE + "Add to dictionary (A/a) or Skip to Ignore >>" + Fore.GREEN)
        if str(user_input).lower() == 'a':
            bloom_filter.add(word)
            logger.log(Fore.BLUE + "Word "'"{}"'" added to dictionary:".format(word))
            # Check bloom filter counter, only when new words are added
            if bloom_filter.counter > 0.95 * bloom_filter.items_count  or bloom_filter.delete_threshold:
                refresh_bloom_filter()
    except Exception as e:
        logger.log(str(e))


def refresh_bloom_filter():
    # ToDo: Implement Primary/Secondary bloom filter swap that will handle resize/deletion requirements
    # Application maintains copy of original items list as well as adhoc added items
    # When item counter threshold is reached or deletion criterion is met, create secondary bloom filter object
    # Switch primary bloom filter object with secondary
    # This will ensure bloom filter meets false positive probability requirements or delete use case if applicable.
    try:
        logger.log("Resize")
    except Exception as e:
        logger.log(str(e))


def get_config_parameters():
    """ Returns user configured application config file
    ...

    Returns
    -------
    tuple
        Tuple of items count, false positive probability, case sensitivity, dictionary file path, test document path
    """
    try:
        config = filedal.read_config("spell_checker_config.ini")
        num = int(get_config_value(config, "CONFIG_DEFAULT", "num_words"))
        prob = float(get_config_value(config, "CONFIG_DEFAULT", "probability"))
        case = bool(get_config_value(config, "CONFIG_DEFAULT", "case_sensitivity"))
        dict_path = str(get_config_value(config, "CONFIG_DEFAULT", "dictionary_path"))
        return num, prob, case, dict_path
    except Exception as e:
        sys.exit(str(e))


def get_config_value(config, section, key):
    """ Returns config values for given key
    ...
    Parameters
    ----------
    config: object
        The config file object
    section : string
        The config section
    key : string
        The config key

    Returns
    -------
    string
        Config value for given key
    """
    try:
        if config.has_option(section, key):
            return config.get(section, key)
        else:
            raise ValueError("Missing value for parameter: " + key)
    except ValueError as e:
        logger.log(str(e))
        sys.exit(1)


def vebose_info(bloom_filter):
    logger.log("Expected number of items to be added in Bloom filter:{}".format(bloom_filter.items_count))
    logger.log("Expected false positive probability:{}".format(bloom_filter.probability))
    logger.log("Case sensitive for bloom filter:{}".format(bloom_filter.case_sensitive))
    logger.log("Bloom filter size that meets above requirements in MB:{}".format(
            round(bloom_filter.filter_size / 8e+6, 2)))
    logger.log("Number of hash functions needed to meet above requirements:{}".format(bloom_filter.hash_count))


# ToDo: Granular exception handling implementation for null check, data type mismatch for all functions
