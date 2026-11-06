def retry(operation):
    """Run an operation, retrying ConnectionError up to three total attempts."""
    for attempt in range(3):
        try:
            return operation()
        except ConnectionError:
            if attempt == 2:
                raise
