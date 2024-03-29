import sys
import atexit

def run_bot(bot_class, conf_fields={}):
    '''Create a new bot of bot_class and run it'''
    try:
        instance = None
        token, conf = get_bot_token_and_conf(conf_fields)
        instance = bot_class(token, **conf)
        atexit.register(instance.cleanup)
        instance.run()
    except:
        print('Error running bot - token or configuration is probably invalid')
        if instance is not None:
            instance.cleanup()
        raise

def get_bot_token_and_conf(conf_fields=[]):
    '''Try to get configuration for the bot from argv.
    If there is no argv then get it from input().
    configuration includes bot token and the things
    specified in require_fields

    conf_fields should be like so:
    {somevar: int, someothervar: str, somevarvar: float, someboolvar: bool}

    argv format should be like so:
    python bot_file.py mytokenhere somevalue=123 othervalue=456
    '''
    
    if len(sys.argv) > 1:
        token = sys.argv[1]
        conf = {}
        for arg_idx in range(2, len(sys.argv)):
            arg_var = sys.argv[arg_idx]
            field = arg_var.split('=', 1)[0]
            field_value = arg_var.split('=', 1)[1]
            if field not in conf_fields:
                raise RuntimeError(f'Unexpected command line argument: {field}')
            conf[field] = read_conf_field(conf_fields[field], field_value)
    else:
        token = input('Paste the bot token here and press enter: ')
        conf = {}
        for field in conf_fields:
            field_type = conf_fields[field]
            field_value = input(f'Enter value of {field} ({field_type.__name__}): ')
            conf[field] = read_conf_field(conf_fields[field], field_value)
    
    return (token, conf)

def read_conf_field(field_type, value):
    if field_type == int:
        return int(value)
    elif field_type == float:
        return float(value)
    elif field_type == bool:
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        else:
            raise ValueError('Boolean value expected for field')
    elif field_type == str:
        return value
    else:
        raise ValueError(
            f'Unsupported conf var type: {field_type}')
        