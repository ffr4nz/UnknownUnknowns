import logging
import os

def getLoger(name, filepath, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s'):
    logging.basicConfig(level=logging.DEBUG,
                        format=format,
                        datefmt='%m-%d %H:%M')

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)



    # Create target Directory if don't exist
    if not os.path.exists(filepath):
      os.mkdir(filepath)
      print("Directory " , filepath ,  " Created ")

    # create file handler which logs even debug messages
    fh = logging.FileHandler(filepath + "/" + name + ".log")
    fh.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter(format)

    fh.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(fh)

    # 'application' code
    # logger.info('Starting logger ...')
    return logger;
