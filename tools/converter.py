def celsius_to_fahrenheit(celsius):
    """
    Convert Celsius to Fahrenheit.

    Parameters
    ----------
    celsius : int, float, or iterable of numbers
        Temperature in degrees Celsius.

    Returns
    -------
    float or list of floats
        Temperature in degrees Fahrenheit. Returns a single float for scalar
        input or a list of floats for iterable input.

    Examples
    --------
    >>> celsius_to_fahrenheit(0)
    32.0
    >>> celsius_to_fahrenheit([0, 100])
    [32.0, 212.0]
    """
    from numbers import Number

    # Single numeric value
    if isinstance(celsius, Number):
        return float(celsius) * 9.0 / 5.0 + 32.0

    # Attempt to treat as iterable
    try:
        return [float(x) * 9.0 / 5.0 + 32.0 for x in celsius]
    except TypeError:
        raise TypeError("Input must be a number or an iterable of numbers")