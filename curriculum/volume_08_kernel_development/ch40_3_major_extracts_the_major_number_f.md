3. MAJOR() extracts the major number for logging.
4. exit: tear down in REVERSE order of creation — destroy device, class, cdev, region, then free the buffer.
Mirror-image cleanup prevents leaks and dangling references.