from datetime import datetime, timedelta
from collections import defaultdict


def generate_time_slots(opening_time, closing_time, duration_minutes):
    """
    Generate time slots between opening and closing hours.

    Args:
        opening_time (time)
        closing_time (time)
        duration_minutes (int)

    Returns:
        list of (start_time, end_time)
    """
    slots = []
    current = datetime.combine(datetime.today(), opening_time)
    closing = datetime.combine(datetime.today(), closing_time)

    while current + timedelta(minutes=duration_minutes) <= closing:
        end = current + timedelta(minutes=duration_minutes)
        slots.append((current.time(), end.time()))
        current = end

    return slots


def group_tables_by_seating(tables):
    """
    Group tables under seating types.

    Returns:
        {
            "Indoor": [table1, table2],
            "Outdoor": [table3, table4]
        }
    """
    grouped = defaultdict(list)
    for table in tables:
        key = table.seating_type.name if table.seating_type else "Other"
        grouped[key].append(table)

    return grouped


def can_merge_tables(tables, required_capacity):
    """
    Check if selected tables can fulfill required capacity.

    Returns:
        (bool, total_capacity)
    """
    total_capacity = sum([t.capacity for t in tables])
    return total_capacity >= required_capacity, total_capacity




def replace_with_space(s):
    return s.replace('_', ' ').replace('-', ' ')



def calculate_end_datetime(start_datetime, duration_hours):
    # If it's a string, convert it
    if isinstance(start_datetime, str):
        start_datetime = datetime.strptime(start_datetime, "%Y-%m-%d %H:%M")

    end_datetime = start_datetime + timedelta(hours=duration_hours)
    return end_datetime



def combine_date_time(date_str: str, time_str: str) -> datetime:
    """
    Combines date and time strings into a single datetime object.

    Args:
        date_str (str): 'YYYY-MM-DD'
        time_str (str): 'HH:MM'

    Returns:
        datetime: Combined datetime object
    """

    try:
        combined_str = f"{date_str} {time_str}"
        return datetime.strptime(combined_str, "%Y-%m-%d %H:%M")
    except ValueError:
        raise ValueError("Invalid format. Expected date='YYYY-MM-DD' and time='HH:MM'")