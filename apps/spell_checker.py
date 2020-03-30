import middletier.spell_service as service
import middletier.logger as logger
import argparse


def main(document_path):
    # Prepare dictionary bloom filter
    logger.log("Preparing dictionary bloom filter")
    bloom_filter = service.prepare_dictionary_bloom()

    # Run spell checker on test document
    logger.log("Spell checking document with bloom filter")
    service.spell_check(bloom_filter, document_path)


if __name__ == "__main__":
    """ Spell checker application main method
        Creates bloom filter using specified items count, false positive probability and case sensitivity 
        Runs spell checker on test document using dictionary bloom filter object

    """
    parser = argparse.ArgumentParser(description=' Parameters for Spell check program ')
    parser.add_argument('-f', '--file', type=str, default='data/test_document.csv',
                        dest="filename", help='File path for document')
    args = parser.parse_args()
    main(args.filename)
