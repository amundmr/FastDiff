#importing module
import logging

class logger():
    """Logger class contains all logging details for fastdiff"""
    
    def __init__(self, level):
        """Initializes logger"""
        #Create and configure logger
        logging.basicConfig(filename="fastdiff.log",
                            format='%(asctime)s %(message)s',
                            filemode='w')
        
        #Creating an object
        logger=logging.getLogger()
        
        #Setting the threshold of logger
        if 
        logger.setLevel(logging.DEBUG)
  
if __name__ == "__main__":
    logger = logger(10)
    #Test messages
    logger.debug("Harmless debug Message")
    logger.info("Just an information")
    logger.warning("Its a Warning")
    logger.error("Did you try to divide by zero")
    logger.critical("Internet is down")