import click
import colors
import datetime
from dateutil import parser
'''
todo:
    make colormap a passable param
'''

colormapping = (
        (datetime.timedelta(minutes=10), colors.green),
        (datetime.timedelta(hours=3), colors.yellow),
        (datetime.timedelta(hours=12), colors.magenta),
        (None, colors.red)
        )

def get_age_timedelta(timestamp_string, pattern):
    if pattern is None:
        output = datetime.datetime.now() - parser.parse(timestamp_string)
    else:
        output = datetime.datetime.now() - datetime.strptime(timestamp_string, pattern)
    return output

def get_colorfn_from_timedelta(age_td, colormapping=colormapping):
    # Find our else_color
    else_color = map(lambda c: c[1], filter(lambda cm: cm[0] is None, colormapping))[0]
    # remove else_color from colormapping
    colormapping = filter(lambda cm: cm[0] is not None, colormapping)
    colormapping = sorted(colormapping, key=lambda cm: cm[0]) # make sure the timestamps are soonest-first
    
    # Check if the age of the timestamp is older than one of the defined thresholds
    for colormap in colormapping:
        if age_td < colormap[0]:
            return colormap[1] # Return early when we have a match

    # if we haven't found a colormap, it must be older than the last threshold, use else_color
    return else_color

@click.command()
#@click.option('--pattern', default="%Y-%m-%d %H:%M", help="Python strptime format string")
@click.option('--pattern', default=None, help="Python strptime format string, guess if none provided")
@click.option('--date-field', default=2, help="Field to extract timestamp from")
@click.option('--field-sep', default="\t", help="Field Seperator")
@click.argument('infile', default="-") #, help="File to process, - for stdin")
def color_by_age(pattern,date_field, field_sep, infile):
    with click.open_file(infile, "r") as infile:
        for line in infile:
            try:
                age = get_age_timedelta(line.split(field_sep)[date_field-1], pattern)
                colorfn = get_colorfn_from_timedelta(age)
                click.echo(colorfn(line), nl=False)
            except:
                click.echo(line, nl=False)


if __name__ == "__main__":
    color_by_age()
