import ConfigParser as configparser


class IniConfig(dict):
    def __init__(self, filenames):
        try:
            config = configparser.ConfigParser(allow_no_value=True)
        except NameError:
            config = configparser.ConfigParser()
        config.read(filenames)

        # Iterate over each section
        for section in config.sections():
            bits = section.split(':')
            key = bits[0].lower()

            # Special django sections
            if key in ('cache', 'database'):
                bits[0] = (key + 's').upper()

                if len(bits) == 1:
                    bits.append('default')

            # Look for any django section
            elif key == 'django':
                bits.pop(0)

                if len(bits) >= 1:
                    bits[0] = bits[0].upper()

            # Ignore other sections
            else:
                continue

            for option in config.options(section):
                current = self
                k, v = bits + [option.upper()], config.get(section, option)

                for bit in k[:-1]:
                    current = current.setdefault(bit, {})
                # Now assign value to current position
                try:
                    current[k[-1]] = v
                except TypeError: # Special-case if current isn't a dict.
                    current = {k[-1]: v}
