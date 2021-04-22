import logging
 
def logger_generator(log_path):
    ''' Output log to file'''
    # set log config
    logging.basicConfig(
                    level    = logging.ERROR,
                    format   = "\n%(asctime)s %(name)s:%(levelname)s:\n%(message)s",
                    datefmt  = '%Y-%m-%d %A %H:%M:%S',
                    filename = log_path,
                    filemode = 'a')                        # append log to file
    # Create an instance
    logger = logging.getLogger()
    return logger

logger = logger_generator("./console_out.log")

